# sunos_listen_ports_facts -- Gathers the facts of the listening ports of the SunOS machine

## Synopsis

Gathers the information of the TCP and UDP ports of a Solaris (SunOS) machine and the related processes.

## Examples

```yaml
# Gather ports facts
- name: Gather ports facts
  datadope.discovery.sunos_listen_ports_facts: {}
```

## Return Values

### tcp_listen (success, list)
List of dicts with the detected TCP ports

### udp_listen (success, list)
List of dicts with the detected UDP ports

# License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

# Authors

- Datadope (@datadope-io)
