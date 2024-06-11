# 1.11.0

## Features

- Improve `HAProxy` software discovery with the new flag `haproxy_ignore_udp`, which 
  ignores UDP bindings and ports.
- New `Jolokia Proxy` software discovery.

## Fixed

- Update `IIS` tests to match the latest `cmdline` changes. 

# 1.10.2

## Fixed

- Avoid unexpected error for oracle instances processing.

# 1.10.1

## Fixed

- Avoid loops when a pid has it's ppid as pid on its child at any depth.

# 1.10.0

## Features

- Improve `Redis` software discovery with TLS support and enhanced information
  gathering.
- Improve `key_value` parser with support for `-` and ` ` in keys.

# 1.9.0

## Features

- New patroni software discovery.

# 1.8.0

## Features

- New php-fpm software discovery.

# 1.7.0

## Features

- Performance improvements in file reading for SNMP Facts.

# 1.6.0

## Features

- Minor changes on the SNMP template: changed the key `serial_numbers` to `entities`.

# 1.5.0

## Features

- New snmp_facts module.
- New snmp_discovery role.

# 1.4.0

## Features

- Include field `cwd` for modules `process_facts` and `win_process_facts`.
- When a relative path is given to plugins `read_remote_file` or `add_file_info`, the
  process `cwd` will be appended to the path to convert it from a relative path to an
  absolute path, avoiding potential errors.
- Strip Ipv6 brackets when present when using plugin `add_binding_info`
- Increase `postgres` commands timeout from `5` seconds to `10` seconds.
- Add `SQL Server` failover cluster detection.
- Improve `Mulesoft` software discovery with specific tasks.
- Improve `MongoDB` software discovery with specific tasks.
- Improve `Redis` software discovery with additional tasks for configuration retrieving.
- Improve `Apache Tomcat` software discovery with enhanced `base` logic and
  more `HTTP/1.1` protocol detection.
- Improve `Apache WebServer` software discovery with mod_status check and enhanced field
  managing.
- Improve `HAProxy` software discovery with additional tasks for configuration
  processing.
- Improve `JBoss Application Server` software discovery by enhancing binding detection
  and finding the software family.
- Improve `Nginx WebServer` ports processing.
- Enhanced cmd regex for `Apache Tomcat` and `Apache WebServer` detection.
- Attributes `class`, `type` and `subtype` refined for:
    - `Apache ActiveMQ`
    - `Apache WebServer`
    - `JBoss Application Server`
    - `Oracle DatabaseServer`
    - `Oracle Listener`

## Fixes

- Handling of empty path for `add_file_info` plugin.
- Malformed regex usage for `Apache Webserver`.
- Role `docker_containers` now is able to handle machines where docker is installed but
  stopped.

# 1.3.1

## Fixes

- Unexpected errors handling for SQL Server and IIS.

# 1.3.0

## Features

- Added support for PostgreSQL Database for Windows OS.
- The `run_command` builtin plugin now supports Windows hosts.

# 1.2.0

## Features

- win_hyperv_facts module now shows hard_drives by default.

## Fixes

- win_process_facts module now uses same field types as process_facts.

# 1.1.1

## Fixes

- Fixed a problem with the system identification when running tasks.

# 1.1.0

## Features

- New win_hyperv_facts module.
- New hyperv_vms role.

# 1.0.2

## Fixes

- Fixed a problem with Oracle Listener ports iteration.
- Fixed a problem with the validation of the module args where depending on the ansible
  version an error could happen.

# 1.0.1

## Fixes

- Fixed a problem with the Apache Webserver regex.

# 1.0.0

Initial version of `datadope.discovery` Ansible collection.

## Collection components

### Modules

- check_connection
- file_parser
- process_facts
- software_facts
- sunos_listen_ports_facts
- win_package_facts
- win_process_facts

### Roles

- docker_containers
- software_discovery

### Playbook

- software_discovery.yml

## Supported software types

- PostgreSQL Database
- Microsoft SQL Server
- IIS
- Apache WebServer
- Redis
- Oracle DatabaseServer
- Oracle Listener
- Oracle Management Agent
- MariaDB DatabaseServer
- MySQL DatabaseServer
- Apache Tomcat Servlet Engine
- Nginx WebServer
- KeepAliveD
- Grafana
- JBoss Application Server
- HAProxy
- Patrol Agent
- Skydive Analyzer
- AWX Task
- AWX Web
- MuleSoft AppServer
- SAP HANA DatabaseServer
- Xymon
- HPE Data Protector
- SAP CCMS
- SAPcontrol
- Zabbix Server
- IOMetrics Visualizer API
- IOMetrics SLAtor
- Dynatrace Server
- ElasticSearch
- InfluxDB
- Logstash
- Memcached
- Telegraf
- Nagios NRPE
- Hobbit
- MongoDB
- chrony ntp service
- Apache ActiveMQ
- Docker
- Panda Security Protection
