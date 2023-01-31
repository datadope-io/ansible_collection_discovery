# process_facts -- Add list of running processes to ansible_facts.

## Synopsis

Provides information about the running processes on the target host, including PID, PPID, user and command line.

## Examples

```yaml
# List running processes
- name: List running processes
  datadope.discovery.processes_info: {}
```


## Return Values

### ansible_facts (always, dict)
Facts to add to ansible_facts:

* processes (always, list): List of running processes. Each element will have the following fields:

  * pid (always, str):
        PID of the process.

  * ppid (always, str):
        Parent PID of the process.

  * user (always, str):
        User which is the owner of the process.

  * cmdline (always, str):
        Command line of the process.

  * cwd (always, str):
        Working directory of the process.

# License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

# Authors

- Datadope (@datadope-io)
