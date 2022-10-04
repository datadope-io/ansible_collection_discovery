# datadope.discovery.software_discovery

This role executes a software discovery in every target host. It will try to discover the software running in the 
host machine and provide valuable information of every discovered software. 

The types of software that this role is going to try to discover are defined in the variable `software_discovery__software_list`, and
refined with `software_discovery__include_software` and `software_discovery__exclude_software` variables.

The resulting information is provided as an ansible fact with key `software` containing a list of dictionaries with
each discovered software information.

## Requirements

The following collections are required:
- community.general
- community.windows for windows target hosts

## Role Variables

###  Role vars
* `software_discovery__custom_tasks_definition_files_path`: (string) Path where the definition of tasks to perform on each type of software is located

### Role defaults
* `software_discovery__include_software`: (list) List of types of software to be discovered from the global list defined in `software_discovery__software_list` variable.
Each element of the list must much the `name` field of the `software_discovery__software_list`element to include.
Use `all` to use the whole list.
* `software_discovery__exclude_software`: (list) List of types of software to exclude from being discovered from the global list defined in `software_discovery__software_list` variableEach element of the list must much the `name` field of the `software_discovery__software_list`element to include.
* `software_discovery__pre_tasks`: (list) Definition of tasks to be executed on every discovered software before custom tasks for each software type are executed
* `software_discovery__post_tasks`: (list) Definition of tasks to be executed on every discovered software after custom tasks for each software type are executed
* `software_discovery__software_list`: (list) Definition of the types of software that will be tried to be discovered in the target hosts.


## Example Playbook

```yaml
- hosts: servers
  roles:
     - role: datadope.discovery.software_discovery
```

A playbook is provided in this collection that can be used to invoke this role. 
See [playbook README file](../../playbooks/README.md).

## License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

## Author Information

Please send suggestions or pull requests to make this role better. 
Also let us know if you encounter any issues installing or using this role.

GitHub: https://github.com/datadope-io/ansible_collection_discovery
