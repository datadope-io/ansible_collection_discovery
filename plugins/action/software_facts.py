# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import ctypes
import os.path
import re
import threading
import time
import traceback
from copy import deepcopy

from ansible.errors import AnsibleRuntimeError
from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.module_utils.six import iteritems, text_type, binary_type
from ansible.parsing.utils.yaml import from_yaml
from ansible.playbook.conditional import Conditional
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.__init__ \
    import merge_hash, isidentifier, ArgumentSpecValidator

DEFAULT_LOOP_VAR = '__item__'

display = Display()


def raise_exception_in_thread(thread, exception):
    ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), ctypes.py_object(exception))


class PluginTimeoutException(BaseException):
    pass


class ThreadStorage:
    result = None
    exception = None


class GenericDetector:
    def __init__(self, software_config):
        self.software_config = software_config
        self._result = []

    @classmethod
    def clear_process_listening_ports_objects(cls, process):
        if 'listening_ports_objects' in process:
            del process['listening_ports_objects']
        if process['pid'] != process['ppid']:
            for child in process.get('children', []):
                cls.clear_process_listening_ports_objects(child)

    def remove_listening_ports_objects(self):
        for sw in self._result:
            process = sw['process']
            self.clear_process_listening_ports_objects(process)

    def get_software(self):
        return self._result

    def fill_process_info(self, hierarchical_processes_by_pid):
        tested_pids = []
        used_pids = set()
        software_processes = []
        for pid, process in iteritems(hierarchical_processes_by_pid):
            if pid not in used_pids and process['cmdline']:
                self._check_process_hierarchy(hierarchical_processes_by_pid, process, software_processes,
                                              tested_pids, used_pids)
        self._result = software_processes
        return used_pids

    def _check_process_hierarchy(self, hierarchical_processes_by_pid, process, software_processes,
                                 tested_pids, used_pids):
        found = False
        ppid = process['ppid']
        if int(ppid) > 0 and ppid not in tested_pids and ppid not in used_pids \
                and ppid in hierarchical_processes_by_pid:
            tested_pids.append(ppid)
            found = self._check_process_hierarchy(hierarchical_processes_by_pid, hierarchical_processes_by_pid[ppid],
                                                  software_processes, tested_pids, used_pids)
        if not found:
            found = self._check_process_is_sw(hierarchical_processes_by_pid, process, software_processes, used_pids)
        return found

    def _children_pids(self, process, pids):
        for p in process.get('children', []):
            if p['pid'] != process['pid']:
                pids.add(p['pid'])
                self._children_pids(p, pids)

    def _check_process_is_sw(self, hierarchical_processes_by_pid, process, software_processes, used_pids):
        if not process['cmdline']:
            return False
        if re.search(self.software_config['cmd_regexp'], process['cmdline'], re.IGNORECASE):
            if self.software_config['process_type'] == 'child':
                process_to_append = hierarchical_processes_by_pid[str(process['ppid'])]
            else:
                process_to_append = process
            # Detected process and children processes should not be used to detect other software
            used_pids.add(process_to_append['pid'])
            self._children_pids(process_to_append, used_pids)
            # used_pids.update(x['pid'] for x in process_to_append.get('children', []))
            software_processes.append({
                'type': self.software_config['name'],
                'process': process_to_append
            })
            return True
        return False

    @classmethod
    def get_children_listening_ports(cls, process):
        listening_ports = set()
        listening_ports_objects = list()
        for child in process.get('children', []):
            listening_ports.update(child.get('listening_ports', []))
            listening_ports_objects.extend(child.get('listening_ports_objects', []))

            if child['pid'] != child['ppid']:
                children_listening_ports, children_listening_ports_objects = cls.get_children_listening_ports(child)
                listening_ports.update(children_listening_ports)
                listening_ports_objects.extend(children_listening_ports_objects)

        return listening_ports, listening_ports_objects

    def fill_global_listening_ports_and_bindings(self):
        for sw in self._result:
            ports = set()
            ports_objects = list()
            bindings = list()

            process = sw['process']
            ports.update(process.get('listening_ports', []))
            ports_objects.extend(process.get('listening_ports_objects', []))

            children_listening_ports, children_listening_ports_objects = self.get_children_listening_ports(process)
            ports.update(children_listening_ports)
            ports_objects.extend(children_listening_ports_objects)

            for port_object in ports_objects:
                bindings.append({
                    'address': port_object['address'],
                    'port': port_object['port'],
                    'protocol': port_object['protocol'],
                    'class': 'service'
                })

            sw['listening_ports'] = sorted(list(ports))
            sw['bindings'] = bindings

    def fill_software_packages(self, packages):
        package_list = []
        pkg_regex = self.software_config.get('pkg_regexp')
        if pkg_regex:
            for pkg in packages:
                if re.search(pkg_regex, pkg, re.IGNORECASE):
                    package_list.extend(packages[pkg])
        for sw in self._result:
            sw['packages'] = package_list
        return package_list

    @staticmethod
    def _get_related_pids_for_process(sw_process, process_by_pid):
        pids = [sw_process['pid']] + [x['pid'] for x in sw_process.get('children', [])]
        parent = sw_process['ppid']
        while int(parent) > 1:
            pids.append(parent)
            parent = process_by_pid[parent]['ppid']
        return pids

    def fill_docker_info(self, dockers, process_by_pid):
        for container in dockers.get('containers', []):
            docker_pid = container.get('State', {}).get('Pid')
            if docker_pid:
                for sw in self._result:
                    process = sw['process']
                    related_pids = self._get_related_pids_for_process(process, process_by_pid)
                    if str(docker_pid) in related_pids:
                        exposed_ports = container['Config'].get('ExposedPorts', {})
                        # All docker data exposed to be usable from plugins.
                        # It will be reduced to a few fields at the end of the process
                        sw['docker'] = {
                            'id': container['Id'],
                            'name': container['Name'],
                            'image': container['Config']['Image'],
                            'network_mode': container['HostConfig']['NetworkMode'],
                            'exposed_ports': exposed_ports,
                            'port_bindings': container['HostConfig']['PortBindings'] or {},
                            'full_data': container
                        }
                        # Listening ports of all related pids are included
                        for pid in related_pids:
                            sw['listening_ports'].extend(process_by_pid[pid].get('listening_ports', []))
                        sw['listening_ports'] = sorted(list(set(sw['listening_ports'])))
                        # # If no port is available from host network, no port is mapped with host
                        # # but is the only port available so we assign to the port.
                        # if not process.get('listening_ports') and exposed_ports:
                        #     try:
                        #         port_list = [int(x.split('/')[0]) for x in exposed_ports.keys()]
                        #         process.setdefault('listening_ports', []).extend(port_list)
                        #         sw.setdefault('listening_ports', []).extend(port_list)
                        #     except ValueError:
                        #         display.v("Docker 'ExposedPorts' format unsupported: {0}".format(exposed_ports))
                        break

    def fill_versions_from_packages(self, matched_packages):
        for sw in self._result:
            version_list = sw.setdefault('version', [])

            package_versions = set()
            for package in matched_packages:
                if 'version' in package and package['version'] is not None:
                    package_versions.add(package['version'])

            version_list.extend([{'type': 'package', 'number': package_version}
                                 for package_version in package_versions])

    def fill_versions_from_docker(self):
        for sw in self._result:
            if 'docker' in sw:
                docker_version = re.findall(r".*:(.*$)", sw['docker']['image'])
                if len(docker_version) > 0:
                    version_list = sw.setdefault('version', [])
                    version_list.extend([{'type': 'docker', 'number': docker_version[0]}])

    def clear_data(self):
        for sw in self._result:
            if not self.software_config.get('return_children', False):
                if 'process' in sw and 'children' in sw['process']:
                    del sw['process']['children']
            if not self.software_config.get('return_packages', False):
                if 'packages' in sw:
                    del sw['packages']
            container = sw.get('docker')
            if container:
                sw['docker'].pop('full_data', None)


class ActionModule(ActionBase):
    @staticmethod
    def get_software_facts_plugin(name, action_module, task_vars):
        from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.utils \
            import get_software_facts_plugin
        return get_software_facts_plugin(name, action_module, task_vars)

    @classmethod
    def _get_software_facts_plugin(cls, name, action_module, task_vars, task):  # noqa
        """
        task parameter is only needed to facilitate testing - plugin mocking
        """
        return cls.get_software_facts_plugin(name, action_module, task_vars)

    def __init__(self, task, connection, play_context, loader, templar, shared_loader_obj):
        self.argument_spec = dict(
            software_list=dict(type='list', elements='dict', required=True),
            include_software=dict(type='list', elements='str', required=False),
            exclude_software=dict(type='list', elements='str', required=False),
            processes=dict(type='list', elements='dict', required=True),
            tcp_listen=dict(type='list', elements='dict', required=True),
            udp_listen=dict(type='list', elements='dict', required=True),
            packages=dict(type='dict', required=False),
            dockers=dict(type='dict', required=False),
            pre_tasks=dict(type='list', elements='dict', required=False),
            post_tasks=dict(type='list', elements='dict', required=False),
        )
        super(ActionModule, self).__init__(task, connection, play_context, loader, templar, shared_loader_obj)
        self._conditional = Conditional(self._loader)
        self._host = None
        self._current_loop_vars = {}

    def execute_module(self, module_name=None, module_args=None, tmp=None, task_vars=None, persist_files=False,
                       delete_remote_tmp=None, wrap_async=False):
        # Make method public
        return super(ActionModule, self)._execute_module(module_name=module_name, module_args=module_args,
                                                         tmp=tmp, task_vars=task_vars, persist_files=persist_files,
                                                         delete_remote_tmp=delete_remote_tmp, wrap_async=wrap_async)

    def run(self, tmp=None, task_vars=None):
        # individual modules might disagree but as the generic the action plugin, pass at this point.
        self._supports_check_mode = True
        self._supports_async = False
        result = super(ActionModule, self).run(tmp=tmp, task_vars=task_vars)
        del tmp
        if not result.get('skipped'):
            if not self._play_context.check_mode:
                self._host = task_vars['inventory_hostname']
                params = self._task.args
                if not self.validate_parameters(params):
                    raise AnsibleRuntimeError('Parameter validation failed')
                software_list = params['software_list']
                processes = params['processes']
                tcp_listen = params['tcp_listen']
                udp_listen = params['udp_listen']
                packages = params.get('packages')
                dockers = params.get('dockers')
                pre_tasks = params.get('pre_tasks')
                post_tasks = params.get('post_tasks')
                include_software = params.get('include_software')
                exclude_software = params.get('exclude_software') or []
                if include_software is None or "all" in include_software:
                    include_software = [x['name'] for x in software_list]
                software_list = [x for x in software_list
                                 if x['name'] in include_software and x['name'] not in exclude_software]
                sw_info = self.process_software(software_list=software_list,
                                                processes=processes,
                                                tcp_listen=tcp_listen,
                                                udp_listen=udp_listen,
                                                packages=packages,
                                                dockers=dockers,
                                                task_vars=task_vars,
                                                pre_tasks=pre_tasks,
                                                post_tasks=post_tasks)
                result['ansible_facts'] = {'software': sw_info}

        return result

    def _display_v(self, msg):
        display.v(msg, host=self._host)

    def validate_parameters(self, parameters):
        validator = ArgumentSpecValidator(self.argument_spec)
        validation_result = validator.validate(parameters)

        if validation_result.error_messages:
            display.warning("Wrong parameters sent to module:\n{0}".format('\n'.join(validation_result.error_messages)))

        return not bool(validation_result.error_messages)

    @classmethod
    def _prepare_processes(cls, processes):
        processes_by_pid = {}
        for p in processes:
            pid = str(p['pid'])
            if pid not in processes_by_pid:
                processes_by_pid[pid] = p
                processes_by_pid[pid]['children'] = []
            else:
                children = processes_by_pid[pid]['children']
                processes_by_pid[pid] = p
                processes_by_pid[pid]['children'] = children
            ppid = str(p['ppid'])
            if ppid not in processes_by_pid:
                processes_by_pid[ppid] = dict(pid=ppid, ppid='0', cmdline='', children=[])
            processes_by_pid[ppid]['children'].append(p)
        return {k: processes_by_pid[k] for k in sorted(processes_by_pid, key=int)}

    @classmethod
    def _add_listening_ports_to_processes(cls, processes_by_pid, listening_ports):
        for port in list(listening_ports):
            pid = str(port['pid'])
            if pid in processes_by_pid:
                # The object is always stored since it may contain additional information, like listening addresses
                processes_by_pid[pid].setdefault('listening_ports_objects', []).append(port)

                # Add port to listening_ports if it is not already there
                pid_listening_ports = processes_by_pid[pid].setdefault('listening_ports', [])
                if port['port'] not in pid_listening_ports:
                    pid_listening_ports.append(port['port'])
        for process in processes_by_pid.values():
            if 'listening_ports' in process:
                process['listening_ports'].sort()

    @classmethod
    def _adjust_ports_from_docker(cls, processes, dockers, tcp_listen, udp_listen):
        if dockers and "containers" in dockers.keys():
            docker_proxy_procs = [cl for cl in processes
                                  if "cmdline" in cl and cl['cmdline'] and "docker-proxy" in cl['cmdline']]
            for proc in docker_proxy_procs:
                container_ip = re.findall(r"-container-ip\s(\d*\.\d*\.\d*\.\d*)", proc['cmdline'])
                port_protocol = re.findall(r"-proto\s([a-z]{3})", proc['cmdline'])
                if len(container_ip) > 0:
                    matched = False
                    container_pid = None
                    for c in dockers['containers']:
                        if "NetworkSettings" in c:
                            if "IPAddress" in c['NetworkSettings'] \
                                    and container_ip[0] == c['NetworkSettings']['IPAddress']:
                                matched = True
                            else:
                                # FIXME: necessary if have IPAddress in NetworkSettings? (not matched)
                                for n in c['NetworkSettings'].get('Networks', {}).values():
                                    if "IPAddress" in n and container_ip[0] == n['IPAddress']:
                                        matched = True
                                        break
                        if matched:
                            container_pid = c.get('State', {}).get('Pid')
                            break

                    if container_pid:
                        container_port = {
                            'name': 'inferred',
                            'pid': container_pid
                        }

                        if len(port_protocol) > 0:
                            port_list = udp_listen if port_protocol[0] == 'udp' else tcp_listen
                            for p in port_list:
                                if str(p.get('pid')) == proc.get('pid'):
                                    port_list.append(dict(p, **container_port))
                                    break
                        else:
                            matched = False
                            for p in tcp_listen:
                                if str(p.get('pid')) == proc.get('pid'):
                                    tcp_listen.append(dict(p, **container_port))
                                    matched = True
                                    break
                            if not matched:
                                for p in udp_listen:
                                    if str(p.get('pid')) == proc.get('pid'):
                                        udp_listen.append(dict(p, **container_port))
                                        break

    @staticmethod
    def _adjust_version(instance):
        version = instance.get('version', [])
        version.sort(key=lambda x: x['type'])
        version.sort(key=lambda x: x['number'])

    @staticmethod
    def _adjust_packages(instance):
        packages = instance.get('packages', [])

        # Since a package could have None as name or version, we need to consider such cases and assume that
        # the value is '' in that cases, since sort does not accept None values.
        packages.sort(key=lambda x: x['name'] if x['name'] is not None else '')
        packages.sort(key=lambda x: x['version'] if x['version'] is not None else '')

    @staticmethod
    def _get_children_pids(children_processes):
        p = []
        for process in children_processes:
            p.append(process['pid'])
            children_processes = process.get("children", [])
            if children_processes:
                p.extend(ActionModule._get_children_pids(children_processes))
        return p

    def process_software(self, software_list, processes, tcp_listen, udp_listen, packages=None, dockers=None,
                         task_vars=None, pre_tasks=None, post_tasks=None):
        processes_by_pid = self._prepare_processes(processes)
        self._adjust_ports_from_docker(processes, dockers, tcp_listen, udp_listen)
        self._add_listening_ports_to_processes(processes_by_pid, tcp_listen + udp_listen)
        result = []
        processes_left = deepcopy(processes_by_pid)
        task_vars = {} if task_vars is None else task_vars
        _task_vars = task_vars.copy()
        for software_config in software_list:
            # Extend the task_vars with the extra vars of each software_config
            task_vars.update(software_config.get('vars', {}))

            # TODO: Allow using a custom detector depending on the software
            detector = GenericDetector(software_config)
            used_pids = detector.fill_process_info(processes_left)
            processes_left = dict((pid, x) for pid, x in iteritems(processes_left) if pid not in used_pids)
            detector.fill_global_listening_ports_and_bindings()
            detector.remove_listening_ports_objects()
            if packages:
                pkg_list = detector.fill_software_packages(packages)  # Keep data to use for getting sw version
                detector.fill_versions_from_packages(pkg_list)
            if dockers:
                detector.fill_docker_info(dockers, processes_by_pid)
                detector.fill_versions_from_docker()
            software_instances = detector.get_software()
            for instance in software_instances:
                self._execute_plugins(software_config, instance, task_vars, pre_tasks, post_tasks)
                if 'discovery_time' not in instance:
                    # Method to send time as iso format compatible with python 2.6 and not using external libs.
                    if time.daylight == 0:
                        offset = time.timezone
                    else:
                        offset = time.altzone
                    instance['discovery_time'] = "{time_str}+{offset:02d}:00".format(
                        time_str=time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime()),
                        offset=int(offset / -3600))
                self._adjust_version(instance)
                self._adjust_packages(instance)
                if instance.get('NOT_A_REAL_SOFTWARE_REMOVE_FROM_LIST', False):
                    recover_processes = [instance["process"]['pid']]
                    recover_processes.extend(ActionModule._get_children_pids(instance["process"].get('children', [])))
                    processes_left.update({x: y for x, y in iteritems(processes_by_pid) if x in recover_processes})
                    processes_left = {k: processes_left[k] for k in sorted(processes_left, key=int)}
                else:
                    result.append(instance)
            detector.clear_data()

            # After the execution of the software entry, revert the task_vars to its original state
            task_vars.clear()
            task_vars.update(_task_vars)
        return result

    @staticmethod
    def run_plugin(plugin, args, attributes, software_instance, wait_event, storage):
        try:
            plugin_result = plugin.run(args, attributes, software_instance)
            storage.result = plugin_result
        except SystemExit:
            pass
        except Exception as e:
            storage.exception = e
        finally:
            wait_event.set()

    @staticmethod
    def _parse_plugin_definition(plugin):
        desc = None
        name = None
        args = {}
        attributes = {}
        for k, v in iteritems(plugin):
            if k == 'name':
                desc = v
            elif k in PLUGIN_MODIFIER_KEYS:
                attributes[k] = v
            elif isinstance(v, (dict, list)):
                name = k
                args = v
            else:
                raise AnsibleRuntimeError("Unsupported attribute '{0}' for plugin definition '{1}'"
                                          .format(k, str(plugin)))
        if desc is None:
            desc = name
        return name, desc, args, attributes

    def _execute_plugins(self, software_config, software_instance, task_vars, pre_tasks=None, post_tasks=None):
        self._display_v("Executing custom plugins for software type '{0}'".format(software_config['name']))
        if pre_tasks is None:
            pre_tasks = []
        if post_tasks is None:
            post_tasks = []
        task_vars['__instance__'] = software_instance
        for task in pre_tasks:
            self._execute_plugin(task, software_instance, task_vars)
        for task in software_config.get('custom_tasks', []):
            self._execute_plugin(task, software_instance, task_vars)
        for task in post_tasks:
            self._execute_plugin(task, software_instance, task_vars)

    def _execute_plugin(self, plugin, software_instance, task_vars, in_block=None):
        name, desc, args, attributes = self._parse_plugin_definition(plugin)
        if name in ('block', 'include_tasks'):
            plugin = None
            if 'register' in attributes:
                display.warning("Ignoring 'register' attribute for plugin '{0}'".format(name))
                del attributes['register']
        else:
            plugin = self._get_software_facts_plugin(name, self, task_vars, desc)

        plugin_execution_data = None
        try:
            # Resolve only loop info to get item
            if 'loop' in attributes:
                plugin_execution_data = dict(task=desc, msg='', results=[])
                loop_items = self._replace_instance_vars(attributes['loop'])
                loop_control = attributes.get('loop_control', {})
                loop_var = loop_control.get('loop_var', DEFAULT_LOOP_VAR)
                index_var = loop_control.get('index_var')
            else:
                loop_items = ['__no_loop__']
                loop_var = None
                index_var = None

            for index, item in enumerate(loop_items):
                item_result_holder = dict(failed=False, skipped=False, msg="",
                                          invocation=dict(plugin_name=name, plugin_args=args))
                if item == '__no_loop__':
                    item = None
                    item_result_holder['task'] = desc
                    plugin_execution_data = item_result_holder
                else:
                    task_vars[loop_var] = item
                    if index_var:
                        task_vars[index_var] = index
                    self._current_loop_vars[loop_var] = item
                    item_result_holder[loop_var] = item
                    plugin_execution_data['results'].append(item_result_holder)  # noqa
                try:
                    self._execute_plugin_for_item_if_applies(args, attributes, desc, in_block, item,
                                                             name, plugin, item_result_holder,
                                                             software_instance, task_vars, index)
                finally:
                    if loop_var:
                        del (self._current_loop_vars[loop_var])
        finally:
            if plugin_execution_data.get('results'):
                # Calculate failed, skipped and msg of global result
                plugin_execution_data['msg'] = 'All items completed'

            self._store_plugin_result(attributes, task_vars, plugin_execution_data)

            display.debug("End execution of plugin '{0}' for task '{1}'{2}"
                          .format(name, desc, " in block '{0}'".format(in_block) if in_block else ""))

    def _execute_plugin_for_item_if_applies(self, args, attributes, desc, in_block, item, name, plugin,
                                            item_result_holder, software_instance, task_vars, index=0):
        env_vars_index = -1
        try:
            if self._check_conditions(attributes.get('when', []), task_vars):
                env_vars_index = self._execute_plugin_for_item(args, attributes, desc, in_block, item,
                                                               item_result_holder, name, plugin,
                                                               software_instance, task_vars, index)
            else:
                item_result_holder.update(dict(skipped=True))
                self._display_v("Skipping execution of plugin '{0}' for task '{1}'{2}{3} due to conditions"
                                .format(name, desc, " in block '{0}'".format(in_block) if in_block else "",
                                        " with item index {0}".format(index) if item is not None else ""))
        finally:
            if env_vars_index > -1:
                del self._task.environment[env_vars_index]

    def _execute_plugin_for_item(self, args, attributes, desc, in_block, item, item_result_holder, name,
                                 plugin, software_instance, task_vars, index=0):
        ignore_errors = boolean(attributes.get('ignore_errors', False))
        env_vars = attributes.get('environment', {})
        if env_vars:
            self._task.environment.append(self._replace_instance_vars(env_vars))
            env_vars_index = len(self._task.environment) - 1
        else:
            env_vars_index = -1
        keys_to_remove = []
        keys_to_update = {}
        if 'vars' in attributes:
            try:
                plugin_vars = self._replace_instance_vars(attributes['vars'])
            except Exception as e:
                self._display_v("{2} while resolving vars for plugin '{3}' for task '{0}': {1}".format(
                    desc, e, "Ignoring error" if ignore_errors else "FAILING: Error", name))
                item_result_holder.update(dict(failed=True, msg=str(e), exception=traceback.format_exc()))
                if ignore_errors:
                    return env_vars_index
                else:
                    raise
            else:
                for var_key, var_value in iteritems(plugin_vars):
                    if var_key in task_vars:
                        keys_to_update[var_key] = task_vars.get(var_value)
                    else:
                        keys_to_remove.append(var_key)
                task_vars.update(plugin_vars)

        try:
            plugins_to_include = None
            if name == 'include_tasks':
                try:
                    include_file_path = self._replace_instance_vars(args.get("file"))
                    if not include_file_path:
                        raise AnsibleRuntimeError("Missing argument 'file' for "
                                                  "'include_tasks' plugin '{0}'"
                                                  .format(desc))
                    include_file_path = os.path.abspath(include_file_path)  # noqa
                    plugins_to_include = self.get_plugins_from_file(include_file_path, desc)
                except Exception as e:
                    item_result_holder.update(dict(failed=True, msg=str(e), exception=traceback.format_exc()))
                    raise
            elif name == 'block':
                plugins_to_include = args
            if plugins_to_include is not None:
                item_result_holder['result'] = None
                try:
                    if not isinstance(plugins_to_include, list):
                        raise AnsibleRuntimeError("'{1}' plugin '{0}' needs a list of plugins as argument"
                                                  .format(desc, name))
                    else:
                        self._display_v("Executing plugin '{1}' for task '{0}'{2}'".format(
                            desc, name, " with item index {0}".format(index) if item is not None else ""))
                        try:
                            for p in plugins_to_include:
                                self._execute_plugin(p, software_instance, task_vars, in_block=desc)
                        except Exception as e:
                            self._display_v("{2} for plugin '{3}' for task '{0}': {1}".format(
                                desc, e, "Ignoring error" if ignore_errors else "FAILING: Error", name))
                            if not ignore_errors or isinstance(e, AssertionError):
                                raise
                except Exception as e:
                    item_result_holder.update(dict(failed=True, msg=str(e), exception=traceback.format_exc()))
                    raise
            else:
                self._display_v("Executing plugin '{0}' for task '{1}'{3}{2}".format(
                    name, desc, " with item index {0}".format(index) if item is not None else "",
                    " in block '{0}'".format(in_block) if in_block else ""))

                timeout = attributes.get('timeout', 0)
                try:
                    self._execute_plugin_for_item_async(args, attributes, desc, in_block, item, item_result_holder,
                                                        name, plugin, software_instance, timeout, index)
                    self._update_instance_facts(task_vars, item_result_holder)
                except Exception as e:
                    item_result_holder.update(dict(failed=True, msg=str(e), exception=traceback.format_exc()))
                    if ignore_errors and not isinstance(e, AssertionError):
                        self._display_v("Ignoring error for plugin '{0}' for task '{1}'{3}: {2}"
                                        .format(name, desc, e,
                                                " in block '{0}'".format(in_block) if in_block else ""))
                    else:
                        self._display_v("FAILING{3}: Error for plugin '{0}' for task '{1}': {2}"
                                        .format(name, desc, e,
                                                " BLOCK '{0}'".format(in_block) if in_block else ""))
                        raise
            return env_vars_index
        finally:
            for key in keys_to_remove:
                if key in task_vars:
                    del (task_vars[key])
            task_vars.update(keys_to_update)

    def get_plugins_from_file(self, include_file_path, desc):
        self._display_v("Including plugins from {0}".format(include_file_path))
        try:
            with open(include_file_path, 'rb') as f:
                plugins_to_include = from_yaml(f) or []
        except Exception as e:
            raise AnsibleRuntimeError("Cannot read file '{1}' for "
                                      "'include_tasks' plugin '{0}': {2}"
                                      .format(desc, include_file_path, str(e)))
        return plugins_to_include

    def _execute_plugin_for_item_async(self, args, attributes, desc, in_block, item, item_result_holder, name, plugin,
                                       software_instance, timeout, index=0):
        # Resolve everything using __instance__ e __item__ (loop_var)
        item_args = plugin.validate_args(self._replace_instance_vars(args))
        item_attributes = self._replace_instance_vars(attributes)
        wait_event = threading.Event()
        storage = ThreadStorage()
        plugin_run_thread = threading.Thread(target=self.run_plugin, args=(plugin,
                                                                           item_args,
                                                                           item_attributes,
                                                                           software_instance,
                                                                           wait_event,
                                                                           storage))
        plugin_run_thread.start()
        if timeout:
            self._display_v("Enabled timeout of {0} seconds for task '{1}'{3}{2}".format(
                timeout, desc, " with item index {0}".format(index) if item is not None else "",
                " in block '{0}'".format(in_block) if in_block else ""))
            finished = wait_event.wait(timeout)
            if not finished:
                raise_exception_in_thread(plugin_run_thread, SystemExit)
                self._display_v(
                    "Killed due to timeout of '{0}' seconds task '{1}'{3}{2}".format(
                        timeout, desc,
                        " with item index {0}".format(index) if item is not None else "",
                        " in block '{0}'".format(in_block) if in_block else ""))
                raise AnsibleRuntimeError("Plugin '{0}' timeout for task '{1}'{3}{2}".format(
                    name, desc,
                    " with item index {0}".format(index) if item is not None else "",
                    " in block '{0}'".format(in_block) if in_block else ""))
        else:
            plugin_run_thread.join()
        if storage.exception:
            self._display_v(
                "Exception while executing plugin '{0}' error task '{1}'{3}{2}".format(
                    name, desc,
                    " with item index {0}".format(index) if item is not None else "",
                    " in block '{0}'".format(in_block) if in_block else ""))
            raise storage.exception
        result = storage.result
        if result is not None:
            if not isinstance(result, dict):
                result = {'result': result}
            item_result_holder.update(result)

    def _replace_instance_vars(self, data):
        if isinstance(data, text_type):
            return self._templar.template(data.replace('<<', '{{').replace('>>', '}}'), cache=False)
        elif isinstance(data, binary_type):
            return self._replace_instance_vars(to_text(data))
        elif isinstance(data, list):
            new_list = []
            for element in data:
                new_list.append(self._replace_instance_vars(element))
            return new_list
        elif isinstance(data, dict):
            new_dict = {}
            for k, v in iteritems(data):
                new_dict[self._replace_instance_vars(k)] = self._replace_instance_vars(v)
            return new_dict
        else:
            return data

    @staticmethod
    def _update_instance_facts(task_vars, plugin_result):
        add_instance_vars = plugin_result.get('__instance__')
        if add_instance_vars:
            list_merge = plugin_result.pop('__list_merge__', 'replace')
            # use update to keep reference to original software_instance
            task_vars['__instance__'].update(merge_hash(task_vars['__instance__'],
                                                        add_instance_vars, list_merge=list_merge))

    def _store_plugin_result(self, attributes, task_vars, plugin_result):
        if 'register' in attributes:
            register_key = self._replace_instance_vars(attributes['register'])  # noqa
            if not isidentifier(register_key):
                raise AnsibleRuntimeError("Invalid variable name in 'register' specified: '%s'" % register_key)
            task_vars[register_key] = plugin_result

    def _check_conditions(self, conditions, all_vars):
        if isinstance(conditions, text_type):
            conditions = [conditions]
        for condition in conditions:
            self._conditional.when = [condition]
            test_result = self._conditional.evaluate_conditional(templar=self._templar, all_vars=all_vars)
            if not test_result:
                return False
        return True


PLUGIN_MODIFIER_KEYS = ['loop', 'register', 'when', 'ignore_errors', 'loop_control', 'environment', 'timeout', 'vars']
