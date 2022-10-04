# datadope.discovery collection development environment

Following you can find the instructions to create a development environment where you can build and test this 
collection and the modifications being performed. This environment allows executing pytest in local apart
from using ansible-test tools to run tests.

## Create python virtual env

Generate a virtual env in a development root dir:

```shell 
python -m venv venv
```

and activate that virtual env:

```shell
source venv/bin/activate
```

Following pip packages must be installed in this virtual env. You can choose ansible version, but it should be 
higher than the minimum supported version:
  * `ansible`
  * `pytest`
  * `pytest-lazy-fixture`
  * `pytest-ansible-units`

## Prepare for ansible collection development

In the development root directory create a subdir: `ansible_collections`.

You have to deploy from source the following collections:
* `ansible.windows`
* `community.general`
* `community.internal_test_tools`
* `communitu.windows`

```
cd ansible_collections
mkdir ansible
cd ansible
git clone git@github.com:ansible-collections/ansible.windows.git windows
cd ..
mkdir community
cd community
git clone git@github.com:ansible-collections/community.general.git general
git clone git@github.com:ansible-collections/community.internal_test_tools.git internal_test_tools
git clone git@github.com:ansible-collections/community.windows.git windows
```

## Deploy datadope.discovery

This collection has to be deployed from sources also under ansible_collections subdir:

```
cd ansible_collections
mkdir datadope
cd datadope
git clone ssh://git@github.com/datadope-io/ansible_collection_discovery.git discovery
```

## Ansible configuration for tests

An ansible.cfg file must be created in the collection main folder:

```
[defaults]
COLLECTIONS_PATHS = <development_root_dir>:<user_dir>.ansible/collections:/usr/share/ansible/collections
```

`development_root_dir`: if the root directory where the virtual env has been created. So `ansible_collections` dir must be a subdir of this root dir.
`user_dir`: user main dir as `/home/username`.


## Running unit tests locally

```
cd ansible_collections/datadope/discovery
pytest tests
```

## Running unit tests using ansible-test tool

```
cd ansible_collections/datadope/discovery
ansible-test units --docker default -v --python 3.8
```


## Running sanity tests using ansible-test tool

```
cd ansible_collections/datadope/discovery
ansible-test sanity --docker default
```
