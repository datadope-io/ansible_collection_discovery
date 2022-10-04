# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

from ansible.module_utils.six import text_type
from ansible.utils.display import Display

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.parsers.__init__ \
    import SoftwareFactsParser

REMOVE_COMMENTS_REGEX = r"(?m)\s*<delimiter>.*$"
EXTRACT_KEY_VALUE_REGEX = r"(\b\w+)\s*=\s*(.*?(?=\s\w+= |$))"

display = Display()


class Parser(SoftwareFactsParser):

    def validate_input(self, source, config):
        pass

    @staticmethod
    def remove_comments(text, delimiter):
        regex = REMOVE_COMMENTS_REGEX.replace('<delimiter>', re.escape(delimiter))
        return re.sub(regex, '', text, 0, re.MULTILINE)

    @staticmethod
    def extract_key_value(line, delimiters):
        line = line.strip()
        if line:
            for delimiter in delimiters:
                if delimiter != '=':
                    line = line.replace(delimiter, '=', 1)
                regex = EXTRACT_KEY_VALUE_REGEX
                matches = re.findall(regex, line)
                if matches and len(matches[0]) > 1:
                    return matches[0][0].strip(), matches[0][1].strip()
            return None, None
        else:
            return None, None

    def parse(self, source, config=None, path_prefix=''):
        if config is None:
            config = {}
        config.setdefault('separators', ['='])
        config.setdefault('comment_delimiters', ['#'])
        # if isinstance(config['separators'], text_type):
        #     config['separators'] = [char for char in config['separators']]
        # if isinstance(config['comment_delimiters'], text_type):
        #     config['comment_delimiters'] = [char for char in config['comment_delimiters']]
        result = {}
        for comment_delimiter in config['comment_delimiters']:
            source = self.remove_comments(source, comment_delimiter)
        for line in source.splitlines():
            key, value = self.extract_key_value(line, config['separators'])
            if key:
                result[key.strip("'")] = value.strip("'")
        return result
