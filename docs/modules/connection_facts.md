# connection_facts -- Gather a list of all current connections on a Linux machine

## Synopsis

Provides information of the existing connections, including PID, process name and commandline.

## Examples

```yaml

- name: List existing connections
  datadope.discovery.connection_facts: {}

```

## Return Values

### connections (success, list)
List of dicts with the connections of the Linux machine

# License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

# Authors

- Datadope (@datadope-io)