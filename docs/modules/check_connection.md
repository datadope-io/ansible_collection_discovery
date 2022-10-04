# check_connection -- Checks if a given endpoint is up and, if so, if it has tls enabled.

## Synopsis

Checks if a given endpoint (address + port) is up, trying to connect to it and, if up, 
checks if it has TLS enabled by trying to cause a certificate error while connecting.

## Parameters

### address (True, str, None)
The ip we are trying to connect to.

### port (True, int, None)
The port of the address.

### timeout (False, int, 1)
The time in seconds that the process is going to be waiting for the checking to take place. 
If this checking takes more than the specified timeout, this will result in an error message

## Examples

```yaml
# Check if ports has tls enabled
- name: Check http or https
  datadope.discovery.check_connection:
    address: "127.0.0.1"
    port: 38956
```


## Return Values

### available (always, bool or None)
If the given endpoint is available

### identified_as (always, bool or None)
If the given endpoint has tls enabled or not

# License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

# Authors

- Datadope (@datadope-io)
