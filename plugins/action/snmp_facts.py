# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import os

from ansible.plugins.action import ActionBase

from ansible_collections.datadope.discovery.plugins.action_utils.snmp_utils.utils import processed_templating_result, \
    get_info_by_sysobject, get_snmp_yml_file, get_snmp_json_file, get_brand_by_sysobject


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp=tmp, task_vars=task_vars)

        params = self._task.args
        params['_pre_check'] = False
        self.get_snmp_facts(result, params, task_vars)

        return result

    def get_snmp_facts(self, result, params, task_vars):
        if not params.get('_pre_check'):
            result.update(self.execute_snmp_module(
                module_args=params,
                task_vars=task_vars
            ))

            params['_pre_check'] = True
            if 'ansible_facts' in result and 'snmp' in result['ansible_facts'] \
                    and 'sysObjectId' in result['ansible_facts']['snmp']:
                snmp_info = get_info_by_sysobject(
                    sysobject_ids_file=get_snmp_yml_file(params.get('sysobject_ids')),
                    snmp_sysobjectid=result['ansible_facts']['snmp']['sysObjectId']
                )
                if 'brand' not in snmp_info:
                    snmp_info.update(get_brand_by_sysobject(
                        sysobjectid=result['ansible_facts']['snmp']['sysObjectId'],
                        enterprise_numbers=get_snmp_json_file(params.get('_enterprise_numbers'))
                    ))
                result['ansible_facts']['snmp_template'] = template = snmp_info.pop('template')
                result['ansible_facts']['snmp'].update(snmp_info)

                if template and not params.get('_template_content'):
                    params['_template_content'] = get_snmp_yml_file(
                        os.path.join(
                            params.get('templates_path'), "{0}.yaml".format(template)
                    ))
                self.get_snmp_facts(result, params, task_vars)
            else:
                return result

        if params.get('_pre_check') and params.get('_template_content'):
            snmp_info = self.execute_snmp_module(
                module_args=params,
                task_vars=task_vars
            )

            if 'ansible_facts' in snmp_info and 'snmp' in snmp_info['ansible_facts']:
                return result['ansible_facts']['snmp'].update(
                    processed_templating_result(
                        params.get('_template_content', {}),
                        snmp_info['ansible_facts']['snmp']
                    )
                )
            
            return snmp_info

        return result

    def execute_snmp_module(self, module_args=None, task_vars=None):
        return super(ActionModule, self)._execute_module(
            module_name='datadope.discovery.snmp_facts',
            module_args=module_args,
            task_vars=task_vars
        )
