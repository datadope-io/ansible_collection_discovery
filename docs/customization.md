# Customization of the information provided for a software type

<!-- TOC -->
* [Customization of the information provided for a software type](#customization-of-the-information-provided-for-a-software-type)
  * [Custom task definition](#custom-task-definition)
  * [Usage of variables](#usage-of-variables)
  * [Supported attributes](#supported-attributes)
    * [loop](#loop)
    * [loop_control](#loop_control)
    * [when](#when)
    * [timeout](#timeout)
    * [ignore_errors](#ignore_errors)
    * [register](#register)
    * [environment](#environment)
    * [vars](#vars)
  * [Builtin plugins](#builtin-plugins)
    * [include_tasks](#include_tasks)
    * [block](#block)
    * [add_binding_info](#add_binding_info)
    * [add_endpoint_info](#add_endpoint_info)
    * [add_file_info](#add_file_info)
    * [add_message_info](#add_message_info)
    * [add_version_info](#add_version_info)
    * [del_instance_fact](#del_instance_fact)
    * [find_containers](#find_containers)
    * [find_elements](#find_elements)
    * [find_in_dict](#find_in_dict)
    * [find_packages](#find_packages)
    * [find_ports](#find_ports)
    * [find_processes](#find_processes)
    * [parse](#parse)
    * [print_var](#print_var)
    * [read_environment_for_process](#read_environment_for_process)
    * [read_remote_file](#read_remote_file)
    * [run_command](#run_command)
    * [run_module](#run_module)
    * [set_instance_fact](#set_instance_fact)
    * [stat](#stat)
    * [update_instance_fact](#update_instance_fact)
    * [which](#which)
  * [Develop new plugins](#develop-new-plugins)
<!-- TOC -->

_software_facts_ ansible module available in `datadope.discovery` ansible collection performs a software discovery
in the target hosts, being able to discover several software types. This module receives a parameter, **software_list**,
with the definition of the kind of software that the module should try to discover.

With a basic definition of a software, some common features from every software can be discovered,
such as the process that is running the software, its command line or the ports that the software is publishing.
But there are other features of a software whose discovery will depend on the type of software.

The _software_facts_ module provides a mechanism to discover these custom features that depend on the software type.

This mechanism is based on the software definition parameter **custom_tasks** that may be provided as part of the
software definition dictionary for every software in the _software_list_ module parameter. See
[software_facts module documentation][software_facts_module_doc].

## Custom task definition

_custom_tasks_ parameter consists of a list of dictionaries.
Each dictionary defines an operation to perform over the information discovered for the specific software.
It has a definition similar to an ansible task definition, with three components:

* **name**: the name of the task to provide information to the reader. It's an optional parameter.
* **the operation to perform**: this part consists of the name of a provided software discovery "plugin" with its arguments.
* **attributes**: modifiers to the operation

For example:
```yaml
    name: Save a variable
    set_instance_fact:
       var1: "{{ value }}"
    when: value > 0
```

In this example "Save a variable" is the name of the task that will execute the operation.
The operation to be performed consists of a "set_instance_fact" plugin with the provided dict of arguments:
`{"var1": "{{ value}}"}`, and the task will be executed only if the value is greater than 0 thanks to the "_when_" attribute.

The available operations like "_set_instance_fact_" are named "software discover plugins"
and the software_facts module provides a set of plugins that can be used to enrich the information to return as part
of the discovered software.

Task format is based on ansible and all ansible tools to manage variables, such as filters, lookups…,
can be used in these tasks.

With the _custom_tasks_ software definition parameter, a list of tasks to execute can be provided for each type of defined
software. But a list of tasks to execute for every type of software before or after executing these custom tasks may
also be provided. This is done using _software_facts_ module arguments **pre_tasks** and **post_tasks** respectively.
Both arguments are a list of tasks that will be executed independently of the software type. See
[software_facts module documentation][software_facts_module_doc].

So, for a software type, the full discovery procedure will be:

* Get the common information for all software types
* Execute tasks defined in **pre_tasks** _software_facts_ argument on every discovered software.
* Execute tasks defined in **custom_tasks** for each specific software type definition in the _software_list_ module argument.
* Execute tasks defined in **post_tasks** _software_facts_ argument on every discovered software.

## Usage of variables

A special variable can be used: `__instance__`. This variable contains the discovered software current information,
and it is the variable where to insert new information to return as the software discovery result.

The processing of these tasks is made during ansible _software_facts_ module execution.
But variables referenced with ansible jinja2 format: "{{ var }}" will be replaced with its value just
before the processing of the software_facts module starts.
This means that variables calculated during software_facts processing, like `__instance__`, can not be accessed using
`{{ __instance__ }}` as this variable doesn't exist when the software_facts module starts processing.

To delay the instant a variable has to be replaced with its value, to the instant these software discovery tasks are
processed, variables must be enclosed between "<<" and ">>". For example: `<< __instance__ >>`.
This way, the variable is replaced at the moment that the task is going to be executed, ensuring it is defined.

## Supported attributes

As referred before, a task may have one or more attributes that define the way the task plugin is executed.
The supported attributes are a subset of the attributes that ansible permits in ansible tasks.
The way of working of each attribute is intended to be the same as the corresponding ansible task attributes.

The supported attributes are:

### loop

Used to iterate through a list of values. It must contain a list (or an expression that resolves to a list).
The plugin defined in the tasks is executed as many times as values in the list.
Each value of the list is provided to the task execution as a var with a default name of `__item__`,
although that name is configurable using the following attribute **loop_control**.

### loop_control

It is a dict and, used together with the loop attribute, allows defining the name of the variable that stores
the value of the loop element for the current iteration. The default name for this variable is `__item__`.
To change this default value a key "**loop_var**" with the desired variable name as value must be provided in this dict.

Apart from the variable that stores the loop list element value for the iteration, a variable with the index of the
iteration can also be provided to the task if a key "**index_var**" is provided in this dict
(no value with the iteration index is provided if this index_var key is not provided).

---
**NOTE**

It is important to point out that the rest of the available attributes are calculated for each of the iterations of a loop.
This way, for example, a "_when_" attribute may use the __item__ variable with the loop iteration value to check if the
plugin must be executed or not. It may be executed for some loop iterations and not for others.
---

### when

A conditional statement. It may be a string with an expression that evaluates to true or false,
or a list or expressions. In case of using a list, all expressions in the list must be true to consider that the overall
expression is true (equivalent to an "AND" of all list expressions).
To specify an OR condition, it must be done inline using the "OR" operator.

In case of the "when" expression evaluates to true the plugin defined in the task is executed.
Otherwise, it is not executed.

The expressions are evaluated using jinja2 evaluation so variables, filters, lookups, … may be used.

It's important to point out that the expression or the list of expressions are considered jinja2 expressions so must
not be enclosed in "{{ }}" or "<< >>", string values must use quotes, etc…

### timeout

Specifies the maximum time (in seconds) for the action to be performed generating an error in case the time reaches
that timeout.

### ignore_errors

Used to specify if the possible errors that certain actions could cause will be ignored (value `True`)
or not (value `False`).

This statement is often used when we want to continue through a group of tasks or a loop even
when something has gone wrong in one of the iterations.

### register

Creates a variable that stores the output of a given plugin. The value of this attribute will be the name of the
variable.

This variable is defined when executing the task and will be available during the execution of all the
remaining tasks related to the software instance that is being processed, but will no longer be available for tasks
related to the processing of the remaining software instances.

The value stored in the generated variable will depend on the executed plugin.

### environment

This attribute is a dictionary with keys and values that will be provided to the plugin in the form of environment vars.
So, when the plugin is executed it will be executed with these environment variables as part of its environment.

### vars
Dictionary with additional variables and their values to provide to the plugin when it is executed or to resolve
expressions used in the plugin arguments.

These vars will only be available during the specific task execution.

## Builtin plugins

As seen previously in this guide, we can make use of certain plugins in order to enrich the software discovery process.

This collection provides a set of built-in plugins, located in [plugins/action_utils/software_facts/plugins/][plugins]
collection folder:

### include_tasks

This plugin executes the list of tasks available in an external file. This allows the organization of the tasks
in different files and adds readability to the `software_list` variable.

**Arguments**

| key  | type | M/O | Description                                   |
|------|------|-----|-----------------------------------------------|
| file | path | M   | Path to the file containing the list of tasks |


For example, a file for each type of software may be available with its customization tasks.
Then, the _custom_task_ field of its definition in _software_list_ will only contain a task with this plugin,
pointing to the precise file. This limits the size of the software_list variable.
And this is the way that the built-in software types definitions are provided.

**Example**

In the following example, the definition of "Apache ActiveMQ" is provided, and it will use the tasks in the provided
file to enrich the information gathered for this type of software.

```yaml
  - name: Apache ActiveMQ
    cmd_regexp: activemq\.ja
    pkg_regexp: activemq
    process_type: parent
    return_children: false
    return_packages: true
    plugins:
      - name: Include Apache ActiveMQ specific plugins
        include_plugins:
          file: "{{ software_discovery__custom_tasks_definition_files_path }}/apache_activemq.yaml"

```

**Note**
`software_discovery__custom_tasks_definition_files_path` var may be used to point to the path where builtin customization files are located:
`roles/software_discovery/files/tasks_definitions`.

### block

This plugin is used to group actions, such as multiple tasks that must be accomplished following a certain
order or for code readability.

**Arguments**

| key | type | M/O | Description                         |
|-----|------|-----|-------------------------------------|
| -   | list | M   | List of tasks to execute as a block |

**Example**

```yaml
- name: Save multiple vars
  block:
    - name: Save first variable
      set_instance_fact:
        var1: value1
    - name: Save second variable
      set_instance_fact:
        var2: value2
  when: __instance__.var3 is defined
```

In this example, two vars: `var1` and `var2` will be added to the software instance result but only if instance
var `var3` is defined. Using this block plugin group two tasks that has the same condition to be executed.

Without using block, the same could be achieved with:

```yaml
- name: Save first variable
  set_instance_fact:
    var1: value1
  when: __instance__.var3 is defined
- name: Save second variable
  set_instance_fact:
    var2: value2
  when: __instance__.var3 is defined
```

### add_binding_info

Adds information about a binding related to the discovered software in the `bindings` field of the software instance.

**Arguments**

| key        | type | M/O | Description                                |
|------------|------|-----|--------------------------------------------|
| address    | str  | O   | Address of the binding                     |
| port       | int  | O   | Port of the binding                        |
| protocol   | str  | O   | Protocol of the binding                    |
| class      | str  | O   | Class of the binding. Default: `service`   |
| extra_data | dict | O   | Additional information as a key/value dict |

At least one of `address` or `port` must be provided.

**Example**

```yaml
- name: Add binding
  add_binding_info:
    address: 127.0.0.1
    port: 80
    protocol: https
    class: service
    extra_data:
        certificate: true
```

### add_endpoint_info

Adds information about an endpoint related to the discovered software in the `endpoints` field of the software instance.

**Arguments**

| key        | type | M/O | Description                                |
|------------|------|-----|--------------------------------------------|
| uri        | str  | M   | URI of the endpoint                        |
| type       | str  | O   | Endpoint type. Default: `generic`          |
| extra_data | dict | O   | Additional information as a key/value dict |

**Example**

```yaml
- name: Add endpoint
  add_endpoint_info:
    uri: https://127.0.0.1:3360
    type: generic
```

### add_file_info

Adds information about a file/dir related to the discovered software in the `files` field of the software instance.

**Arguments**

| key        | type | M/O | Description                                |
|------------|------|-----|--------------------------------------------|
| path       | str  | M   | Path (dir) of the file                     |
| name       | str  | O   | Name of the file if available              |
| type       | str  | M   | Identification on the file entry           |
| subtype    | str  | O   | Additional identification of the entry     |
| extra_data | dict | O   | Additional information as a key/value dict |


**Example**

```yaml
- name: Add file info
  add_file_info:
    path: /etc/nginx
    name: nginx.conf
    type: config
    subtype: generic
    extra_data:
        raw: True
```

### add_message_info

Adds a message to provide to the client. It also allows to set a variable, so it can be used for any processing purpose.

**Arguments**

| key        | type | M/O | Description                                |
|------------|------|-----|--------------------------------------------|
| msg        | str  | M   | Message to store                           |
| key        | str  | O   | Name of a key to set                       |
| value      | any  | O   | Value to set for the key                   |
| extra_data | dict | O   | Additional information as a key/value dict |

**Example**

```yaml
- name: Add message from server
  add_message_info:
    msg: "Generic msg from server"
    key: can_connect
    value: true
```

### add_version_info

Adds the given information to the `version` list field of the software instance.

**Arguments**

| key            | type | M/O | Description                                                               |
|----------------|------|-----|---------------------------------------------------------------------------|
| version_type   | str  | M   | Identifier of the way the version was discovered, as `file`, `command`... |
| version_number | str  | M   | Version string                                                            |


**Example**

```yaml
- name: Add version from package
  add_version_info:
    version_type: package
    version_number: 2.0.3
```

### del_instance_fact

Deletes a specified list of variables from the instance given their names.

**Arguments**

| key | type | M/O | Description                                           |
|-----|------|-----|-------------------------------------------------------|
| -   | list | M   | List of names of the vars to delete from the instance |

**Example**

```yaml
- name: Remove temporary vars
  del_instance_fact:
    - var_temporary_1
    - var_temporary_2
```

### find_containers

This plugin searches for containers given a filter from the list of docker containers found in the target hosts.

Filtering is made using [find_elements](#find_elements).
Docker containers list is provided to this plugin as the source.

**Arguments**

| key     | type | M/O | Description                        |
|---------|------|-----|------------------------------------|
| filter  | dict | O   | Dict containing the filtering info |

**Example**

```yaml
- name: Find containers
  find_containers:
    filter:
      container_name: ^cont*
  register: result
```

### find_elements

This plugin searches for elements that match the specified values inside a given collection.

`filter` argument is a key/value dict. An element in `source` match the filter if it has all the keys in filter
and those keys values match filter values, taking into account tha those filter values are considered regular
expressions.

**Arguments**

| key    | type | M/O | Description                                                                          |
|--------|------|-----|--------------------------------------------------------------------------------------|
| source | list | M   | List of element to filter                                                            |
| filter | dict | O   | Dict containing the filtering info. Default '{}' => all source elements match filter |

**Example**

```yaml
- name: Find in elements
  find_elements:
    source: list_dict
    filter:
      value: var1
  register: result
```

### find_in_dict

This plugin returns the list of values in the provided dict whose key is the provided item,
processing the source dict recursively.

**Arguments**

| key    | type | M/O | Description                     |
|--------|------|-----|---------------------------------|
| source | dict | M   | Source dict where to find items |
| item   | str  | M   | Name of the key to look for     |

**Example**

```yaml
- name: Find in dict
  find_in_dict:
    item: key3
    source:
      key1: value1
      key2: value2
      key3: value3
      other:
        key3: inner
  register: result  # result will store the list: ['value3', 'inner'].
```

### find_packages

This plugin searches for packages that match a given a filter from the list of packages found in the target host.

Filtering is made using [find_elements](#find_elements).
The packages list is provided to this plugin as the source.

**Arguments**

| key     | type | M/O | Description                        |
|---------|------|-----|------------------------------------|
| filter  | dict | O   | Dict containing the filtering info |

**Example**

```yaml
- name: Find package
  find_packages:
    filter:
      name: "test"
  register: result
```

### find_ports

This plugin searches for ports that match a given a filter from the lists of tcp ports and udp ports found in the target host.

Filtering is made using [find_elements](#find_elements).
The port lists are provided to this plugin as the source.

**Arguments**

| key     | type | M/O | Description                        |
|---------|------|-----|------------------------------------|
| filter  | dict | O   | Dict containing the filtering info |

**Example**

```yaml
- name: Find ports
  find_ports:
    filter:
      protocol: "udp"
      port: "3[0-9]{3}1"
  register: result
```

### find_processes

This plugin searches for processes that match a given a filter from the list of processes found in the target host.

Filtering is made using [find_elements](#find_elements).
The processes list is provided to this plugin as the source.

**Arguments**

| key     | type | M/O | Description                        |
|---------|------|-----|------------------------------------|
| filter  | dict | O   | Dict containing the filtering info |

**Example**

```yaml
- name: Search process
  find_processes:
    filter:
      cmdline: "regex_cmdline"
  register: result
```

### parse

Provides a JSON representation of the content, given a parser type.

**Arguments**

| key           | type | M/O | Description                            |
|---------------|------|-----|----------------------------------------|
| content       | str  | M   | Content to parse                       |
| parser        | str  | M   | Type of parser to apply to the content |
| parser_params | dict | O   | Parameters to provide to the parser    |

Several parsers are available:
* `json`: Expects content to be a json string.
* `yaml`: Expects content to be a YAML string.
* `xml`: Expects content to be in XML.
* `ini`: Expects content to be in INI format. If there are values without section, they will be added to the "default" section.
* `key_value`: Expects content to be in a key/value format. The key and value separator may be defined using a parser parameter (defaults to `=`).
* `environ`: Expects content to be an environ file in proc linux filesystem.
* `custom`: An ansible module must be specified to parse the content. In this case, the content is expected to be a file path.

Built-in parsers implementations are located in [plugins/action_utils/software_facts/parsers][parsers].

**Example**

```yaml
- name: Parse json string
  parse:
    content: '{"key1": "value1", "key2", "value2"}'
    parser: "json"
  register: json_data
```

### print_var

Displays the value of the provided var in the ansible command output console.

**Arguments**

| key | type | M/O | Description                |
|-----|------|-----|----------------------------|
| var | str  | M   | Name of the var to display |

**Example**

```yaml
- name: Print a var
  print_var:
    var: json_data
```

### read_environment_for_process

Reads the environment vars attached to a process. The process is defined using its pid.

This plugin reads the environ file in `proc` filesystem and then parses the file contents.
Additionally, if the software instance is running in a docker container, proc file info (if available) is merged with
docker environment info (from docker container `Config.Env` data).

Its returns the content of the file before parsing (in `content` return value)
and the parsed file as a JSON (in `parsed` return value).

**Arguments**

| key | type | M/O | Description        |
|-----|------|-----|--------------------|
| pid | str  | M   | Pid of the process |


**Example**

```yaml
- name: Read process environment
  read_environment_for_process:
    pid: << __instance__.process.pid >>
  register: env_vars
```

### read_remote_file

Reads a file from the target host. A parser may be defined to be applied to the content of the file. In this case,
the content of the file is provided to the [parse plugin](#parse).

This plugin manages if the software instance is running in a docker container. If that is the case, it reads the
file from the container's file system instead of the target host file system (unless `in_docker` argument value is set
to `False`).

**Arguments**

| key                | type | M/O | Description                                                                                                                               |
|--------------------|------|-----|-------------------------------------------------------------------------------------------------------------------------------------------|
| file_path          | str  | M   | Path to the file to read                                                                                                                  |
| parser             | str  | O   | Parser to apply to the file content                                                                                                       |
| parser_params      | dict | O   | Parameters to provide to the parser                                                                                                       |
| in_docker          | bool | O   | If `false`, the file is read from the host file system even if the software instance is running in a docker container                     |
| delegate_reading   | bool | O   | If `true`, this plugin will not read the file. File reading is delegated to the parser which must be a _custom_ parser able to read files |

**Example**

```yaml
- name: Read config file
  read_remote_file:
    file_path: "file_path"
    parser: key_value
    parser_params:
      comment_delimiters:
        - "#"
        - "["
  register: result
```

### run_command

This plugin executes a command on the target host, using ansible's `command` module.
It manages if the software instance is running in a docker container. If that is the case, then it executes the command
in the container.

The command to run may be provided as a string with the full command or with a list of arguments that will form the command.

**Arguments**

| key           | type | M/O | Description                                                                                            |
|---------------|------|-----|--------------------------------------------------------------------------------------------------------|
| cmd           | str  | O   | Full command line to execute                                                                           |
| argv          | list | O   | Command and arguments provided as a list                                                               |
| in_docker     | bool | O   | If `false`, the command is executed in host even if software instance is running in a docker container |

One of `cmd` or `argv`arguments must be provided.

**Example**

```yaml
- name: Run command using cmd
  run_command:
    cmd: "postgres -V"
  register: result

- name: Run command using argv
  run_command:
    argv:
      - postgres
      - "-V"
  register: result
```

### run_module

This plugin executes the provided ansible module.

**Arguments**

| key           | type | M/O | Description                                                                                       |
|---------------|------|-----|---------------------------------------------------------------------------------------------------|
| <module_name> | any  | M   | Module_args                                                                                       |

This module should have only one argument which key will be the module name. The value of that key will be the arguments
to pass to the module.

**Example**

```yaml
- name: Check http or https
  run_module:
    check_connection:
      address: 127.0.0.1
      port: 3356
  register: response

- name: Request information from endpoint
  run_module:
    uri:
      url: 127.0.0.1
      method: "GET"
      body_format: "json"
      body:
        operation: "read-resource"
  register: response
```

### set_instance_fact

Stores variables in the software instance return data.

**Arguments**

| key         | type | M/O | Description                                                           |
|-------------|------|-----|-----------------------------------------------------------------------|
| <key_value> | dict | M   | Keys of the dict will be the names of the variables to set the values |

**Example**

```yaml
    - name: Store variables in instance
      set_instance_fact:
        name_var1: value1
        name_var2: value2
        name_var3: value3
```

### stat

Executes module `ansible.builtin.stat` (or `ansible.windows.win_stat` for Windows targets) on the provided path.
If the software instance is running in a docker container, the path is adapted to point to the file in the docker
container file system.

See [ansible.builtin.stat][ansible.builtin.stat] or [ansible.windows.win_stat][ansible.windows.win_stat] documentation
for detailed information.

**Arguments**

| key            | type | M/O | Description                                                                                          |
|----------------|------|-----|------------------------------------------------------------------------------------------------------|
| path           | str  | M   | Path of the file/dir to process                                                                      |
| follow         | bool | O   | Whether to follow symlinks (default False)                                                           |
| get_mime       | bool | O   | Use file magic and return data about the nature of the file (default True)                           |
| get_attributes | bool | O   | Get file attributes using lsattr tool if present (default True)                                      |
| in_docker      | bool | O   | If `false`, stat is executed in host file even if software instance is running in a docker container |

`get_mime` and `get_attributes` are not used and will be ignored in Windows target hosts.
**Example**

```yaml
- name: Check config file
  stat:
    path: "/etc/nginx/nginx.conf"
  register: conf_file_stat
```

### update_instance_fact

Updates software instance facts. With these plugins, complex modifications in the software facts are easier to achieve
than using [set_instance_fact](#set_instance_fact) module.

**Arguments**

| key     | type | M/O | Description                                                                                                                        |
|---------|------|-----|------------------------------------------------------------------------------------------------------------------------------------|
| updates | list | M   | Each list element will be a dict with a `path` element referring to the key to modify, and a `value` element with the modification |

**Example**

```yaml
- name: put notification_email_from
  update_instance_fact:
    updates:
      - path: configuration.global_defs.notification_email_from
        value: <<__instance__._notification_email_from>>
```

### which

Returns the file info if the file exists in the provided paths.
If the software instance is running in a docker container, provided paths are adapted to point to the file system
in the docker container.

**Arguments**

| key                      | type | M/O | Description                                                                                                                              |
|--------------------------|------|-----|------------------------------------------------------------------------------------------------------------------------------------------|
| name                     | str  | M   | Name of the file to look for                                                                                                             |
| paths                    | list | M   | List of paths of directories to search. All paths must be fully qualified                                                                |
| hidden                   | bool | O   | If `true`, hidden files will be included (default False)                                                                                 |
| windows_valid_extensions | list | O   | Valid extensions to consider a file as an executable (default '.bat', '.bin', '.cmd', '.com', '.exe', '.ps1') (Only for Windows targets) |
| in_docker                | bool | O   | If `false`, which is executed in the host file system even if the software instance is running in a docker container                     |


**Example**

```yaml
- name: Run which
  which:
    name: file_name
    paths:
     - /etc
     - /var/etc
  register: result
```

## Develop new plugins

New plugins may be developed to provide functionalities not available with the built-in plugins and tools.

To develop a new plugin, a python class has to be implemented, and it must be a subclass of
[SoftwareFactsPlugin class][SoftwareFactsPlugin].

```python
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__  \
    import SoftwareFactsPlugin

class MyPlugin(SoftwareFactsPlugin):

    @classmethod
    def get_args_spec(cls):
        return {}

    def run(self, args=None, attributes=None, software_instance=None):
        return None
```

Custom plugins python files should be located by default in [plugins/action_utils.software_facts.plugins](../plugins/action_utils/software_facts/plugins)
or a subdirectory. But also may be located in any accessible path if this path is set in the environment
var: `SOFTWARE_DISCOVERY_EXTRA_PLUGINS_PATH`. This var expects a list of paths separated by `:`.


[software_facts_module_doc]: modules/software_facts.md
[SoftwareFactsPlugin]: ../plugins/action_utils/software_facts/plugins/__init__.py
[plugins]: ../plugins/action_utils/software_facts/plugins
[parsers]: ../plugins/action_utils/software_facts/parsers
[ansible.builtin.stat]: https://docs.ansible.com/ansible/latest/collections/ansible/builtin/stat_module.html
[ansible.windows.win_stat]: https://docs.ansible.com/ansible/latest/collections/ansible/windows/win_stat_module.html
