# Ansible Collection - datadope.discovery

<!-- TOC -->
* [Ansible Collection - datadope.discovery](#ansible-collection---datadopediscovery)
* [Provided artifacts](#provided-artifacts)
  * [Modules](#modules)
    * [software_facts](#software_facts)
    * [process_facts](#process_facts)
    * [win_process_facts](#win_process_facts)
    * [win_package_facts](#win_package_facts)
    * [sunos_listen_ports_facts](#sunos_listen_ports_facts)
    * [file_parser](#file_parser)
    * [check_connection](#check_connection)
  * [Roles](#roles)
    * [software_discovery](#software_discovery)
    * [docker_containers](#docker_containers)
  * [Playbooks](#playbooks)
    * [software_discovery.yml](#software_discoveryyml)
  * [Other artifacts](#other-artifacts)
* [Software Discovery procedure](#software-discovery-procedure)
  * [Supported software types](#supported-software-types)
* [License](#license)
* [Author Information](#author-information)
* [Contribution](#contribution)
<!-- TOC -->

The main goal of this collection is to provide the tools to discover the software that is running on the target hosts.

This is achieved using software_facts ansible module (actually, it is an ansible action as it is executed in the 
ansible controller). A role and a playbook are also provided so users of these collection may use them out-of-the-box.

Some additional modules and roles are provided as they are needed to run the software discovery.

Additional documentation for this collection is available in the [docs](docs) folder.

# Provided artifacts

## Modules

### software_facts

The main module in the collection. This module is in charge of discovering the software running in the target hosts
among a set of supported software types. 

As pointed before, the execution of this module is done in the controller so, it is actually an ansible action. This is
possible because all the information needed to discover the software is provided to this module as input arguments. 
Being an action implies that the module definition is located in a python .py file located in the collection modules dir.
while actual action implementation is located in action dir.

The information needed for these arguments is collected using other ansible modules, most of them are modules available
in the ansible community. Some of them weren't available and have been implemented in this collection.

Although the main process of this module is run in the controller, as previously said, one of this module feature
is the ability to execute custom operations to enrich the information discovered for the software instance. Some of 
these operations could be executed in the target hosts.

More details in [Software Discovery procedure](#software-discovery-procedure).

See [definition](plugins/modules/software_facts.py), [implementation](plugins/action/software_facts.py) and 
[doc](docs/modules/software_facts.md).

### process_facts

This module gets the list of processes that are being executed in the target hosts.

**Supported platforms**
- Linux
- HP-UX
- AIX
- Solaris

See [implementation](plugins/modules/process_facts.py) and [doc](docs/modules/software_facts.md).

### win_process_facts

This module provides the same information as [process_facts](#process_facts), but it supports Windows target hosts.


Windows modules are implemented using PowerShell. But module definition must be provided in a python file.

See [definition](plugins/modules/win_package_facts.py), [implementation](plugins/modules/win_package_facts.ps1) and 
[doc](docs/modules/win_package_facts.md).

### win_package_facts

This module provides the packages installed in the target hosts. 
It returns the same information as ansible's core module
[ansible.builtin.package_facts][ansible.builtin.package_facts], but it supports Windows target hosts.

Windows modules are implemented using PowerShell. But module definition must be provided in a python file.

See [definition](plugins/modules/win_process_facts.py), [implementation](plugins/modules/win_process_facts.ps1) and 
[doc](docs/modules/win_process_facts.md).

### sunos_listen_ports_facts

This module gather facts on processes listening on TCP and UDP ports.
It returns the same information as ansible's community general
[community.general.listen_ports_facts][community.general.listen_ports_facts], 
but it supports Solaris (SunOS)target hosts.

See [implementation](plugins/modules/sunos_listen_ports_facts.py) and 
[doc](docs/modules/sunos_listen_ports_facts.md).

### file_parser

This module provides tools to parse different types of configuration files.

**Supported software configuration files types**
- Apache Webserver
- HAProxy
- Keepalived
- nginx

See [implementation](plugins/modules/file_parser.py) and [doc](docs/modules/file_parser.md).

### check_connection

This module tries to establish a connection from the target host to the port of an address 
and check if the connection can be established. 

See [implementation](plugins/modules/check_connection.py) and [doc](docs/modules/check_connection.md).

## Roles

### software_discovery

This role executes all the steps to discover the software running in the target hosts. 
It reads the necessary input data: processes, packages, docker containers,... from the target 
and passes the obtained information to the software_discovery module.

See [implementation](roles/software_discovery) and [doc](docs/roles/software_discovery.md).

### docker_containers

This role is in charge of obtaining the docker containers running in the target host 
(if docker is running in the hosts). This information is an input for the software_discovery module.

This role tries to use modules from ansible's `community.docker` collection to get the data.
But modules of this collection require a python library that is not always installed in the target machine,
so a fallback mechanism has been implemented using ansible `command` module to execute the CLI command `docker`.
Both mechanisms return the same information of the discovered docker containers.

See [implementation](roles/docker_containers) and [doc](docs/roles/docker_containers.md).

## Playbooks

### software_discovery.yml

This playbook is an out-of-the-box playbook to run the software_discovery role and execute discovery
in the target hosts determined by the ansible inventory.

Additionally, it provides the capability to generate output files that may be used as skeletons
to create unit tests to test the discovery of a software type procedure.

See [implementation](playbooks/software_discovery.yml) and [doc](docs/playbooks/software_discovery.md).

## Other artifacts

Filters `path_join` and `split` have been implemented to support versions of ansible before their builtin support. 

# Software Discovery procedure

Providing a command line regex (`cmd_regexp`) to identify the running software instance may be enough 
to support a new software type. 
Although more information would be needed to get more detailed info about the discovered software such as configuration
options, running databases,... Most of this extra information will depend on the type of software so a mechanism for
running customized operations for each software type has been implemented. Field `custom_tasks` is used to get these
operations that will be executed to enrich the information collected for each software instance.

Without custom tasks, some information will be available for every discovered software, such as:
- The main OS process associated to the software instance.
- Port or ports where the software instance is listening.
- If the software instance is running in a docker container, information about that container.
- The package or packages used to install the software (if available).
- Some version info obtained from the docker or the packages.

This information can be enriched with custom information for each software type. The additional information provided for
each software will depend on the software type.

There would be two ways to implement these custom operations:
* Provide a python module implementing SoftwareDiscoveryPlugin that executes these custom operations. 
Only one custom task executing this plugin would be needed.
* Use the provided plugins to create a list of tasks that perform the operations needed to obtain the desired data. 

The latter option is the preferred one as the custom operations are defined in a declarative way, using yaml the same
way as for creating ansible roles. So it will be easy for ansible users to understand and create these custom tasks.

Creating python plugins should be used only when there's no way to implement an operation using current plugins, or 
it will be difficult and the readability of the custom tasks will be affected significantly.

Detailed information about creating custom tasks can be found in [customization.md](docs/customization.md).

## Supported software types

Supported software types must be included in the variable `software_discovery__software_list` at 
`software_discovery` [role default vars](roles/software_discovery/defaults/main.yml) because this is the default
value of this var, and it is the one used by the role or playbook (if not explicitly overridden).

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

# License

GNU General Public License v3.0 or later

See [COPYING](COPYING) to see the full text.

# Author Information

Datadope (@datadope-io)

You can contact Datadope in info@datadope.io.

# Contribution

Please send suggestions or pull requests to make this collection better.

We plan to increase the number of supported software types and platforms, 
but the necessities and priorities are very different, so we will be very happy to receive contributions for new 
software types support, enrich already supported software types, improvements, issues...

You can find more information on how to develop and test this collection 
in [docs/development_environment.md](docs/development_environment.md).

How to implement a new software type and execute custom tasks to provide specific information for a discovered
software instance is deeply explained in [docs/customization.md](docs/customization.md) and how to create tests for
new software types is explained in [docs/creating_auto_test.md](docs/creating_auto_test.md).

See [CONTRIBUTING.md](CONTRIBUTING.md) for more information about contribution guidelines.

Please, contact us if you need more information to submit your contributions.


[ansible.builtin.package_facts]: https://docs.ansible.com/ansible/latest/collections/ansible/builtin/package_facts_module.html
[community.general.listen_ports_facts]: https://docs.ansible.com/ansible/latest/collections/community/general/listen_ports_facts_module.html