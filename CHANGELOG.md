# 1.4.0

## Features
- Include field `cwd` for modules `process_facts` and `win_process_facts`.
- When a relative path is given to plugins `read_remote_file` or `add_file_info`, the process `cwd` will be
  appended to the path to convert it from a relative path to an absolute path, avoiding potential errors.
- Increase `postgres` commands timeout from `5` seconds to `10` seconds.
- Add SQL Server failover cluster detection.
- Improve Mulesoft software discovery with specific tasks.
- Improve MongoDB software discovery with specific tasks.
- Improve Redis software discovery with additional tasks.

## Fixes
- Handling of empty path for `add_file_info` plugin.

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
- Fixed a problem with the validation of the module args where depending on the ansible version an error could happen.

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