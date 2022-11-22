# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import re

import yaml

try:
    from yaml import CSafeLoader as _SafeLoader
except ImportError:
    from yaml import SafeLoader as _SafeLoader

from ansible_collections.datadope.discovery.plugins.action_utils.snmp_utils.post_process import post_process


def index_dependency(dependency, destination_table, tagged_result):
    if 'index' in dependency:
        return _get_dependency_by_value(dependency, destination_table, tagged_result)


def _get_dependency_by_value(dependency, destination_table, tagged_result):
    attr = '_index'
    dependency_table = dependency['table']
    if dependency['index'].get('type') == 'value':
        attr = dependency['index'].get('name')
    for dest_dict in tagged_result.get(destination_table, {}).values():
        dest_value = dest_dict.get(attr)
        if dest_value:
            source_dict = dict(tagged_result.get(dependency_table, {}).get(dest_value, {}))
            if source_dict:
                source_dict.pop('_index')
                dest_dict.update(source_dict)


def get_info_by_sysobject(sysobject_ids_file, snmp_sysobjectid):
    result = {'template': 'generic_template'}
    stripped_oid = snmp_sysobjectid[13:] if snmp_sysobjectid.startswith('.') else snmp_sysobjectid[12:]
    for tpl in reversed(list(sysobject_ids_file.keys())):
        result.update(_get_info_by_template(tpl, sysobject_ids_file[tpl], stripped_oid))
        if 'model' not in result.keys() and tpl != list(sysobject_ids_file.keys())[0]:
            continue

        return result

    return result


def _get_info_by_template(template, brands, stripped_oid):
    for brand, snmp_types in brands.items():
        for snmp_type, oids in snmp_types.items():
            if stripped_oid in oids.keys():
                return _get_info_by_stripped_oid(template, brand, oids, stripped_oid, snmp_type)
        for snmp_type, oids in snmp_types.items():
            if stripped_oid.split('.')[0] in oids.keys():
                return _get_info_by_stripped_oid(template, brand, oids, stripped_oid.split('.')[0], snmp_type)

    return {}


def _get_info_by_stripped_oid(template, brand, oids, stripped_oid, snmp_type):
    return {k: v for k, v in {
        'template': template,
        'brand': brand,
        'model': oids.get(stripped_oid),
        'snmp_type': snmp_type
    }.items() if v is not None}


def get_brand_by_sysobject(sysobjectid, enterprise_numbers):
    if sysobjectid and enterprise_numbers:
        regex = r'.*1\.3\.6\.1\.4\.1\.(\d*).*'
        result = re.compile(regex).search(sysobjectid)
        if result:
            sys_brand = enterprise_numbers.get(result.group(1))
            return {'brand': sys_brand}

    return {}


def processed_templating_result(snmp_template, snmp_facts):
    indexed_results = snmp_facts.pop('_indexed_result', {})
    for val in snmp_template.values():
        remove_attrs = {}
        for key, cfg in val.items():
            if 'type' not in cfg.keys():
                process_func = post_process(cfg.get('post_process'))
                snmp_facts[key] = process_func(snmp_facts[key]) if process_func else snmp_facts[key]
                continue

            for attr, entry in cfg.get('entries', {}).items():
                process_func = post_process(entry.get('post_process'))
                for element in indexed_results.get(key, {}).values():
                    if attr in element:
                        element[attr] = process_func(element[attr]) if process_func else element[attr]

            for dependency in cfg.get('dependencies', []):
                if 'index' in dependency:
                    index_dependency(dependency, key, indexed_results)
                for attr, entry in val[dependency['table']]['entries'].items():
                    if 'omit' in entry.keys() and entry['omit']:
                        remove_attrs.setdefault(key, []).append(attr)

            if 'omit' in cfg.keys() and cfg['omit']:
                remove_attrs.pop(key, None)
                continue
            remove_attrs.setdefault(key, [])
            for attr, entry in cfg['entries'].items():
                if 'omit' in entry.keys() and entry['omit']:
                    remove_attrs[key].append(attr)

        snmp_facts.update(
            _remove_omitted_attrs(
                remove_attrs,
                indexed_results
            ))

        return snmp_facts

    return {}


def _remove_omitted_attrs(remove_attrs, indexed_results):
    result = {}
    for key, attrs in remove_attrs.items():
        elements = list(indexed_results.get(key, {}).values())
        for element in elements:
            element.pop('_index', None)
            for attr in attrs:
                element.pop(attr, None)
        result[key] = elements

    return result


def get_snmp_template(templates_path, template_name):
    return load_yaml(os.path.join(templates_path, "{0}.yaml".format(template_name)))


def load_yaml(path):
    """
    Load and parse YAML file ``path``.
    """
    with open(path, 'r') as stream:
        return yaml.load(stream, Loader=_SafeLoader)
