# win_package_facts -- Gather the facts of the packages of the machine

## Synopsis

Gather the information from the packages of the machine.

Supports x32 and x64 systems.

The module goal is to replicate the functionality of the linux module package_facts, 
maintaining the format of the said module.


## Parameters

### gather_current_user (optional, bool, True)
Establish if the current user packages should be gathered, in addition to the system-wide packages.

### gather_external_users (optional, bool, False)
Establish if the other users' packages should be gathered, in addition to the system-wide packages. 
This option mounts other users' registries if they are not logged in, so it should be used with care, 
since it could have an impact on the system. Also, this option requires the user to be an administrator.


## Notes

   - The external users' registries are unmounted after the information is gathered.
   - The value of each key of packages is a list of dicts, since multiple versions of the same package can be installed while maintaining the name of the package.
   - The generated data (packages) and the fields within follows the package_facts schema to achieve compatibility with the said module output, even though this module is capable of extracting additional information about the system packages.

## See Also

`ansible.builtin.package_facts_module`: The official documentation on the **ansible.builtin.package_facts** module.

## Examples

```yaml
    
    - name: Gather system packages facts
      community.windows.win_package_facts:

    - name: Gather system and current user packages facts
      community.windows.win_package_facts:
        gather_current_user: true

    - name: Gather system and external users packages facts
      community.windows.win_package_facts:
        gather_external_users: true

    - name: Gather system, current user and external users packages facts
      community.windows.win_package_facts:
        gather_current_user: true
        gather_external_users: true

```


## Return Values

packages (success, list): List of dicts with the detected packages

# License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

# Authors

- Datadope (@datadope-io)
