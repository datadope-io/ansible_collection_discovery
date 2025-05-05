# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: print_var
short_description: Prints the given variable.
description:
     - Prints a given variable to the console.
     - Useful for testing.
options:
  var:
    description:
      - The name of the variable to be printed.
    type: str
    required: true
'''

EXAMPLES = r'''
  print_var:
    var: test_var
'''

from ansible import constants as C  # noqa
from ansible.errors import AnsibleUndefinedVariable  # noqa
from ansible.module_utils.common.text.converters import to_text, jsonify  # noqa
from ansible.utils.display import Display  # noqa

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.__init__ \
    import _TEMPLAR_HAS_TEMPLATE_CACHE

display = Display()


class PrintVar(SoftwareFactsPlugin):

    @classmethod
    def get_name(cls):
        return super(PrintVar, cls).get_name()

    @classmethod
    def get_args_spec(cls):
        args = super(PrintVar, cls).get_args_spec()
        args.update(dict(
            var=dict(type='str', required=True)))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        var = args['var']
        try:
            templar_args = dict(convert_bare=True, fail_on_undefined=True, cache=False)
            if not _TEMPLAR_HAS_TEMPLATE_CACHE:
                templar_args.pop('cache')

            results = self._templar.template(var, **templar_args)
            if results == var:
                # If var name is same as result, try to template it
                results = self._templar.template("{{" + results + "}}", **templar_args)
        except AnsibleUndefinedVariable as e:
            results = u"VARIABLE IS NOT DEFINED!"
            if display.verbosity > 0:
                results += u": %s" % to_text(e)

        if isinstance(results, (list, dict)):
            results = jsonify(results, indent=4)

        display.display("<{0}> {1} = {2}".format(self._task_vars['inventory_hostname'], var, results),
                        color=C.COLOR_OK)  # noqa
        return None
