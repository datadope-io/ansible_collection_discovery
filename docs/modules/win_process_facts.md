# win_process_facts -- Gather the facts of the current processes of the machine

## Synopsis

Gather the information from the running processes of the machine and the user that owns them.

## Parameters

### date_format (optional, str, %c)
Establishes the format of the date fields gathered when the extended_data option is set.

Applies to the following fields: creation_date, install_date and termination_date.

### extended_data (optional, bool, False)
By default, the module gathers: cmdline, cwd, pid, ppid and user. 
By setting this option to true, all the information related to the process is gathered, extending the module's output.


## Notes

   - The extended_data flag is disabled by default as the gathered information that is collected by default is usually enough to achieve the goal of the module.
   - Due to Windows limitations, the field 'cwd' refers to the path of the executable and not the actual path the process is working on for interoperability purposes, since it's not possible to gather de working directory in a stable, standard way.

## Examples

```yaml
    
    - name: Gather processes facts
      datadope.discovery.win_process_facts:

    - name: Gather full processes facts
      datadope.discovery.win_process_facts:
        extended_data: true

    - name: Gather full processes facts with only the year within the date fields
      datadope.discovery.win_process_facts:
        extended_data: true
        date_format: '%Y'

```


## Return Values

### processes (success, list)
List of dicts with the processes of the machine

# License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

# Authors

- Datadope (@datadope-io)
