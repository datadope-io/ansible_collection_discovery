# Playbook software_discovery.yml

This playbook may be used to run datadope.discovery.software_discovery role provided by this collection.

Invoking this playbook the role is executed, but it is also prepared to store in a file 
the information used to run the role and its result. This file may be used later to prepare a unit test to test
software discovery.

## Playbook variables

These are the variables used by the playbook (see [vars file](./vars/main.yml) for default values). 
To activate the output file generation `software_discovery__copy_input_data` must be set to `true` (default is `false`).

* `software_discovery__copy_input_data`: (bool) If true, the playbook will generate a file as the prototype to generate a test for each processed host.
* `software_discovery__copy_input_data_dest_path`: (string) Generated file location.
* `software_discovery__copy_input_data_file_name`: (string) Generated file name.
* `software_discovery__copy_input_data_file_format`: (string) Format of the generated file (json or yaml)

See [role README file](../roles/software_discovery/README.md) for variables used by the role itself.

## Example 

Discover Redis software in servers host1 and host2, storing the output in yaml files with default paths and names. 

``` shell
ansible-playbook -i "host1,host2" datadope.discovery.software_discovery --become \
-e '{"software_discovery__copy_input_data":true}' \
-e "software_discovery__copy_input_data_file_format=yaml" \
-e '{"software_discovery__include_software":["Redis"]}'
```

## License

GNU General Public License v3.0 or later

See [COPYING](../COPYING) to see the full text.

## Author Information

Please send suggestions or pull requests to make this playbook better. 
Also let us know if you encounter any issues installing or using this playbook.

GitHub: https://github.com/datadope-io/ansible_collection_discovery