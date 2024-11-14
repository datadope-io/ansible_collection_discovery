# datadope.discovery.connections_discovery

## Requirements

### Windows

It is required to have Powershell 3.0 or newer installed on the machine, as well as enough rights to query the
current processes and connections of the machine.

### Linux 

To gather information about Linux connections, it is necessary to have superuser privileges. This is because the
`connection_facts` module explores the `/proc` directory to query current processes and connections, which requires
elevated permissions.

## Example Playbook

```yaml
- hosts: servers
  roles:
     - role: datadope.discovery.connection_facts
```

## License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

## Author Information

Please send suggestions or pull requests to make this role better. 
Also let us know if you encounter any issues installing or using this role.

GitHub: https://github.com/datadope-io/ansible_collection_discovery

