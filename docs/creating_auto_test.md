# Unit testing software discovery based on files

Every file in [auto/resources](../tests/unit/plugins/action/auto/resources) dir or in any subdir, 
with extension `.json`, `.yaml` or `.yml` will generate a unit test case that will be executed 
when pytest is invoked for unit testing.

The file must represent a dictionary with the following keys:

| Field                              | Type | Meaning                                                                                                   |
|------------------------------------|------|-----------------------------------------------------------------------------------------------------------|
| `software_list`                    | list | Software discovery configuration.                                                                         |
| `expected_result`                  | list | Software instances that should have been discovered using the rest of the input file                      |
| `processes`                        | list | Processes to use to discover the software                                                                 |
| `tcp_listen`                       | list | Listening tcp ports to use to discover the software                                                       |
| `udp_listen`                       | list | Listening udp ports to use to discover the software                                                       |
| `packages`                         | dict | Packages information as returned by ansible `package_facts` module (empty dict if this key doesn't exist) |
| `dockers`                          | dict | Docker information as returned by docker role  (empty dict if this key doesn't exist)                     |
| `task_vars`                        | dict | Variables to pass to the resolver                                                                         |
| `mocked_plugin_tasks`              | dict | Definition of the behavior to implement when that task should be executed                                 |
| `expected_tasks_calls`             | dict | Definition of the expected number of calls per task names to check the correct test behavior              |
| `expected_tasks_calls_mode_strict` | bool | Flag to indicate the way that the previous dict must be processed                                         |

In [Generation of a test file skeleton](#generation-of-a-test-file-skeleton) below, 
a way to obtain a skeleton of these files is explained.

### General notes

For equality assertion of fields in dicts, the values `any`, `*` or `.*` are considered as "any value" so 
fields with one of these values will not provoke an _AssertionError_ despite they will be different from the actual
values. But the field must exist in the actual dictionary, if it doesn't exist an _AssertionError_ will be raised.

For accounting, a task is considered executed if its plugin would be executed after conditions are resolved. 

## Input data

Lists `software_list`, `processes`, `tcp_listen`, `udp_listen` and dictionaries `packages` and `dockers`
correspond to the parameters that software_facts ansible action expects to run. 
Tests will use these objects as arguments for each test execution.

## Expected result

`expected_result` list will be used to compare the result of the discovery process test. The result must be equal
to this list taking into account the "any value" field value described above.


## Task vars

Task vars needed to execute the discovery that ansible would fill in a real scenario should be provided using 
_task_vars_ dictionary.

If not provided in the _task_vars_ dict, a var named `software_discovery__custom_tasks_definition_files_path` is included automatically 
in the dict. Its value will be the path to the _tasks_definitions_ folder in _software_discovery_ role.

## Mocking plugins

Dictionary `mocked_plugin_tasks` defines the behavior of the test 
as being able to replace the normal behavior of a plugin.
Additionally, definitions in this dictionary may check that the behavior of the discovery
is the expected one, raising assertion errors if not.

Each element of this dictionary has as its _key_ the name of a discovery plugin task. 
Its _value_ has to be a dictionary that defines the behavior for that task.

When discovery is configured to run a task with that name, the test intercepts the call to the corresponding
plugin configured in the task performing different actions depending on the definition dictionary.

The different options available for the task mocking definition are the following:

### Related to plugin behavior

The following options replace normal plugin behaviour with an action. Real plugin is not executed.

| Option                  | Type | Meaning                                                                                                                                  |
|-------------------------|------|------------------------------------------------------------------------------------------------------------------------------------------|
| `fail`                  | str  | Test will fail immediately with an _AssertionError_ using the value as the assertion message                                             | 
| `raise_exception`       | str  | Plugin will raise an _AnsibleRuntimeException_ using the value as _message_                                                              |
| `plugin_result`         | any  | Plugin will return the value of this key instead of actually performing its real function                                                |
| `execute_module_result` | any  | Real plugin is executed but, if it calls `execute_module`, the call will return the value of this key without actually call the function |
| `sleep`                 | int  | Sleep the provided time before continuing.                                                                                               |

`sleep` could be used combined with the other options that will be executed after waiting the provided seconds.

If more of one of the other options is present in the mocking task definition, 
the priority is `fail`, `raise_exception` and `plugin_result`, `execute_module_result`. 

If none of the options is present, real plugin will be executed normally.

Tasks associated to _block_ and _include_tasks_ plugins are not affected for these options.

### Related to checking that plugin behaves as expected

| Option                | Type | Meaning                                                                                                                                                         |
|-----------------------|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `expected_args`       | dict | Expected arguments to receive when calling the plugin                                                                                                           |
| `expected_attributes` | dict | Expected attributes to receive when calling the plugin                                                                                                          |
| `expected_result`     | dict | Expected result when calling the real plugin                                                                                                                    |
| `expected_exception`  | dict | Fails is plugin execution don't raise and exception or its type or message are different to the provided `type` and `message` values. These fields are optional |
| `check_instance_vars` | dict | Checks if the provided vars exist and have the same values as in the stored instance object after executing the plugin.                                         |

If _plugin_result_ is provided, _expected_result_, _expected_exception_ and _check_instance_vars_ are ignored.

If _message_ is provided in _expected_exception_ the test will check if that message is part of the exception message.
It is not necessary to provide the whole exception message.

Tasks associated to _block_ and _include_tasks_ plugins are not affected by these options.

**If a plugin raises an exception even if _ignore_errors_ is defined for the task, _expected_exception_ must be
explicitly defined for that task (or for the specific task call number). If not defined, an _AssertError_ will be
raised and the test will fail. This is done to avoid unexpected behaviors hidden by an _ignore_errors_ attribute.**

### Related to task call count and behavior

Previous options included directly in the task mocking definition dict are executed the same way every time a task with
that name is executed.

With the following options it is possible to check that the number of calls to a task with the same name is the expected
one, but also to provide different behavior for each time a task with the same name is invoked.

A task with the same name will be executed more than once if the task is inside a loop 
but also if the name is repeated along the plugins definition.

| Option            | Type | Meaning                                                                                                                                                            |
|-------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `number_of_calls` | int  | At the end of the discovery procedure the times a task with that name is called has to match this number                                                           |
| `call`            | list | Each element of the list is a dict that may have any of the options described in previous sections and will be used for the corresponding call number to the task  |

If _call_ is present, options provided as the first level of task definition are ignored 
and the plugin behavior and checks are defined with the corresponding call index object of the _call_ list.

If _call_ is present, the number of elements of the list must correspond to the times a task with that name is called.
If the task is called more or fewer times than elements, an _AssertionError_ is raised.

If both _call_ and _number_of_calls_ are present, the length of _call_ must be the same as _number_of_calls_ or an
_AssertionError_ will be raised.

A call element can be defined as the string `run` to indicate that nothing special should be done (it is the same as
providing an empty dict).

## Checks expected tasks execution

Apart from using _number_of_calls_ and _call_ list length to check the tasks are executed as expected, a global
field `expected_tasks_calls` may be provided with a dictionary being its keys the task names, and the values the
number of times a task with that name is executed ("any value" characters may be used as described before. A
`0` value will ignore the task too).

The comparison between this provided dictionary and the real one is decided using `expected_tasks_calls_mode_strict`
global test file field.

If this key doesn't exist or its value is false only the task names included in the 
_expected_tasks_calls_ dictionary are taken into account. An _AssertionError_ will be raised only if a task name 
present in this dictionary was actually executed a different number of times. It will raise an _AssertionError_ also if
there is some task in this dictionary that wasn't actually executed.

If _expected_tasks_calls_mode_strict_ is _true_, a strict comparison will be performed taking into account all the
tasks that were actually executed. So, if a task with a name that is not provided in _expected_tasks_calls_ dictionary 
was executed, an _AssertionError_ will be raised too.

# Generation of a test file skeleton

A test file skeleton may be created using the provided [software_discovery playbook](../playbooks/software_discovery.yml).

If this playbook is executed with the variable `software_discovery__copy_input_data` set to `True`, 
a file is generated for every target host including the processes, packages, dockers, ... read from the hosts. 
The result of the software discovery is included in the file too, as `expected_result`. This file can be used to prepare
an auto test, adding mocking of tasks, vars, ... as explained before. 

This is an example of a playbook invocation to get this test file skeleton:

```bash
ansible-playbook -i "host1,host2" datadope.discovery.software_discovery --become \
-e '{"software_discovery__copy_input_data":true}' \
-e "software_discovery__copy_input_data_file_format=yaml"
```

That example will generate two files: `host1_input_data.yaml` and `host2_input_data.yaml` in default dir `/var/tmp` in
the ansible controller.

The name and location of generated files may be modified using the playbook variables. 
See the [playbook readme file](../playbooks/README.md) to see the available vars.

**IMPORTANT NOTE**: Please obfuscate any password or private information that may be present in the data gathered from
the target hosts. In process and docker data environment variables with this kind of information may be read from the 
host and stored in the skeleton files.
