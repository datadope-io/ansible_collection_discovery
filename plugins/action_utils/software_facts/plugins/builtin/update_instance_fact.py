# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
---
software_facts_plugin: update_instance_fact
short_description: Update currently set facts from processed instance
description:
    - This plugin allows updating existing variables.
options:
  updates:
    description:
      - A list of dictionaries, each a desired update to make.
    type: list
    elements: dict
    required: True
    suboptions:
      path:
        description:
        - The path in a currently set variable to update.
        - The path can be in dot or bracket notation.
        - It should be a valid jinja reference.
        type: str
        required: True
      value:
        description:
        - The value to be set at the path.
        - Can be a simple or complex data structure.
        type: raw
        required: True

author:
- Datadope based on ansible module I(update_fact) from Bradley Thornton (@cidrblock)
"""

EXAMPLES = r"""
- name: put notification_email_from
  update_instance_fact:
    updates:
      - path: configuration.global_defs.notification_email_from
        value: <<__instance__._notification_email_from>>
"""

import ast  # noqa: E402
import re  # noqa: E402
from jinja2 import Template, TemplateSyntaxError  # noqa: E402

from ansible.errors import AnsibleActionFail  # noqa: E402
from ansible.module_utils.common._collections_compat import MutableSequence  # noqa
from ansible.module_utils.common.text.converters import to_native  # noqa: E402
from ansible.utils.display import Display  # noqa: E402
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.__init__ \
    import MutableMapping  # noqa: E402
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402

display = Display()


class UpdateInstanceFact(SoftwareFactsPlugin):

    def __init__(self, action_module, task_vars):
        super(UpdateInstanceFact, self).__init__(action_module, task_vars)
        self._result = None

    @classmethod
    def get_args_spec(cls):
        # Dict of facts to create and their values
        return dict(updates=dict(type='list', required=True, elements='dict',
                                 options=dict(path=dict(type='str', required=True),
                                              value=dict(type='raw', required=True))))

    @staticmethod
    def _ensure_valid_jinja(args):
        """Ensure each path is jinja valid"""
        errors = []
        for entry in args["updates"]:
            try:
                Template("{{" + entry["path"] + "}}")
            except TemplateSyntaxError as exc:
                error = (
                    "While processing '{path}' found malformed path."
                    " Ensure syntax follows valid jinja format. The error was:"
                    " {error}"
                ).format(path=entry["path"], error=to_native(exc))
                errors.append(error)
        if errors:
            raise AnsibleActionFail(" ".join(errors))

    @staticmethod
    def _field_split(path):
        """Split the path into it's parts
        :param path: The user provided path
        :type path: str
        :return: the individual parts of the path
        :rtype: list
        """
        que = list(path)
        val = que.pop(0)
        fields = []
        field = ""
        try:
            while True:
                field = ""
                # found a '.', move to the next character
                if val == ".":
                    val = que.pop(0)
                # found a '[', pop until ']' and then get the next
                if val == "[":
                    val = que.pop(0)
                    while val != "]":
                        field += val
                        val = que.pop(0)
                    val = que.pop(0)
                else:
                    while val not in [".", "["]:
                        field += val
                        val = que.pop(0)
                try:
                    # make numbers numbers
                    fields.append(ast.literal_eval(field))
                except Exception:  # noqa
                    # or strip the quotes
                    fields.append(re.sub("['\"]", "", field))
        except IndexError:
            # pop'ed past the end of the que
            # so add the final field
            try:
                fields.append(ast.literal_eval(field))
            except Exception:  # noqa
                fields.append(re.sub("['\"]", "", field))
        return fields

    def set_value(self, obj, path, val):
        """Set a value
        :param obj: The object to modify
        :type obj: mutable object
        :param path: The path to where the update should be made
        :type path: list
        :param val: The new value to place at path
        :type val: string, dict, list, bool, etc
        """
        first, rest = path[0], path[1:]
        if rest:
            try:
                new_obj = obj[first]
            except (KeyError, TypeError):
                msg = "Error: the key '{first}' was not found " "in {obj}.".format(
                    obj=obj,
                    first=first,
                )
                raise AnsibleActionFail(msg)
            self.set_value(new_obj, rest, val)
        else:
            if isinstance(obj, MutableMapping):
                if obj.get(first) != val:
                    self._result["changed"] = True
                    obj[first] = val
            elif isinstance(obj, MutableSequence):
                if not isinstance(first, int):
                    msg = (
                        "Error: {obj} is a list, "
                        "but index provided was not an integer: '{first}'"
                    ).format(obj=obj, first=first)
                    raise AnsibleActionFail(msg)
                if first > len(obj):
                    msg = "Error: {obj} not long enough for item #{first} to be set.".format(
                        obj=obj,
                        first=first,
                    )
                    raise AnsibleActionFail(msg)
                if first == len(obj):
                    obj.append(val)
                    self._result["changed"] = True
                else:
                    if obj[first] != val:
                        obj[first] = val
                        self._result["changed"] = True
            else:
                msg = "update_fact can only modify mutable objects."
                raise AnsibleActionFail(msg)

    def run(self, args=None, attributes=None, software_instance=None):
        results = set()
        self._result = {"changed": False}
        self._ensure_valid_jinja(args)
        for entry in args["updates"]:
            parts = self._field_split(entry["path"])
            obj, path = parts[0], parts[1:]
            results.add(obj)
            if obj not in software_instance:
                msg = "'{obj}' was not found in the current facts.".format(obj=obj)
                raise AnsibleActionFail(msg)
            retrieved = software_instance.get(obj)
            if path:
                self.set_value(retrieved, path, entry["value"])
            else:
                if software_instance[obj] != entry["value"]:
                    software_instance[obj] = entry["value"]
                    self._result["changed"] = True

        for key in results:
            value = software_instance.get(key)
            self._result[key] = value
        return self._result
