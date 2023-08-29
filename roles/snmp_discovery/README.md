# datadope.discovery.snmp_discovery

This role executes a SNMP discovery in every target host. It will try to discover the device using the IP and UDP port through 
the SNMP protocol and provide valuable information about the network devices.

The type of information that will be discovered is defined by a template that requests the defined scalar and tabular objects.

Two files are provided as databases associated with their corresponding variables. The `SysobjectIDs file` is used to identify 
the brand and model through a unique identifier (sysObjectId OID) and associate different defined templates. If we cannot categorize 
the device, we will use the `Enterprise-numbers file` to identify the company associated with the device.

The resulting information is provided as an ansible fact with key `snmp` containing a dict with device information.

## Requirements

The following collections are required:
- community.general

## Role Variables

###  Role vars
* `snmp_discovery__sysobject_files_path`: (string) Path where the files required for the role are located.
* `snmp_discovery__sysobject_ids`: (string) Path where the SysObjectsIDs file are located.
* `snmp_discovery__enterprise_numbers`: (string) Path where the Enterprise numbers file are located.
* `snmp_discovery__templates_path`: (string) Path where the template files are located.

### Role defaults
* `snmp_discovery__host`: (string) Host on which to perform SNMP Facts.
* `snmp_discovery__version`: (string) Version for SNMP.
* `snmp_discovery__community`: (string) Community for SNMP v2c.
* `snmp_discovery__port`: (int) Port for SNMP Facts.
* `snmp_discovery__timeout`: (int) Timeout for SNMP Facts.
* `snmp_discovery__retries`: (float) Number of retries for SNMP Facts.


## Example Playbook

```yaml
- hosts: servers
  roles:
     - role: datadope.discovery.snmp_discovery
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
