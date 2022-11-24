# datadope.discovery.hyperv_vms

This role gets Hyper-V virtual machines in a Windows host if Hyper-V is enabled.

The result is provided as an ansible fact with key `virtual_machines` that will contain a list with the information of
the virtual machines. The information provided for each virtual machine is similar to the information returned by
a `Get-VM` command.

Due to Hyper-V limitations, the only way of obtaining the hostname of a virtual machine is by doing a DNS serch with the
addresses of the virtual machines, which my end in `null` hostname attributes when no result is obtained.

## Requirements

### Powershell

It is required to have Powershell 3.0 or newer installed on the machine, as well as enough rights to query the
information of Hyper-V

### Linux systems

In order to be able to gather the network information of Linux guests, it is necessary to have installed the linux
cloud tools (usually, the package `linux-cloud-tools-virtual`).

For example, you may install this package on debian based system by running:

```shell
sudo apt-get install "linux-cloud-tools-$(uname -r)"
```

## Example Playbook

```yaml
- hosts: servers
  roles:
     - role: datadope.discovery.hyperv_vms
```

## License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

## Author Information

Please send suggestions or pull requests to make this role better. 
Also let us know if you encounter any issues installing or using this role.

GitHub: https://github.com/datadope-io/ansible_collection_discovery

