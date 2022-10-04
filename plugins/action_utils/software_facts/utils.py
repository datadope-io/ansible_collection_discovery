# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import re
import sys

from ansible.errors import AnsibleRuntimeError
from ansible.module_utils.six import iteritems
from ansible.utils.display import Display

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.__init__ \
    import import_module
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.parsers.__init__ \
    import SoftwareFactsParser
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin


extra_plugins_var = 'SOFTWARE_DISCOVERY_EXTRA_PLUGINS_PATH'
extra_parsers_var = 'SOFTWARE_DISCOVERY_EXTRA_PARSERS_PATH'

display = Display()


def to_snake_case(string):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def to_camel_case(string):
    return ''.join(word.title() for word in string.split('_'))


def _import_files(files_path):
    main_path = os.path.dirname(__file__) + '/' + files_path
    for root, dirs, files in os.walk(main_path):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for filename in files:
            filename, extension = os.path.splitext(filename)
            if extension.lower() == '.py' and not filename.startswith('_'):
                rel_dir = os.path.relpath(root, main_path)
                package = __package__ + '.' + files_path
                if rel_dir != '.':
                    package = '.'.join([package] + rel_dir.split('/'))
                import_module('{0}.{1}'.format(package, filename))


def _import_external_files(path_var):
    external_plugins_paths = set()
    if extra_plugins_var in os.environ:
        external_plugins_paths.update(os.environ[path_var].split(':'))
    for path in external_plugins_paths:
        if path not in sys.path:
            sys.path.append(path)
        for root, dirs, files in os.walk(path):
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']
            for filename in files:
                filename, extension = os.path.splitext(filename)
                if extension.lower() == '.py' and not filename.startswith('_'):
                    rel_dir = os.path.relpath(root, path)
                    module = []
                    if rel_dir != '.':
                        module.extend(rel_dir.split('/'))
                    import_module('.'.join(module + [filename]))


def _inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


# Load plugins
_import_files(files_path='plugins')
_import_external_files(path_var=extra_plugins_var)
_plugins_modules = dict((m.get_name(), m) for m in _inheritors(SoftwareFactsPlugin))
display.debug("Software Facts Plugins: {0}".format(
    ', '.join(["{0}={1}".format(name, m.__name__) for name, m in iteritems(_plugins_modules)])))

# Load parsers
_import_files(files_path='parsers')
_import_external_files(path_var=extra_parsers_var)
_parsers_modules = dict((m.get_name(), m) for m in _inheritors(SoftwareFactsParser))
display.debug("Software Facts Parsers: {0}".format(
    ', '.join(["{0}={1}".format(name, m.__name__) for name, m in iteritems(_parsers_modules)])))


def get_software_facts_plugin(name, action_module, task_vars):
    klass = _plugins_modules.get(name)
    if klass:
        return klass(action_module, task_vars)
    raise AnsibleRuntimeError("Software Facts plugin {0} not found".format(name))


def get_software_facts_parser(name, action_module, task_vars):
    klass = _parsers_modules.get(name)
    if klass:
        return klass(action_module, task_vars)
    raise AnsibleRuntimeError("Software Facts parser '{0}' not found".format(name))
