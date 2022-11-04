# 1.0.1

## Fixes
- Fixed a problem with the Apache Webserver regex

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