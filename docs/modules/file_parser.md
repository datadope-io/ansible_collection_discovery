# file_parser -- Processes the given file with the specified parser.

## Synopsis

Processes the given file using one of the supported parsers, supporting the injection of env vars.

## Parameters

### file_path (True, str, None)
Path of the file to parse.

### parser (True, str, None)
Parser that will handle the parsing of the file.

### env_vars (False, dict, None)
Environment variables that need to be injected into the parser.

### path_prefix (False, str, None)
Prefix that will be appended to every path that the parser will access during its operation.

### strict_vars (False, bool, False)
Determines if the process should fail if a defined environment variable is not available.

## Examples

```yaml
# List running processes
- name: Parse config file
  datadope.discovery.file_parser:
    file_path: "/etc/httpd/conf/httpd.conf"
    parser: "apache_webserver"
```

## Return Values

### parsed (always, dict)
Parsed file.

# License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

# Authors

- Datadope (@datadope-io)
