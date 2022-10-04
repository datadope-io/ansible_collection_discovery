# datadope.discovery.docker_containers

This role gets running docker containers in a host if docker is installed. 

Non-running docker containers may be included if var `docker_containers__docker_ps_all` is set to `true`.

The result is provided as an ansible fact with key `dockers` with an element `containers` that will contain a list of 
running dockers information. The information provided for each docker is similar to the information returned by
a `docker inspect` command.

## Requirements

### Docker

When you are a Docker user and using Ansible 2.10 or newer, 
then there is a dependency on the collection named `community.docker`. 
This collection is needed as the `docker_` modules are now part of collections and not standard in Ansible anymore. 
Installing the collection:

```sh
ansible-galaxy collection install community.docker
```

This community requires the [Docker SDK for Python](https://pypi.org/project/docker/) to be installed on the host to run.


A fallback method is implemented in case these requirements are not fulfilled 
issuing commands as `docker ps` `docker inspect` on the host machine.

## Role Variables

* `docker_containers__docker_ps_all`: (bool) If true, the dockers result fact will include non-running dockers.

## Example Playbook

```yaml
- hosts: servers
  roles:
     - role: datadope.discovery.docker_containers
```

## License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

## Author Information

Please send suggestions or pull requests to make this role better. 
Also let us know if you encounter any issues installing or using this role.

GitHub: https://github.com/datadope-io/ansible_collection_discovery

