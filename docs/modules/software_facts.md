# software_facts -- Add list of detected software to ansible_facts.

## Synopsis

Provides information about the configured software if it's found in the system.

## Parameters

### software_list (True, list, None)
List of software type configurations to discover. Each element will have the following fields:

* name (True, str, None):
      Name of the software to discover

* process_type (True, str, None):
      Type of process discovery with processes

* return_children (False, bool, False):
      Return children processes if true

* cmd_regexp (True, str, None):
      Regex to apply on processes to detect this software

* pkg_regexp (True, str, None):
      Regex to apply to packages to detect this software

* return_packages (False, bool, False):
      Return list of packages

* custom_tasks (False, list, None):
      Tasks to execute to enrich software returned information

* vars (False, dict, None):
      Variables to provide as task vars to the plugins executed by the provided tasks.

### include_software (False, list, None)
List of software types to include from *software_list*.

Each element will match the *name* field for each element of *software_list* option.

If any element of the list is **all**, this option is omitted or is `null`, all the software types will be included except the ones explicitly indicated in *exclude_software*.

### exclude_software (False, list, None)
List of software types to exclude from *software_list*.

Each element will match the *name* field for each element of *software_list* option.

Software types in this list will never be processed.

### processes (True, list, None)
List of processes running in the host. Each element of the list has to have the fields:

* pid (True, str, None):
      PID of the process.

* ppid (True, str, None):
      Parent PID of the process.

* cmdline (True, str, None):
      Command line of the process.


### tcp_listen (True, list, None)
List of tcp ports listening in the host.

Empty list if no udp port is in listen state.

### udp_listen (True, list, None)
List of udp ports listening in the host.

Empty list if no udp port is in listen state.

### packages (False, dict, None)
Packages installed in the target host as a dict.

Expected package format as module package_facts return.

Returned dict key is the package name, and value is a list of objects with packager info for every package version

### dockers (False, dict, None)
Information of every docker container running on the machine.

Provided information for each docker should be the same as one obtained with a docker inspect command.

### pre_tasks (False, list, None)
List of plugins to execute with every discovered software instance.

These plugins will be executed before specific software type plugins.

### post_tasks (False, list, None)
List of plugins to execute with every discovered software instance.

These plugins will be executed after specific software type plugins.


## Examples

```yaml
# List running software
- name: List running software
  datadope.discovery.software_facts: {}
```

## Return Values

### ansible_facts (always, dict)
Facts to add to ansible_facts:

* software (always, list): List of the detected software.

  * type (always, str): Name of the software type.

  * process (always, dict):
        Discovered processes for the given software.

    * pid (always, str):
          PID of the software process.

     * ppid (always, str):
          Parent PID of the software process.

    * cmdline (always, str):
          CMDLine of the software process.

    * listening_ports (if available, list):
          List of the ports where the software is listening.

    * children (when process_type is set to child, list)
         List of the child processes of the parent (same structure from this process object)
    
  * listening_ports (if available, list): List of the ports where the software is listening.

  * packages (if `packages` is provided and return_packages is True, list, ): List of packages info

  * version (if available, list):
          Information about theversion of software obtained in different ways. Each version element has the fields:

    * type (always, str): 
            The mechanism used to get the version

    * number (always, str)
            Version info


  * discovery_time (always, str):
          Instant when Discovery was executed.
          With time format: yyyy-mm-ddTHH:MM:SS+0x:00.

  * docker (If the software is installed as a docker container, dict):
          Information about the container that is running the software. The object will have the following fields: 

    * id (always, str):
            Docker container Id.

    * image (always, str):
            Docker container image (from container's Config.Image field).

    * name (always, str):
            Docker container Name.

    * exposed_ports (always, dict):
            Docker container exposed ports (from container's Config.ExposedPorts field).

    * network_mode (always, str):
            Docker container network mode (from container's HostConfig.NetworkMode field).

    * port_bindings (always, dict):
            Docker container port bindings (from container's HostConfig.PortBindings field)


  * files (if available, list):
          List of files discovered for the software instance. Each element will have the fields:

    * path (always, str):
            The full path of the file/object to store

    * name (if a file name is available., str):
            The name of the file itself

    * type (always, str):
            Type of the file to be stored. Ex: 'bin', 'config', etc.

    * subtype (if provided, str):
            A secondary type if it's needed due to multiple files of the same type

    * extra_data (if additional info is available., dict):
            A dict to store additional information about the file being returned.


  * bindings (if available, list):
          List of bindings discovered for the software instance. Each element will have the fields:
          A binding is a connection point to the software conformed by an address and a port.

    * address (if provided, str):
            IP information of the object to add.

    * port (if provided, str):
            Port information of the object to add.

    * protocol (if provided, str):
            Protocol of the object to add.

    * class (always, str):
            Class type of the IP/port.

    * extra_data (if additional info is available., dict):
            A dict to store additional information about the file being returned.


  * endpoints (if available, list):
          List of endpoints discovered for the software instance.
          An endpoint is a connection point to the software conformed by an uri.
          Each element will have the fields:

    * uri (always, str):
            The uri of the endpoint.

    * type (always, str):
            Type of the endpoint.

    * extra_data (if additional info is available., dict):
            A dict to store additional information about the file being returned.


  * messages (if available, list):
          List of messages sent by the remote host in the discovery process. Each element will have the fields:

    * msg (always, str):
            The message to store.

    * key (If the message should be associated with a variable., str):
            A key to provide with the message to identify the problem

    * value (If the key field is returned., raw):
            A value for the key. Can be of any type of data

    * extra_data (if additional info is available., dict):
            A dict to store additional information about the message we are storing.


  * extra_data (if additional info is available., dict):
          Other information related to the precise software not having place in the other software fields.
          Data is returned as key/value pairs. Value may be of any type of data.

# License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

# Authors

- Datadope (@datadope-io)
