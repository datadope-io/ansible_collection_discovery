# win_hyperv_facts -- Gather the Hyper-V virtual machines of the machine

## Synopsis

Gather the information of the Hyper-V virtual machines of the machine.

Extended information about the virtual machines can be gathered using a flag.


## Parameters

### date_format (optional, str, %c)
Establishes the format of the date fields gathered.

Applies to the field creation_time

### extended_data (optional, bool, False)
By default, the module gathers: id, name, serial, hostname, network_adapters, path, creation_time, processor_count, memory, min_memory, max_memory, state and hypervisor. By setting this option to true, all the information related to the virtual machine is gathered, extending the module's output.


## Notes

   - The extended_data flag is disabled by default as the gathered information that is collected by default is usually enough to achieve the goal of the module.
   - Due to Hyper-V limitations, hostname of the virtual machines can only be obtained by doing a DNS search with each one of the VM's addresses.

## Examples

```yaml

    - name: Gather Hyper-V facts
      datadope.discovery.win_hyperv_facts:

    - name: Gather full Hyper-V facts
      datadope.discovery.win_hyperv_facts:
        extended_data: true
    
    - name: Gather full Hyper-V facts with only the year within the date fields
      datadope.discovery.win_hyperv_facts:
        extended_data: true
        date_format: '%Y'

```


## Return Values

### virtual_machines (success, list)
List of dicts with the Hyper-V virtual machines of the machine

# License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

# Authors

- Datadope (@datadope-io)
