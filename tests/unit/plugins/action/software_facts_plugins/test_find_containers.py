from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.errors import AnsibleRuntimeError

from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.find_containers \
    import FindContainers as PluginToTest


def test_get_args_spec():
    assert PluginToTest.get_args_spec() == {
        'filter': {
            'type': 'dict',
            'required': False,
            'default': {}
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (dict(filter={'foo': 'bar'}), True),
        (dict(), True),
        (dict(filter='fail'), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'find_containers'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = {
        'filter': {
            'Config': {
                'Image': 'skydive:.*27.*'
            }
        }
    }
    expected_result = [
        {
            "Platform": "linux",
            "State": {
                "Status": "running",
                "Pid": 5410,
                "OOMKilled": False,
                "Dead": False,
                "Paused": False,
                "Running": True,
                "FinishedAt": "2022-04-26T15:54:39.214694889Z",
                "Restarting": False,
                "Error": "",
                "StartedAt": "2022-04-26T15:54:45.981734261Z",
                "ExitCode": 0
            },
            "Config": {
                "Tty": False,
                "Hostname": "skydive01.novalocal",
                "Env": [
                    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                ],
                "Domainname": "",
                "StdinOnce": False,
                "Image": "skydive:v0.27.0",
                "Cmd": [
                    "analyzer",
                    "-c",
                    "/etc/skydive/skydive.yml"
                ],
                "WorkingDir": "",
                "Labels": {},
                "AttachStdin": False,
                "User": "",
                "Volumes": {
                    "/var/lib/skydive": {},
                    "/etc/skydive/skydive.yml": {}
                },
                "ExposedPorts": {
                    "8082/tcp": {}
                },
                "OnBuild": None,
                "AttachStderr": False,
                "Entrypoint": [
                    "/usr/local/bin/skydive"
                ],
                "AttachStdout": False,
                "OpenStdin": False
            },
            "HostsPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hosts",
            "Image": "sha256:b369c109fc2634db304c113cd9ae5386dcfdbee12a37abed3b0544a2a3e83d38",
            "Args": [
                "analyzer",
                "-c",
                "/etc/skydive/skydive.yml"
            ],
            "Driver": "overlay2",
            "Path": "/usr/local/bin/skydive",
            "HostnamePath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hostname",
            "RestartCount": 0,
            "Name": "/skydive-analyzer",
            "Created": "2022-02-21T11:57:10.201558481Z",
            "ExecIDs": None,
            "GraphDriver": {
                "Data": {
                    "LowerDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0-init/diff:"
                                "/var/lib/docker/overlay2/c3341d451baed12e57e850b43b2c6205849a00e"
                                "3697aa31c62872c74318c84c6/diff:/var/lib/docker/overlay2/7a056e9d"
                                "541e437c2baecb9469f65e25a5434cc1f6195c743ec27a0ce729f458/diff:"
                                "/var/lib/docker/overlay2/73c276c089c4c664867fac16d2b79904449b992"
                                "8bf8f2fdadb08743f4dcb0570/diff",
                    "WorkDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/work",
                    "MergedDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/merged",
                    "UpperDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/diff"
                },
                "Name": "overlay2"
            },
            "Mounts": [
                {
                    "RW": True,
                    "Source": "/etc/skydive/skydive.yml",
                    "Destination": "/etc/skydive/skydive.yml",
                    "Propagation": "rprivate",
                    "Mode": "rw",
                    "Type": "bind"
                },
                {
                    "RW": True,
                    "Source": "/var/lib/skydive",
                    "Destination": "/var/lib/skydive",
                    "Propagation": "rprivate",
                    "Mode": "rw",
                    "Type": "bind"
                }
            ],
            "ProcessLabel": "",
            "NetworkSettings": {
                "Bridge": "",
                "GlobalIPv6PrefixLen": 0,
                "LinkLocalIPv6Address": "",
                "HairpinMode": False,
                "IPAddress": "",
                "SecondaryIPAddresses": None,
                "SandboxID": "e4dcc47facee23c3ebc096c0f8113bfe13a1b7458afeb7bca9377f756cd52d2a",
                "SandboxKey": "/var/run/docker/netns/default",
                "GlobalIPv6Address": "",
                "Gateway": "",
                "LinkLocalIPv6PrefixLen": 0,
                "EndpointID": "",
                "SecondaryIPv6Addresses": None,
                "MacAddress": "",
                "IPPrefixLen": 0,
                "IPv6Gateway": "",
                "Networks": {
                    "host": {
                        "NetworkID": "efe5541c0d38ec7e32ddd9e836e96497f0dfddce03630245bb96032dadc1c5fe",
                        "MacAddress": "",
                        "GlobalIPv6PrefixLen": 0,
                        "Links": None,
                        "GlobalIPv6Address": "",
                        "IPAddress": "",
                        "Gateway": "",
                        "DriverOpts": None,
                        "IPPrefixLen": 0,
                        "EndpointID": "ba283edb832a5cee669fc1fcfcee56331ff46dea1cce4ad680fadb1434300039",
                        "IPv6Gateway": "",
                        "IPAMConfig": None,
                        "Aliases": None
                    }
                },
                "Ports": {}
            },
            "AppArmorProfile": "",
            "ResolvConfPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/resolv.conf",
            "LogPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/60aec879332b18e43681ae2e-json.log",
            "HostConfig": {
                "CpuPeriod": 0,
                "MemorySwappiness": None,
                "AutoRemove": False,
                "MemorySwap": 0,
                "PortBindings": None,
                "BlkioDeviceReadIOps": None,
                "Capabilities": None,
                "UsernsMode": "",
                "UTSMode": "",
                "ConsoleSize": [
                    0,
                    0
                ],
                "CpusetMems": "",
                "Dns": [],
                "Memory": 0,
                "PidsLimit": None,
                "CgroupParent": "",
                "Privileged": False,
                "IOMaximumIOps": 0,
                "LogConfig": {
                    "Type": "json-file",
                    "Config": {
                        "max-size": "20m",
                        "max-file": "1"
                    }
                },
                "NanoCpus": 0,
                "CpusetCpus": "",
                "PidMode": "",
                "DnsSearch": [],
                "BlkioWeight": 0,
                "RestartPolicy": {
                    "MaximumRetryCount": 0,
                    "Name": "unless-stopped"
                },
                "OomScoreAdj": 0,
                "BlkioDeviceReadBps": None,
                "VolumeDriver": "",
                "ReadonlyRootfs": False,
                "CpuShares": 0,
                "PublishAllPorts": False,
                "MemoryReservation": 0,
                "BlkioWeightDevice": None,
                "CpuPercent": 0,
                "NetworkMode": "host",
                "BlkioDeviceWriteBps": None,
                "Isolation": "",
                "GroupAdd": None,
                "ReadonlyPaths": [
                    "/proc/bus",
                    "/proc/fs",
                    "/proc/irq",
                    "/proc/sys",
                    "/proc/sysrq-trigger"
                ],
                "CpuRealtimeRuntime": 0,
                "Devices": None,
                "BlkioDeviceWriteIOps": None,
                "VolumesFrom": None,
                "Binds": [
                    "/var/lib/skydive/:/var/lib/skydive:rw",
                    "/etc/skydive/skydive.yml:/etc/skydive/skydive.yml:rw"
                ],
                "CpuQuota": 0,
                "KernelMemory": 0,
                "Cgroup": "",
                "ExtraHosts": None,
                "Runtime": "runc",
                "Ulimits": None,
                "CapDrop": None,
                "DnsOptions": [],
                "Links": None,
                "ShmSize": 67108864,
                "CpuRealtimePeriod": 0,
                "IpcMode": "private",
                "MaskedPaths": [
                    "/proc/asound",
                    "/proc/acpi",
                    "/proc/kcore",
                    "/proc/keys",
                    "/proc/latency_stats",
                    "/proc/timer_list",
                    "/proc/timer_stats",
                    "/proc/sched_debug",
                    "/proc/scsi",
                    "/sys/firmware"
                ],
                "ContainerIDFile": "",
                "SecurityOpt": None,
                "CapAdd": None,
                "CpuCount": 0,
                "DeviceCgroupRules": None,
                "KernelMemoryTCP": 0,
                "OomKillDisable": False,
                "DeviceRequests": None,
                "IOMaximumBandwidth": 0
            },
            "MountLabel": "",
            "Id": "60aec879332b18e43681ae2e"
        },
        {
            "Platform": "linux",
            "State": {
                "Status": "running",
                "Pid": 5415,
                "OOMKilled": False,
                "Dead": False,
                "Paused": False,
                "Running": True,
                "FinishedAt": "2022-04-26T15:54:39.214694889Z",
                "Restarting": False,
                "Error": "",
                "StartedAt": "2022-04-26T15:54:45.981734261Z",
                "ExitCode": 0
            },
            "Config": {
                "Tty": False,
                "Hostname": "skydive01.novalocal",
                "Env": [
                    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                ],
                "Domainname": "",
                "StdinOnce": False,
                "Image": "skydive:v0.27.0",
                "Cmd": [
                    "analyzer",
                    "-c",
                    "/etc/skydive/skydive.yml"
                ],
                "WorkingDir": "",
                "Labels": {},
                "AttachStdin": False,
                "User": "",
                "Volumes": {
                    "/var/lib/skydive": {},
                    "/etc/skydive/skydive.yml": {}
                },
                "ExposedPorts": {
                    "8082/tcp": {}
                },
                "OnBuild": None,
                "AttachStderr": False,
                "Entrypoint": [
                    "/usr/local/bin/skydive"
                ],
                "AttachStdout": False,
                "OpenStdin": False
            },
            "HostsPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hosts",
            "Image": "sha256:b369c109fc2634db304c113cd9ae5386dcfdbee12a37abed3b0544a2a3e83d38",
            "Args": [
                "analyzer",
                "-c",
                "/etc/skydive/skydive.yml"
            ],
            "Driver": "overlay2",
            "Path": "/usr/local/bin/skydive",
            "HostnamePath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hostname",
            "RestartCount": 0,
            "Name": "/skydive-analyzer",
            "Created": "2022-02-21T11:57:10.201558481Z",
            "ExecIDs": None,
            "GraphDriver": {
                "Data": {
                    "LowerDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0-init/diff:"
                                "/var/lib/docker/overlay2/c3341d451baed12e57e850b43b2c6205849a00e"
                                "3697aa31c62872c74318c84c6/diff:/var/lib/docker/overlay2/7a056e9d"
                                "541e437c2baecb9469f65e25a5434cc1f6195c743ec27a0ce729f458/diff:"
                                "/var/lib/docker/overlay2/73c276c089c4c664867fac16d2b79904449b992"
                                "8bf8f2fdadb08743f4dcb0570/diff",
                    "WorkDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/work",
                    "MergedDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/merged",
                    "UpperDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/diff"
                },
                "Name": "overlay2"
            },
            "Mounts": [
                {
                    "RW": True,
                    "Source": "/etc/skydive/skydive.yml",
                    "Destination": "/etc/skydive/skydive.yml",
                    "Propagation": "rprivate",
                    "Mode": "rw",
                    "Type": "bind"
                },
                {
                    "RW": True,
                    "Source": "/var/lib/skydive",
                    "Destination": "/var/lib/skydive",
                    "Propagation": "rprivate",
                    "Mode": "rw",
                    "Type": "bind"
                }
            ],
            "ProcessLabel": "",
            "NetworkSettings": {
                "Bridge": "",
                "GlobalIPv6PrefixLen": 0,
                "LinkLocalIPv6Address": "",
                "HairpinMode": False,
                "IPAddress": "",
                "SecondaryIPAddresses": None,
                "SandboxID": "e4dcc47facee23c3ebc096c0f8113bfe13a1b7458afeb7bca9377f756cd52d2a",
                "SandboxKey": "/var/run/docker/netns/default",
                "GlobalIPv6Address": "",
                "Gateway": "",
                "LinkLocalIPv6PrefixLen": 0,
                "EndpointID": "",
                "SecondaryIPv6Addresses": None,
                "MacAddress": "",
                "IPPrefixLen": 0,
                "IPv6Gateway": "",
                "Networks": {
                    "host": {
                        "NetworkID": "efe5541c0d38ec7e32ddd9e836e96497f0dfddce03630245bb96032dadc1c5fe",
                        "MacAddress": "",
                        "GlobalIPv6PrefixLen": 0,
                        "Links": None,
                        "GlobalIPv6Address": "",
                        "IPAddress": "",
                        "Gateway": "",
                        "DriverOpts": None,
                        "IPPrefixLen": 0,
                        "EndpointID": "ba283edb832a5cee669fc1fcfcee56331ff46dea1cce4ad680fadb1434300039",
                        "IPv6Gateway": "",
                        "IPAMConfig": None,
                        "Aliases": None
                    }
                },
                "Ports": {}
            },
            "AppArmorProfile": "",
            "ResolvConfPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/resolv.conf",
            "LogPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/60aec879332b18e43681ae2e-json.log",
            "HostConfig": {
                "CpuPeriod": 0,
                "MemorySwappiness": None,
                "AutoRemove": False,
                "MemorySwap": 0,
                "PortBindings": None,
                "BlkioDeviceReadIOps": None,
                "Capabilities": None,
                "UsernsMode": "",
                "UTSMode": "",
                "ConsoleSize": [
                    0,
                    0
                ],
                "CpusetMems": "",
                "Dns": [],
                "Memory": 0,
                "PidsLimit": None,
                "CgroupParent": "",
                "Privileged": False,
                "IOMaximumIOps": 0,
                "LogConfig": {
                    "Type": "json-file",
                    "Config": {
                        "max-size": "20m",
                        "max-file": "1"
                    }
                },
                "NanoCpus": 0,
                "CpusetCpus": "",
                "PidMode": "",
                "DnsSearch": [],
                "BlkioWeight": 0,
                "RestartPolicy": {
                    "MaximumRetryCount": 0,
                    "Name": "unless-stopped"
                },
                "OomScoreAdj": 0,
                "BlkioDeviceReadBps": None,
                "VolumeDriver": "",
                "ReadonlyRootfs": False,
                "CpuShares": 0,
                "PublishAllPorts": False,
                "MemoryReservation": 0,
                "BlkioWeightDevice": None,
                "CpuPercent": 0,
                "NetworkMode": "host",
                "BlkioDeviceWriteBps": None,
                "Isolation": "",
                "GroupAdd": None,
                "ReadonlyPaths": [
                    "/proc/bus",
                    "/proc/fs",
                    "/proc/irq",
                    "/proc/sys",
                    "/proc/sysrq-trigger"
                ],
                "CpuRealtimeRuntime": 0,
                "Devices": None,
                "BlkioDeviceWriteIOps": None,
                "VolumesFrom": None,
                "Binds": [
                    "/var/lib/skydive/:/var/lib/skydive:rw",
                    "/etc/skydive/skydive.yml:/etc/skydive/skydive.yml:rw"
                ],
                "CpuQuota": 0,
                "KernelMemory": 0,
                "Cgroup": "",
                "ExtraHosts": None,
                "Runtime": "runc",
                "Ulimits": None,
                "CapDrop": None,
                "DnsOptions": [],
                "Links": None,
                "ShmSize": 67108864,
                "CpuRealtimePeriod": 0,
                "IpcMode": "private",
                "MaskedPaths": [
                    "/proc/asound",
                    "/proc/acpi",
                    "/proc/kcore",
                    "/proc/keys",
                    "/proc/latency_stats",
                    "/proc/timer_list",
                    "/proc/timer_stats",
                    "/proc/sched_debug",
                    "/proc/scsi",
                    "/sys/firmware"
                ],
                "ContainerIDFile": "",
                "SecurityOpt": None,
                "CapAdd": None,
                "CpuCount": 0,
                "DeviceCgroupRules": None,
                "KernelMemoryTCP": 0,
                "OomKillDisable": False,
                "DeviceRequests": None,
                "IOMaximumBandwidth": 0
            },
            "MountLabel": "",
            "Id": "60aec879332b18e43681ae2e"
        }
    ]
    task_vars = {
        "dockers": {
            "containers": [
                {
                    "Platform": "linux",
                    "State": {
                        "Status": "running",
                        "Pid": 5410,
                        "OOMKilled": False,
                        "Dead": False,
                        "Paused": False,
                        "Running": True,
                        "FinishedAt": "2022-04-26T15:54:39.214694889Z",
                        "Restarting": False,
                        "Error": "",
                        "StartedAt": "2022-04-26T15:54:45.981734261Z",
                        "ExitCode": 0
                    },
                    "Config": {
                        "Tty": False,
                        "Hostname": "skydive01.novalocal",
                        "Env": [
                            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                        ],
                        "Domainname": "",
                        "StdinOnce": False,
                        "Image": "skydive:v0.27.0",
                        "Cmd": [
                            "analyzer",
                            "-c",
                            "/etc/skydive/skydive.yml"
                        ],
                        "WorkingDir": "",
                        "Labels": {},
                        "AttachStdin": False,
                        "User": "",
                        "Volumes": {
                            "/var/lib/skydive": {},
                            "/etc/skydive/skydive.yml": {}
                        },
                        "ExposedPorts": {
                            "8082/tcp": {}
                        },
                        "OnBuild": None,
                        "AttachStderr": False,
                        "Entrypoint": [
                            "/usr/local/bin/skydive"
                        ],
                        "AttachStdout": False,
                        "OpenStdin": False
                    },
                    "HostsPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hosts",
                    "Image": "sha256:b369c109fc2634db304c113cd9ae5386dcfdbee12a37abed3b0544a2a3e83d38",
                    "Args": [
                        "analyzer",
                        "-c",
                        "/etc/skydive/skydive.yml"
                    ],
                    "Driver": "overlay2",
                    "Path": "/usr/local/bin/skydive",
                    "HostnamePath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hostname",
                    "RestartCount": 0,
                    "Name": "/skydive-analyzer",
                    "Created": "2022-02-21T11:57:10.201558481Z",
                    "ExecIDs": None,
                    "GraphDriver": {
                        "Data": {
                            "LowerDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0-init/diff:"
                                        "/var/lib/docker/overlay2/c3341d451baed12e57e850b43b2c6205849a00e"
                                        "3697aa31c62872c74318c84c6/diff:/var/lib/docker/overlay2/7a056e9d"
                                        "541e437c2baecb9469f65e25a5434cc1f6195c743ec27a0ce729f458/diff:"
                                        "/var/lib/docker/overlay2/73c276c089c4c664867fac16d2b79904449b992"
                                        "8bf8f2fdadb08743f4dcb0570/diff",
                            "WorkDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/work",
                            "MergedDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/merged",
                            "UpperDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/diff"
                        },
                        "Name": "overlay2"
                    },
                    "Mounts": [
                        {
                            "RW": True,
                            "Source": "/etc/skydive/skydive.yml",
                            "Destination": "/etc/skydive/skydive.yml",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        },
                        {
                            "RW": True,
                            "Source": "/var/lib/skydive",
                            "Destination": "/var/lib/skydive",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        }
                    ],
                    "ProcessLabel": "",
                    "NetworkSettings": {
                        "Bridge": "",
                        "GlobalIPv6PrefixLen": 0,
                        "LinkLocalIPv6Address": "",
                        "HairpinMode": False,
                        "IPAddress": "",
                        "SecondaryIPAddresses": None,
                        "SandboxID": "e4dcc47facee23c3ebc096c0f8113bfe13a1b7458afeb7bca9377f756cd52d2a",
                        "SandboxKey": "/var/run/docker/netns/default",
                        "GlobalIPv6Address": "",
                        "Gateway": "",
                        "LinkLocalIPv6PrefixLen": 0,
                        "EndpointID": "",
                        "SecondaryIPv6Addresses": None,
                        "MacAddress": "",
                        "IPPrefixLen": 0,
                        "IPv6Gateway": "",
                        "Networks": {
                            "host": {
                                "NetworkID": "efe5541c0d38ec7e32ddd9e836e96497f0dfddce03630245bb96032dadc1c5fe",
                                "MacAddress": "",
                                "GlobalIPv6PrefixLen": 0,
                                "Links": None,
                                "GlobalIPv6Address": "",
                                "IPAddress": "",
                                "Gateway": "",
                                "DriverOpts": None,
                                "IPPrefixLen": 0,
                                "EndpointID": "ba283edb832a5cee669fc1fcfcee56331ff46dea1cce4ad680fadb1434300039",
                                "IPv6Gateway": "",
                                "IPAMConfig": None,
                                "Aliases": None
                            }
                        },
                        "Ports": {}
                    },
                    "AppArmorProfile": "",
                    "ResolvConfPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/resolv.conf",
                    "LogPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/60aec879332b18e43681ae2e-json.log",
                    "HostConfig": {
                        "CpuPeriod": 0,
                        "MemorySwappiness": None,
                        "AutoRemove": False,
                        "MemorySwap": 0,
                        "PortBindings": None,
                        "BlkioDeviceReadIOps": None,
                        "Capabilities": None,
                        "UsernsMode": "",
                        "UTSMode": "",
                        "ConsoleSize": [
                            0,
                            0
                        ],
                        "CpusetMems": "",
                        "Dns": [],
                        "Memory": 0,
                        "PidsLimit": None,
                        "CgroupParent": "",
                        "Privileged": False,
                        "IOMaximumIOps": 0,
                        "LogConfig": {
                            "Type": "json-file",
                            "Config": {
                                "max-size": "20m",
                                "max-file": "1"
                            }
                        },
                        "NanoCpus": 0,
                        "CpusetCpus": "",
                        "PidMode": "",
                        "DnsSearch": [],
                        "BlkioWeight": 0,
                        "RestartPolicy": {
                            "MaximumRetryCount": 0,
                            "Name": "unless-stopped"
                        },
                        "OomScoreAdj": 0,
                        "BlkioDeviceReadBps": None,
                        "VolumeDriver": "",
                        "ReadonlyRootfs": False,
                        "CpuShares": 0,
                        "PublishAllPorts": False,
                        "MemoryReservation": 0,
                        "BlkioWeightDevice": None,
                        "CpuPercent": 0,
                        "NetworkMode": "host",
                        "BlkioDeviceWriteBps": None,
                        "Isolation": "",
                        "GroupAdd": None,
                        "ReadonlyPaths": [
                            "/proc/bus",
                            "/proc/fs",
                            "/proc/irq",
                            "/proc/sys",
                            "/proc/sysrq-trigger"
                        ],
                        "CpuRealtimeRuntime": 0,
                        "Devices": None,
                        "BlkioDeviceWriteIOps": None,
                        "VolumesFrom": None,
                        "Binds": [
                            "/var/lib/skydive/:/var/lib/skydive:rw",
                            "/etc/skydive/skydive.yml:/etc/skydive/skydive.yml:rw"
                        ],
                        "CpuQuota": 0,
                        "KernelMemory": 0,
                        "Cgroup": "",
                        "ExtraHosts": None,
                        "Runtime": "runc",
                        "Ulimits": None,
                        "CapDrop": None,
                        "DnsOptions": [],
                        "Links": None,
                        "ShmSize": 67108864,
                        "CpuRealtimePeriod": 0,
                        "IpcMode": "private",
                        "MaskedPaths": [
                            "/proc/asound",
                            "/proc/acpi",
                            "/proc/kcore",
                            "/proc/keys",
                            "/proc/latency_stats",
                            "/proc/timer_list",
                            "/proc/timer_stats",
                            "/proc/sched_debug",
                            "/proc/scsi",
                            "/sys/firmware"
                        ],
                        "ContainerIDFile": "",
                        "SecurityOpt": None,
                        "CapAdd": None,
                        "CpuCount": 0,
                        "DeviceCgroupRules": None,
                        "KernelMemoryTCP": 0,
                        "OomKillDisable": False,
                        "DeviceRequests": None,
                        "IOMaximumBandwidth": 0
                    },
                    "MountLabel": "",
                    "Id": "60aec879332b18e43681ae2e"
                },
                {
                    "Platform": "linux",
                    "State": {
                        "Status": "running",
                        "Pid": 5411,
                        "OOMKilled": False,
                        "Dead": False,
                        "Paused": False,
                        "Running": True,
                        "FinishedAt": "2022-04-26T15:54:39.214694889Z",
                        "Restarting": False,
                        "Error": "",
                        "StartedAt": "2022-04-26T15:54:45.981734261Z",
                        "ExitCode": 0
                    },
                    "Config": {
                        "Tty": False,
                        "Hostname": "skydive01.novalocal",
                        "Env": [
                            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                        ],
                        "Domainname": "",
                        "StdinOnce": False,
                        "Image": "skydive:v0.28.0",
                        "Cmd": [
                            "analyzer",
                            "-c",
                            "/etc/skydive/skydive.yml"
                        ],
                        "WorkingDir": "",
                        "Labels": {},
                        "AttachStdin": False,
                        "User": "",
                        "Volumes": {
                            "/var/lib/skydive": {},
                            "/etc/skydive/skydive.yml": {}
                        },
                        "ExposedPorts": {
                            "8082/tcp": {}
                        },
                        "OnBuild": None,
                        "AttachStderr": False,
                        "Entrypoint": [
                            "/usr/local/bin/skydive"
                        ],
                        "AttachStdout": False,
                        "OpenStdin": False
                    },
                    "HostsPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hosts",
                    "Image": "sha256:b369c109fc2634db304c113cd9ae5386dcfdbee12a37abed3b0544a2a3e83d38",
                    "Args": [
                        "analyzer",
                        "-c",
                        "/etc/skydive/skydive.yml"
                    ],
                    "Driver": "overlay2",
                    "Path": "/usr/local/bin/skydive",
                    "HostnamePath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hostname",
                    "RestartCount": 0,
                    "Name": "/skydive-analyzer",
                    "Created": "2022-02-21T11:57:10.201558481Z",
                    "ExecIDs": None,
                    "GraphDriver": {
                        "Data": {
                            "LowerDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0-init/diff:"
                                        "/var/lib/docker/overlay2/c3341d451baed12e57e850b43b2c6205849a00e"
                                        "3697aa31c62872c74318c84c6/diff:/var/lib/docker/overlay2/7a056e9d"
                                        "541e437c2baecb9469f65e25a5434cc1f6195c743ec27a0ce729f458/diff:"
                                        "/var/lib/docker/overlay2/73c276c089c4c664867fac16d2b79904449b992"
                                        "8bf8f2fdadb08743f4dcb0570/diff",
                            "WorkDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/work",
                            "MergedDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/merged",
                            "UpperDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/diff"
                        },
                        "Name": "overlay2"
                    },
                    "Mounts": [
                        {
                            "RW": True,
                            "Source": "/etc/skydive/skydive.yml",
                            "Destination": "/etc/skydive/skydive.yml",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        },
                        {
                            "RW": True,
                            "Source": "/var/lib/skydive",
                            "Destination": "/var/lib/skydive",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        }
                    ],
                    "ProcessLabel": "",
                    "NetworkSettings": {
                        "Bridge": "",
                        "GlobalIPv6PrefixLen": 0,
                        "LinkLocalIPv6Address": "",
                        "HairpinMode": False,
                        "IPAddress": "",
                        "SecondaryIPAddresses": None,
                        "SandboxID": "e4dcc47facee23c3ebc096c0f8113bfe13a1b7458afeb7bca9377f756cd52d2a",
                        "SandboxKey": "/var/run/docker/netns/default",
                        "GlobalIPv6Address": "",
                        "Gateway": "",
                        "LinkLocalIPv6PrefixLen": 0,
                        "EndpointID": "",
                        "SecondaryIPv6Addresses": None,
                        "MacAddress": "",
                        "IPPrefixLen": 0,
                        "IPv6Gateway": "",
                        "Networks": {
                            "host": {
                                "NetworkID": "efe5541c0d38ec7e32ddd9e836e96497f0dfddce03630245bb96032dadc1c5fe",
                                "MacAddress": "",
                                "GlobalIPv6PrefixLen": 0,
                                "Links": None,
                                "GlobalIPv6Address": "",
                                "IPAddress": "",
                                "Gateway": "",
                                "DriverOpts": None,
                                "IPPrefixLen": 0,
                                "EndpointID": "ba283edb832a5cee669fc1fcfcee56331ff46dea1cce4ad680fadb1434300039",
                                "IPv6Gateway": "",
                                "IPAMConfig": None,
                                "Aliases": None
                            }
                        },
                        "Ports": {}
                    },
                    "AppArmorProfile": "",
                    "ResolvConfPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/resolv.conf",
                    "LogPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/60aec879332b18e43681ae2e-json.log",
                    "HostConfig": {
                        "CpuPeriod": 0,
                        "MemorySwappiness": None,
                        "AutoRemove": False,
                        "MemorySwap": 0,
                        "PortBindings": None,
                        "BlkioDeviceReadIOps": None,
                        "Capabilities": None,
                        "UsernsMode": "",
                        "UTSMode": "",
                        "ConsoleSize": [
                            0,
                            0
                        ],
                        "CpusetMems": "",
                        "Dns": [],
                        "Memory": 0,
                        "PidsLimit": None,
                        "CgroupParent": "",
                        "Privileged": False,
                        "IOMaximumIOps": 0,
                        "LogConfig": {
                            "Type": "json-file",
                            "Config": {
                                "max-size": "20m",
                                "max-file": "1"
                            }
                        },
                        "NanoCpus": 0,
                        "CpusetCpus": "",
                        "PidMode": "",
                        "DnsSearch": [],
                        "BlkioWeight": 0,
                        "RestartPolicy": {
                            "MaximumRetryCount": 0,
                            "Name": "unless-stopped"
                        },
                        "OomScoreAdj": 0,
                        "BlkioDeviceReadBps": None,
                        "VolumeDriver": "",
                        "ReadonlyRootfs": False,
                        "CpuShares": 0,
                        "PublishAllPorts": False,
                        "MemoryReservation": 0,
                        "BlkioWeightDevice": None,
                        "CpuPercent": 0,
                        "NetworkMode": "host",
                        "BlkioDeviceWriteBps": None,
                        "Isolation": "",
                        "GroupAdd": None,
                        "ReadonlyPaths": [
                            "/proc/bus",
                            "/proc/fs",
                            "/proc/irq",
                            "/proc/sys",
                            "/proc/sysrq-trigger"
                        ],
                        "CpuRealtimeRuntime": 0,
                        "Devices": None,
                        "BlkioDeviceWriteIOps": None,
                        "VolumesFrom": None,
                        "Binds": [
                            "/var/lib/skydive/:/var/lib/skydive:rw",
                            "/etc/skydive/skydive.yml:/etc/skydive/skydive.yml:rw"
                        ],
                        "CpuQuota": 0,
                        "KernelMemory": 0,
                        "Cgroup": "",
                        "ExtraHosts": None,
                        "Runtime": "runc",
                        "Ulimits": None,
                        "CapDrop": None,
                        "DnsOptions": [],
                        "Links": None,
                        "ShmSize": 67108864,
                        "CpuRealtimePeriod": 0,
                        "IpcMode": "private",
                        "MaskedPaths": [
                            "/proc/asound",
                            "/proc/acpi",
                            "/proc/kcore",
                            "/proc/keys",
                            "/proc/latency_stats",
                            "/proc/timer_list",
                            "/proc/timer_stats",
                            "/proc/sched_debug",
                            "/proc/scsi",
                            "/sys/firmware"
                        ],
                        "ContainerIDFile": "",
                        "SecurityOpt": None,
                        "CapAdd": None,
                        "CpuCount": 0,
                        "DeviceCgroupRules": None,
                        "KernelMemoryTCP": 0,
                        "OomKillDisable": False,
                        "DeviceRequests": None,
                        "IOMaximumBandwidth": 0
                    },
                    "MountLabel": "",
                    "Id": "60aec879332b18e43681ae2e"
                },
                {
                    "Platform": "linux",
                    "State": {
                        "Status": "running",
                        "Pid": 5415,
                        "OOMKilled": False,
                        "Dead": False,
                        "Paused": False,
                        "Running": True,
                        "FinishedAt": "2022-04-26T15:54:39.214694889Z",
                        "Restarting": False,
                        "Error": "",
                        "StartedAt": "2022-04-26T15:54:45.981734261Z",
                        "ExitCode": 0
                    },
                    "Config": {
                        "Tty": False,
                        "Hostname": "skydive01.novalocal",
                        "Env": [
                            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                        ],
                        "Domainname": "",
                        "StdinOnce": False,
                        "Image": "skydive:v0.27.0",
                        "Cmd": [
                            "analyzer",
                            "-c",
                            "/etc/skydive/skydive.yml"
                        ],
                        "WorkingDir": "",
                        "Labels": {},
                        "AttachStdin": False,
                        "User": "",
                        "Volumes": {
                            "/var/lib/skydive": {},
                            "/etc/skydive/skydive.yml": {}
                        },
                        "ExposedPorts": {
                            "8082/tcp": {}
                        },
                        "OnBuild": None,
                        "AttachStderr": False,
                        "Entrypoint": [
                            "/usr/local/bin/skydive"
                        ],
                        "AttachStdout": False,
                        "OpenStdin": False
                    },
                    "HostsPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hosts",
                    "Image": "sha256:b369c109fc2634db304c113cd9ae5386dcfdbee12a37abed3b0544a2a3e83d38",
                    "Args": [
                        "analyzer",
                        "-c",
                        "/etc/skydive/skydive.yml"
                    ],
                    "Driver": "overlay2",
                    "Path": "/usr/local/bin/skydive",
                    "HostnamePath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hostname",
                    "RestartCount": 0,
                    "Name": "/skydive-analyzer",
                    "Created": "2022-02-21T11:57:10.201558481Z",
                    "ExecIDs": None,
                    "GraphDriver": {
                        "Data": {
                            "LowerDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0-init/diff:"
                                        "/var/lib/docker/overlay2/c3341d451baed12e57e850b43b2c6205849a00e"
                                        "3697aa31c62872c74318c84c6/diff:/var/lib/docker/overlay2/7a056e9d"
                                        "541e437c2baecb9469f65e25a5434cc1f6195c743ec27a0ce729f458/diff:"
                                        "/var/lib/docker/overlay2/73c276c089c4c664867fac16d2b79904449b992"
                                        "8bf8f2fdadb08743f4dcb0570/diff",
                            "WorkDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/work",
                            "MergedDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/merged",
                            "UpperDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/diff"
                        },
                        "Name": "overlay2"
                    },
                    "Mounts": [
                        {
                            "RW": True,
                            "Source": "/etc/skydive/skydive.yml",
                            "Destination": "/etc/skydive/skydive.yml",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        },
                        {
                            "RW": True,
                            "Source": "/var/lib/skydive",
                            "Destination": "/var/lib/skydive",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        }
                    ],
                    "ProcessLabel": "",
                    "NetworkSettings": {
                        "Bridge": "",
                        "GlobalIPv6PrefixLen": 0,
                        "LinkLocalIPv6Address": "",
                        "HairpinMode": False,
                        "IPAddress": "",
                        "SecondaryIPAddresses": None,
                        "SandboxID": "e4dcc47facee23c3ebc096c0f8113bfe13a1b7458afeb7bca9377f756cd52d2a",
                        "SandboxKey": "/var/run/docker/netns/default",
                        "GlobalIPv6Address": "",
                        "Gateway": "",
                        "LinkLocalIPv6PrefixLen": 0,
                        "EndpointID": "",
                        "SecondaryIPv6Addresses": None,
                        "MacAddress": "",
                        "IPPrefixLen": 0,
                        "IPv6Gateway": "",
                        "Networks": {
                            "host": {
                                "NetworkID": "efe5541c0d38ec7e32ddd9e836e96497f0dfddce03630245bb96032dadc1c5fe",
                                "MacAddress": "",
                                "GlobalIPv6PrefixLen": 0,
                                "Links": None,
                                "GlobalIPv6Address": "",
                                "IPAddress": "",
                                "Gateway": "",
                                "DriverOpts": None,
                                "IPPrefixLen": 0,
                                "EndpointID": "ba283edb832a5cee669fc1fcfcee56331ff46dea1cce4ad680fadb1434300039",
                                "IPv6Gateway": "",
                                "IPAMConfig": None,
                                "Aliases": None
                            }
                        },
                        "Ports": {}
                    },
                    "AppArmorProfile": "",
                    "ResolvConfPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/resolv.conf",
                    "LogPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/60aec879332b18e43681ae2e-json.log",
                    "HostConfig": {
                        "CpuPeriod": 0,
                        "MemorySwappiness": None,
                        "AutoRemove": False,
                        "MemorySwap": 0,
                        "PortBindings": None,
                        "BlkioDeviceReadIOps": None,
                        "Capabilities": None,
                        "UsernsMode": "",
                        "UTSMode": "",
                        "ConsoleSize": [
                            0,
                            0
                        ],
                        "CpusetMems": "",
                        "Dns": [],
                        "Memory": 0,
                        "PidsLimit": None,
                        "CgroupParent": "",
                        "Privileged": False,
                        "IOMaximumIOps": 0,
                        "LogConfig": {
                            "Type": "json-file",
                            "Config": {
                                "max-size": "20m",
                                "max-file": "1"
                            }
                        },
                        "NanoCpus": 0,
                        "CpusetCpus": "",
                        "PidMode": "",
                        "DnsSearch": [],
                        "BlkioWeight": 0,
                        "RestartPolicy": {
                            "MaximumRetryCount": 0,
                            "Name": "unless-stopped"
                        },
                        "OomScoreAdj": 0,
                        "BlkioDeviceReadBps": None,
                        "VolumeDriver": "",
                        "ReadonlyRootfs": False,
                        "CpuShares": 0,
                        "PublishAllPorts": False,
                        "MemoryReservation": 0,
                        "BlkioWeightDevice": None,
                        "CpuPercent": 0,
                        "NetworkMode": "host",
                        "BlkioDeviceWriteBps": None,
                        "Isolation": "",
                        "GroupAdd": None,
                        "ReadonlyPaths": [
                            "/proc/bus",
                            "/proc/fs",
                            "/proc/irq",
                            "/proc/sys",
                            "/proc/sysrq-trigger"
                        ],
                        "CpuRealtimeRuntime": 0,
                        "Devices": None,
                        "BlkioDeviceWriteIOps": None,
                        "VolumesFrom": None,
                        "Binds": [
                            "/var/lib/skydive/:/var/lib/skydive:rw",
                            "/etc/skydive/skydive.yml:/etc/skydive/skydive.yml:rw"
                        ],
                        "CpuQuota": 0,
                        "KernelMemory": 0,
                        "Cgroup": "",
                        "ExtraHosts": None,
                        "Runtime": "runc",
                        "Ulimits": None,
                        "CapDrop": None,
                        "DnsOptions": [],
                        "Links": None,
                        "ShmSize": 67108864,
                        "CpuRealtimePeriod": 0,
                        "IpcMode": "private",
                        "MaskedPaths": [
                            "/proc/asound",
                            "/proc/acpi",
                            "/proc/kcore",
                            "/proc/keys",
                            "/proc/latency_stats",
                            "/proc/timer_list",
                            "/proc/timer_stats",
                            "/proc/sched_debug",
                            "/proc/scsi",
                            "/sys/firmware"
                        ],
                        "ContainerIDFile": "",
                        "SecurityOpt": None,
                        "CapAdd": None,
                        "CpuCount": 0,
                        "DeviceCgroupRules": None,
                        "KernelMemoryTCP": 0,
                        "OomKillDisable": False,
                        "DeviceRequests": None,
                        "IOMaximumBandwidth": 0
                    },
                    "MountLabel": "",
                    "Id": "60aec879332b18e43681ae2e"
                }
            ]
        }
    }

    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = PluginToTest(_action_module, task_vars)

    result = plugin.run(args, None, None)

    assert result == expected_result


def test_run_no_filter(action_module):
    args = {
        'filter': {}
    }
    expected_result = [
        {
            "Platform": "linux",
            "State": {
                "Status": "running",
                "Pid": 5410,
                "OOMKilled": False,
                "Dead": False,
                "Paused": False,
                "Running": True,
                "FinishedAt": "2022-04-26T15:54:39.214694889Z",
                "Restarting": False,
                "Error": "",
                "StartedAt": "2022-04-26T15:54:45.981734261Z",
                "ExitCode": 0
            },
            "Config": {
                "Tty": False,
                "Hostname": "skydive01.novalocal",
                "Env": [
                    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                ],
                "Domainname": "",
                "StdinOnce": False,
                "Image": "skydive:v0.27.0",
                "Cmd": [
                    "analyzer",
                    "-c",
                    "/etc/skydive/skydive.yml"
                ],
                "WorkingDir": "",
                "Labels": {},
                "AttachStdin": False,
                "User": "",
                "Volumes": {
                    "/var/lib/skydive": {},
                    "/etc/skydive/skydive.yml": {}
                },
                "ExposedPorts": {
                    "8082/tcp": {}
                },
                "OnBuild": None,
                "AttachStderr": False,
                "Entrypoint": [
                    "/usr/local/bin/skydive"
                ],
                "AttachStdout": False,
                "OpenStdin": False
            },
            "HostsPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hosts",
            "Image": "sha256:b369c109fc2634db304c113cd9ae5386dcfdbee12a37abed3b0544a2a3e83d38",
            "Args": [
                "analyzer",
                "-c",
                "/etc/skydive/skydive.yml"
            ],
            "Driver": "overlay2",
            "Path": "/usr/local/bin/skydive",
            "HostnamePath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hostname",
            "RestartCount": 0,
            "Name": "/skydive-analyzer",
            "Created": "2022-02-21T11:57:10.201558481Z",
            "ExecIDs": None,
            "GraphDriver": {
                "Data": {
                    "LowerDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0-init/diff:"
                                "/var/lib/docker/overlay2/c3341d451baed12e57e850b43b2c6205849a00e"
                                "3697aa31c62872c74318c84c6/diff:/var/lib/docker/overlay2/7a056e9d"
                                "541e437c2baecb9469f65e25a5434cc1f6195c743ec27a0ce729f458/diff:"
                                "/var/lib/docker/overlay2/73c276c089c4c664867fac16d2b79904449b992"
                                "8bf8f2fdadb08743f4dcb0570/diff",
                    "WorkDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/work",
                    "MergedDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/merged",
                    "UpperDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/diff"
                },
                "Name": "overlay2"
            },
            "Mounts": [
                {
                    "RW": True,
                    "Source": "/etc/skydive/skydive.yml",
                    "Destination": "/etc/skydive/skydive.yml",
                    "Propagation": "rprivate",
                    "Mode": "rw",
                    "Type": "bind"
                },
                {
                    "RW": True,
                    "Source": "/var/lib/skydive",
                    "Destination": "/var/lib/skydive",
                    "Propagation": "rprivate",
                    "Mode": "rw",
                    "Type": "bind"
                }
            ],
            "ProcessLabel": "",
            "NetworkSettings": {
                "Bridge": "",
                "GlobalIPv6PrefixLen": 0,
                "LinkLocalIPv6Address": "",
                "HairpinMode": False,
                "IPAddress": "",
                "SecondaryIPAddresses": None,
                "SandboxID": "e4dcc47facee23c3ebc096c0f8113bfe13a1b7458afeb7bca9377f756cd52d2a",
                "SandboxKey": "/var/run/docker/netns/default",
                "GlobalIPv6Address": "",
                "Gateway": "",
                "LinkLocalIPv6PrefixLen": 0,
                "EndpointID": "",
                "SecondaryIPv6Addresses": None,
                "MacAddress": "",
                "IPPrefixLen": 0,
                "IPv6Gateway": "",
                "Networks": {
                    "host": {
                        "NetworkID": "efe5541c0d38ec7e32ddd9e836e96497f0dfddce03630245bb96032dadc1c5fe",
                        "MacAddress": "",
                        "GlobalIPv6PrefixLen": 0,
                        "Links": None,
                        "GlobalIPv6Address": "",
                        "IPAddress": "",
                        "Gateway": "",
                        "DriverOpts": None,
                        "IPPrefixLen": 0,
                        "EndpointID": "ba283edb832a5cee669fc1fcfcee56331ff46dea1cce4ad680fadb1434300039",
                        "IPv6Gateway": "",
                        "IPAMConfig": None,
                        "Aliases": None
                    }
                },
                "Ports": {}
            },
            "AppArmorProfile": "",
            "ResolvConfPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/resolv.conf",
            "LogPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/60aec879332b18e43681ae2e-json.log",
            "HostConfig": {
                "CpuPeriod": 0,
                "MemorySwappiness": None,
                "AutoRemove": False,
                "MemorySwap": 0,
                "PortBindings": None,
                "BlkioDeviceReadIOps": None,
                "Capabilities": None,
                "UsernsMode": "",
                "UTSMode": "",
                "ConsoleSize": [
                    0,
                    0
                ],
                "CpusetMems": "",
                "Dns": [],
                "Memory": 0,
                "PidsLimit": None,
                "CgroupParent": "",
                "Privileged": False,
                "IOMaximumIOps": 0,
                "LogConfig": {
                    "Type": "json-file",
                    "Config": {
                        "max-size": "20m",
                        "max-file": "1"
                    }
                },
                "NanoCpus": 0,
                "CpusetCpus": "",
                "PidMode": "",
                "DnsSearch": [],
                "BlkioWeight": 0,
                "RestartPolicy": {
                    "MaximumRetryCount": 0,
                    "Name": "unless-stopped"
                },
                "OomScoreAdj": 0,
                "BlkioDeviceReadBps": None,
                "VolumeDriver": "",
                "ReadonlyRootfs": False,
                "CpuShares": 0,
                "PublishAllPorts": False,
                "MemoryReservation": 0,
                "BlkioWeightDevice": None,
                "CpuPercent": 0,
                "NetworkMode": "host",
                "BlkioDeviceWriteBps": None,
                "Isolation": "",
                "GroupAdd": None,
                "ReadonlyPaths": [
                    "/proc/bus",
                    "/proc/fs",
                    "/proc/irq",
                    "/proc/sys",
                    "/proc/sysrq-trigger"
                ],
                "CpuRealtimeRuntime": 0,
                "Devices": None,
                "BlkioDeviceWriteIOps": None,
                "VolumesFrom": None,
                "Binds": [
                    "/var/lib/skydive/:/var/lib/skydive:rw",
                    "/etc/skydive/skydive.yml:/etc/skydive/skydive.yml:rw"
                ],
                "CpuQuota": 0,
                "KernelMemory": 0,
                "Cgroup": "",
                "ExtraHosts": None,
                "Runtime": "runc",
                "Ulimits": None,
                "CapDrop": None,
                "DnsOptions": [],
                "Links": None,
                "ShmSize": 67108864,
                "CpuRealtimePeriod": 0,
                "IpcMode": "private",
                "MaskedPaths": [
                    "/proc/asound",
                    "/proc/acpi",
                    "/proc/kcore",
                    "/proc/keys",
                    "/proc/latency_stats",
                    "/proc/timer_list",
                    "/proc/timer_stats",
                    "/proc/sched_debug",
                    "/proc/scsi",
                    "/sys/firmware"
                ],
                "ContainerIDFile": "",
                "SecurityOpt": None,
                "CapAdd": None,
                "CpuCount": 0,
                "DeviceCgroupRules": None,
                "KernelMemoryTCP": 0,
                "OomKillDisable": False,
                "DeviceRequests": None,
                "IOMaximumBandwidth": 0
            },
            "MountLabel": "",
            "Id": "60aec879332b18e43681ae2e"
        },
        {
            "Platform": "linux",
            "State": {
                "Status": "running",
                "Pid": 5411,
                "OOMKilled": False,
                "Dead": False,
                "Paused": False,
                "Running": True,
                "FinishedAt": "2022-04-26T15:54:39.214694889Z",
                "Restarting": False,
                "Error": "",
                "StartedAt": "2022-04-26T15:54:45.981734261Z",
                "ExitCode": 0
            },
            "Config": {
                "Tty": False,
                "Hostname": "skydive01.novalocal",
                "Env": [
                    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                ],
                "Domainname": "",
                "StdinOnce": False,
                "Image": "skydive:v0.28.0",
                "Cmd": [
                    "analyzer",
                    "-c",
                    "/etc/skydive/skydive.yml"
                ],
                "WorkingDir": "",
                "Labels": {},
                "AttachStdin": False,
                "User": "",
                "Volumes": {
                    "/var/lib/skydive": {},
                    "/etc/skydive/skydive.yml": {}
                },
                "ExposedPorts": {
                    "8082/tcp": {}
                },
                "OnBuild": None,
                "AttachStderr": False,
                "Entrypoint": [
                    "/usr/local/bin/skydive"
                ],
                "AttachStdout": False,
                "OpenStdin": False
            },
            "HostsPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hosts",
            "Image": "sha256:b369c109fc2634db304c113cd9ae5386dcfdbee12a37abed3b0544a2a3e83d38",
            "Args": [
                "analyzer",
                "-c",
                "/etc/skydive/skydive.yml"
            ],
            "Driver": "overlay2",
            "Path": "/usr/local/bin/skydive",
            "HostnamePath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hostname",
            "RestartCount": 0,
            "Name": "/skydive-analyzer",
            "Created": "2022-02-21T11:57:10.201558481Z",
            "ExecIDs": None,
            "GraphDriver": {
                "Data": {
                    "LowerDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0-init/diff:"
                                "/var/lib/docker/overlay2/c3341d451baed12e57e850b43b2c6205849a00e"
                                "3697aa31c62872c74318c84c6/diff:/var/lib/docker/overlay2/7a056e9d"
                                "541e437c2baecb9469f65e25a5434cc1f6195c743ec27a0ce729f458/diff:"
                                "/var/lib/docker/overlay2/73c276c089c4c664867fac16d2b79904449b992"
                                "8bf8f2fdadb08743f4dcb0570/diff",
                    "WorkDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/work",
                    "MergedDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/merged",
                    "UpperDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/diff"
                },
                "Name": "overlay2"
            },
            "Mounts": [
                {
                    "RW": True,
                    "Source": "/etc/skydive/skydive.yml",
                    "Destination": "/etc/skydive/skydive.yml",
                    "Propagation": "rprivate",
                    "Mode": "rw",
                    "Type": "bind"
                },
                {
                    "RW": True,
                    "Source": "/var/lib/skydive",
                    "Destination": "/var/lib/skydive",
                    "Propagation": "rprivate",
                    "Mode": "rw",
                    "Type": "bind"
                }
            ],
            "ProcessLabel": "",
            "NetworkSettings": {
                "Bridge": "",
                "GlobalIPv6PrefixLen": 0,
                "LinkLocalIPv6Address": "",
                "HairpinMode": False,
                "IPAddress": "",
                "SecondaryIPAddresses": None,
                "SandboxID": "e4dcc47facee23c3ebc096c0f8113bfe13a1b7458afeb7bca9377f756cd52d2a",
                "SandboxKey": "/var/run/docker/netns/default",
                "GlobalIPv6Address": "",
                "Gateway": "",
                "LinkLocalIPv6PrefixLen": 0,
                "EndpointID": "",
                "SecondaryIPv6Addresses": None,
                "MacAddress": "",
                "IPPrefixLen": 0,
                "IPv6Gateway": "",
                "Networks": {
                    "host": {
                        "NetworkID": "efe5541c0d38ec7e32ddd9e836e96497f0dfddce03630245bb96032dadc1c5fe",
                        "MacAddress": "",
                        "GlobalIPv6PrefixLen": 0,
                        "Links": None,
                        "GlobalIPv6Address": "",
                        "IPAddress": "",
                        "Gateway": "",
                        "DriverOpts": None,
                        "IPPrefixLen": 0,
                        "EndpointID": "ba283edb832a5cee669fc1fcfcee56331ff46dea1cce4ad680fadb1434300039",
                        "IPv6Gateway": "",
                        "IPAMConfig": None,
                        "Aliases": None
                    }
                },
                "Ports": {}
            },
            "AppArmorProfile": "",
            "ResolvConfPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/resolv.conf",
            "LogPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/60aec879332b18e43681ae2e-json.log",
            "HostConfig": {
                "CpuPeriod": 0,
                "MemorySwappiness": None,
                "AutoRemove": False,
                "MemorySwap": 0,
                "PortBindings": None,
                "BlkioDeviceReadIOps": None,
                "Capabilities": None,
                "UsernsMode": "",
                "UTSMode": "",
                "ConsoleSize": [
                    0,
                    0
                ],
                "CpusetMems": "",
                "Dns": [],
                "Memory": 0,
                "PidsLimit": None,
                "CgroupParent": "",
                "Privileged": False,
                "IOMaximumIOps": 0,
                "LogConfig": {
                    "Type": "json-file",
                    "Config": {
                        "max-size": "20m",
                        "max-file": "1"
                    }
                },
                "NanoCpus": 0,
                "CpusetCpus": "",
                "PidMode": "",
                "DnsSearch": [],
                "BlkioWeight": 0,
                "RestartPolicy": {
                    "MaximumRetryCount": 0,
                    "Name": "unless-stopped"
                },
                "OomScoreAdj": 0,
                "BlkioDeviceReadBps": None,
                "VolumeDriver": "",
                "ReadonlyRootfs": False,
                "CpuShares": 0,
                "PublishAllPorts": False,
                "MemoryReservation": 0,
                "BlkioWeightDevice": None,
                "CpuPercent": 0,
                "NetworkMode": "host",
                "BlkioDeviceWriteBps": None,
                "Isolation": "",
                "GroupAdd": None,
                "ReadonlyPaths": [
                    "/proc/bus",
                    "/proc/fs",
                    "/proc/irq",
                    "/proc/sys",
                    "/proc/sysrq-trigger"
                ],
                "CpuRealtimeRuntime": 0,
                "Devices": None,
                "BlkioDeviceWriteIOps": None,
                "VolumesFrom": None,
                "Binds": [
                    "/var/lib/skydive/:/var/lib/skydive:rw",
                    "/etc/skydive/skydive.yml:/etc/skydive/skydive.yml:rw"
                ],
                "CpuQuota": 0,
                "KernelMemory": 0,
                "Cgroup": "",
                "ExtraHosts": None,
                "Runtime": "runc",
                "Ulimits": None,
                "CapDrop": None,
                "DnsOptions": [],
                "Links": None,
                "ShmSize": 67108864,
                "CpuRealtimePeriod": 0,
                "IpcMode": "private",
                "MaskedPaths": [
                    "/proc/asound",
                    "/proc/acpi",
                    "/proc/kcore",
                    "/proc/keys",
                    "/proc/latency_stats",
                    "/proc/timer_list",
                    "/proc/timer_stats",
                    "/proc/sched_debug",
                    "/proc/scsi",
                    "/sys/firmware"
                ],
                "ContainerIDFile": "",
                "SecurityOpt": None,
                "CapAdd": None,
                "CpuCount": 0,
                "DeviceCgroupRules": None,
                "KernelMemoryTCP": 0,
                "OomKillDisable": False,
                "DeviceRequests": None,
                "IOMaximumBandwidth": 0
            },
            "MountLabel": "",
            "Id": "60aec879332b18e43681ae2e"
        },
        {
            "Platform": "linux",
            "State": {
                "Status": "running",
                "Pid": 5415,
                "OOMKilled": False,
                "Dead": False,
                "Paused": False,
                "Running": True,
                "FinishedAt": "2022-04-26T15:54:39.214694889Z",
                "Restarting": False,
                "Error": "",
                "StartedAt": "2022-04-26T15:54:45.981734261Z",
                "ExitCode": 0
            },
            "Config": {
                "Tty": False,
                "Hostname": "skydive01.novalocal",
                "Env": [
                    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                ],
                "Domainname": "",
                "StdinOnce": False,
                "Image": "skydive:v0.27.0",
                "Cmd": [
                    "analyzer",
                    "-c",
                    "/etc/skydive/skydive.yml"
                ],
                "WorkingDir": "",
                "Labels": {},
                "AttachStdin": False,
                "User": "",
                "Volumes": {
                    "/var/lib/skydive": {},
                    "/etc/skydive/skydive.yml": {}
                },
                "ExposedPorts": {
                    "8082/tcp": {}
                },
                "OnBuild": None,
                "AttachStderr": False,
                "Entrypoint": [
                    "/usr/local/bin/skydive"
                ],
                "AttachStdout": False,
                "OpenStdin": False
            },
            "HostsPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hosts",
            "Image": "sha256:b369c109fc2634db304c113cd9ae5386dcfdbee12a37abed3b0544a2a3e83d38",
            "Args": [
                "analyzer",
                "-c",
                "/etc/skydive/skydive.yml"
            ],
            "Driver": "overlay2",
            "Path": "/usr/local/bin/skydive",
            "HostnamePath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hostname",
            "RestartCount": 0,
            "Name": "/skydive-analyzer",
            "Created": "2022-02-21T11:57:10.201558481Z",
            "ExecIDs": None,
            "GraphDriver": {
                "Data": {
                    "LowerDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0-init/diff:"
                                "/var/lib/docker/overlay2/c3341d451baed12e57e850b43b2c6205849a00e"
                                "3697aa31c62872c74318c84c6/diff:/var/lib/docker/overlay2/7a056e9d"
                                "541e437c2baecb9469f65e25a5434cc1f6195c743ec27a0ce729f458/diff:"
                                "/var/lib/docker/overlay2/73c276c089c4c664867fac16d2b79904449b992"
                                "8bf8f2fdadb08743f4dcb0570/diff",
                    "WorkDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/work",
                    "MergedDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/merged",
                    "UpperDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/diff"
                },
                "Name": "overlay2"
            },
            "Mounts": [
                {
                    "RW": True,
                    "Source": "/etc/skydive/skydive.yml",
                    "Destination": "/etc/skydive/skydive.yml",
                    "Propagation": "rprivate",
                    "Mode": "rw",
                    "Type": "bind"
                },
                {
                    "RW": True,
                    "Source": "/var/lib/skydive",
                    "Destination": "/var/lib/skydive",
                    "Propagation": "rprivate",
                    "Mode": "rw",
                    "Type": "bind"
                }
            ],
            "ProcessLabel": "",
            "NetworkSettings": {
                "Bridge": "",
                "GlobalIPv6PrefixLen": 0,
                "LinkLocalIPv6Address": "",
                "HairpinMode": False,
                "IPAddress": "",
                "SecondaryIPAddresses": None,
                "SandboxID": "e4dcc47facee23c3ebc096c0f8113bfe13a1b7458afeb7bca9377f756cd52d2a",
                "SandboxKey": "/var/run/docker/netns/default",
                "GlobalIPv6Address": "",
                "Gateway": "",
                "LinkLocalIPv6PrefixLen": 0,
                "EndpointID": "",
                "SecondaryIPv6Addresses": None,
                "MacAddress": "",
                "IPPrefixLen": 0,
                "IPv6Gateway": "",
                "Networks": {
                    "host": {
                        "NetworkID": "efe5541c0d38ec7e32ddd9e836e96497f0dfddce03630245bb96032dadc1c5fe",
                        "MacAddress": "",
                        "GlobalIPv6PrefixLen": 0,
                        "Links": None,
                        "GlobalIPv6Address": "",
                        "IPAddress": "",
                        "Gateway": "",
                        "DriverOpts": None,
                        "IPPrefixLen": 0,
                        "EndpointID": "ba283edb832a5cee669fc1fcfcee56331ff46dea1cce4ad680fadb1434300039",
                        "IPv6Gateway": "",
                        "IPAMConfig": None,
                        "Aliases": None
                    }
                },
                "Ports": {}
            },
            "AppArmorProfile": "",
            "ResolvConfPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/resolv.conf",
            "LogPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/60aec879332b18e43681ae2e-json.log",
            "HostConfig": {
                "CpuPeriod": 0,
                "MemorySwappiness": None,
                "AutoRemove": False,
                "MemorySwap": 0,
                "PortBindings": None,
                "BlkioDeviceReadIOps": None,
                "Capabilities": None,
                "UsernsMode": "",
                "UTSMode": "",
                "ConsoleSize": [
                    0,
                    0
                ],
                "CpusetMems": "",
                "Dns": [],
                "Memory": 0,
                "PidsLimit": None,
                "CgroupParent": "",
                "Privileged": False,
                "IOMaximumIOps": 0,
                "LogConfig": {
                    "Type": "json-file",
                    "Config": {
                        "max-size": "20m",
                        "max-file": "1"
                    }
                },
                "NanoCpus": 0,
                "CpusetCpus": "",
                "PidMode": "",
                "DnsSearch": [],
                "BlkioWeight": 0,
                "RestartPolicy": {
                    "MaximumRetryCount": 0,
                    "Name": "unless-stopped"
                },
                "OomScoreAdj": 0,
                "BlkioDeviceReadBps": None,
                "VolumeDriver": "",
                "ReadonlyRootfs": False,
                "CpuShares": 0,
                "PublishAllPorts": False,
                "MemoryReservation": 0,
                "BlkioWeightDevice": None,
                "CpuPercent": 0,
                "NetworkMode": "host",
                "BlkioDeviceWriteBps": None,
                "Isolation": "",
                "GroupAdd": None,
                "ReadonlyPaths": [
                    "/proc/bus",
                    "/proc/fs",
                    "/proc/irq",
                    "/proc/sys",
                    "/proc/sysrq-trigger"
                ],
                "CpuRealtimeRuntime": 0,
                "Devices": None,
                "BlkioDeviceWriteIOps": None,
                "VolumesFrom": None,
                "Binds": [
                    "/var/lib/skydive/:/var/lib/skydive:rw",
                    "/etc/skydive/skydive.yml:/etc/skydive/skydive.yml:rw"
                ],
                "CpuQuota": 0,
                "KernelMemory": 0,
                "Cgroup": "",
                "ExtraHosts": None,
                "Runtime": "runc",
                "Ulimits": None,
                "CapDrop": None,
                "DnsOptions": [],
                "Links": None,
                "ShmSize": 67108864,
                "CpuRealtimePeriod": 0,
                "IpcMode": "private",
                "MaskedPaths": [
                    "/proc/asound",
                    "/proc/acpi",
                    "/proc/kcore",
                    "/proc/keys",
                    "/proc/latency_stats",
                    "/proc/timer_list",
                    "/proc/timer_stats",
                    "/proc/sched_debug",
                    "/proc/scsi",
                    "/sys/firmware"
                ],
                "ContainerIDFile": "",
                "SecurityOpt": None,
                "CapAdd": None,
                "CpuCount": 0,
                "DeviceCgroupRules": None,
                "KernelMemoryTCP": 0,
                "OomKillDisable": False,
                "DeviceRequests": None,
                "IOMaximumBandwidth": 0
            },
            "MountLabel": "",
            "Id": "60aec879332b18e43681ae2e"
        }
    ]
    task_vars = {
        "dockers": {
            "containers": [
                {
                    "Platform": "linux",
                    "State": {
                        "Status": "running",
                        "Pid": 5410,
                        "OOMKilled": False,
                        "Dead": False,
                        "Paused": False,
                        "Running": True,
                        "FinishedAt": "2022-04-26T15:54:39.214694889Z",
                        "Restarting": False,
                        "Error": "",
                        "StartedAt": "2022-04-26T15:54:45.981734261Z",
                        "ExitCode": 0
                    },
                    "Config": {
                        "Tty": False,
                        "Hostname": "skydive01.novalocal",
                        "Env": [
                            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                        ],
                        "Domainname": "",
                        "StdinOnce": False,
                        "Image": "skydive:v0.27.0",
                        "Cmd": [
                            "analyzer",
                            "-c",
                            "/etc/skydive/skydive.yml"
                        ],
                        "WorkingDir": "",
                        "Labels": {},
                        "AttachStdin": False,
                        "User": "",
                        "Volumes": {
                            "/var/lib/skydive": {},
                            "/etc/skydive/skydive.yml": {}
                        },
                        "ExposedPorts": {
                            "8082/tcp": {}
                        },
                        "OnBuild": None,
                        "AttachStderr": False,
                        "Entrypoint": [
                            "/usr/local/bin/skydive"
                        ],
                        "AttachStdout": False,
                        "OpenStdin": False
                    },
                    "HostsPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hosts",
                    "Image": "sha256:b369c109fc2634db304c113cd9ae5386dcfdbee12a37abed3b0544a2a3e83d38",
                    "Args": [
                        "analyzer",
                        "-c",
                        "/etc/skydive/skydive.yml"
                    ],
                    "Driver": "overlay2",
                    "Path": "/usr/local/bin/skydive",
                    "HostnamePath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hostname",
                    "RestartCount": 0,
                    "Name": "/skydive-analyzer",
                    "Created": "2022-02-21T11:57:10.201558481Z",
                    "ExecIDs": None,
                    "GraphDriver": {
                        "Data": {
                            "LowerDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0-init/diff:"
                                        "/var/lib/docker/overlay2/c3341d451baed12e57e850b43b2c6205849a00e"
                                        "3697aa31c62872c74318c84c6/diff:/var/lib/docker/overlay2/7a056e9d"
                                        "541e437c2baecb9469f65e25a5434cc1f6195c743ec27a0ce729f458/diff:"
                                        "/var/lib/docker/overlay2/73c276c089c4c664867fac16d2b79904449b992"
                                        "8bf8f2fdadb08743f4dcb0570/diff",
                            "WorkDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/work",
                            "MergedDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/merged",
                            "UpperDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/diff"
                        },
                        "Name": "overlay2"
                    },
                    "Mounts": [
                        {
                            "RW": True,
                            "Source": "/etc/skydive/skydive.yml",
                            "Destination": "/etc/skydive/skydive.yml",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        },
                        {
                            "RW": True,
                            "Source": "/var/lib/skydive",
                            "Destination": "/var/lib/skydive",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        }
                    ],
                    "ProcessLabel": "",
                    "NetworkSettings": {
                        "Bridge": "",
                        "GlobalIPv6PrefixLen": 0,
                        "LinkLocalIPv6Address": "",
                        "HairpinMode": False,
                        "IPAddress": "",
                        "SecondaryIPAddresses": None,
                        "SandboxID": "e4dcc47facee23c3ebc096c0f8113bfe13a1b7458afeb7bca9377f756cd52d2a",
                        "SandboxKey": "/var/run/docker/netns/default",
                        "GlobalIPv6Address": "",
                        "Gateway": "",
                        "LinkLocalIPv6PrefixLen": 0,
                        "EndpointID": "",
                        "SecondaryIPv6Addresses": None,
                        "MacAddress": "",
                        "IPPrefixLen": 0,
                        "IPv6Gateway": "",
                        "Networks": {
                            "host": {
                                "NetworkID": "efe5541c0d38ec7e32ddd9e836e96497f0dfddce03630245bb96032dadc1c5fe",
                                "MacAddress": "",
                                "GlobalIPv6PrefixLen": 0,
                                "Links": None,
                                "GlobalIPv6Address": "",
                                "IPAddress": "",
                                "Gateway": "",
                                "DriverOpts": None,
                                "IPPrefixLen": 0,
                                "EndpointID": "ba283edb832a5cee669fc1fcfcee56331ff46dea1cce4ad680fadb1434300039",
                                "IPv6Gateway": "",
                                "IPAMConfig": None,
                                "Aliases": None
                            }
                        },
                        "Ports": {}
                    },
                    "AppArmorProfile": "",
                    "ResolvConfPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/resolv.conf",
                    "LogPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/60aec879332b18e43681ae2e-json.log",
                    "HostConfig": {
                        "CpuPeriod": 0,
                        "MemorySwappiness": None,
                        "AutoRemove": False,
                        "MemorySwap": 0,
                        "PortBindings": None,
                        "BlkioDeviceReadIOps": None,
                        "Capabilities": None,
                        "UsernsMode": "",
                        "UTSMode": "",
                        "ConsoleSize": [
                            0,
                            0
                        ],
                        "CpusetMems": "",
                        "Dns": [],
                        "Memory": 0,
                        "PidsLimit": None,
                        "CgroupParent": "",
                        "Privileged": False,
                        "IOMaximumIOps": 0,
                        "LogConfig": {
                            "Type": "json-file",
                            "Config": {
                                "max-size": "20m",
                                "max-file": "1"
                            }
                        },
                        "NanoCpus": 0,
                        "CpusetCpus": "",
                        "PidMode": "",
                        "DnsSearch": [],
                        "BlkioWeight": 0,
                        "RestartPolicy": {
                            "MaximumRetryCount": 0,
                            "Name": "unless-stopped"
                        },
                        "OomScoreAdj": 0,
                        "BlkioDeviceReadBps": None,
                        "VolumeDriver": "",
                        "ReadonlyRootfs": False,
                        "CpuShares": 0,
                        "PublishAllPorts": False,
                        "MemoryReservation": 0,
                        "BlkioWeightDevice": None,
                        "CpuPercent": 0,
                        "NetworkMode": "host",
                        "BlkioDeviceWriteBps": None,
                        "Isolation": "",
                        "GroupAdd": None,
                        "ReadonlyPaths": [
                            "/proc/bus",
                            "/proc/fs",
                            "/proc/irq",
                            "/proc/sys",
                            "/proc/sysrq-trigger"
                        ],
                        "CpuRealtimeRuntime": 0,
                        "Devices": None,
                        "BlkioDeviceWriteIOps": None,
                        "VolumesFrom": None,
                        "Binds": [
                            "/var/lib/skydive/:/var/lib/skydive:rw",
                            "/etc/skydive/skydive.yml:/etc/skydive/skydive.yml:rw"
                        ],
                        "CpuQuota": 0,
                        "KernelMemory": 0,
                        "Cgroup": "",
                        "ExtraHosts": None,
                        "Runtime": "runc",
                        "Ulimits": None,
                        "CapDrop": None,
                        "DnsOptions": [],
                        "Links": None,
                        "ShmSize": 67108864,
                        "CpuRealtimePeriod": 0,
                        "IpcMode": "private",
                        "MaskedPaths": [
                            "/proc/asound",
                            "/proc/acpi",
                            "/proc/kcore",
                            "/proc/keys",
                            "/proc/latency_stats",
                            "/proc/timer_list",
                            "/proc/timer_stats",
                            "/proc/sched_debug",
                            "/proc/scsi",
                            "/sys/firmware"
                        ],
                        "ContainerIDFile": "",
                        "SecurityOpt": None,
                        "CapAdd": None,
                        "CpuCount": 0,
                        "DeviceCgroupRules": None,
                        "KernelMemoryTCP": 0,
                        "OomKillDisable": False,
                        "DeviceRequests": None,
                        "IOMaximumBandwidth": 0
                    },
                    "MountLabel": "",
                    "Id": "60aec879332b18e43681ae2e"
                },
                {
                    "Platform": "linux",
                    "State": {
                        "Status": "running",
                        "Pid": 5411,
                        "OOMKilled": False,
                        "Dead": False,
                        "Paused": False,
                        "Running": True,
                        "FinishedAt": "2022-04-26T15:54:39.214694889Z",
                        "Restarting": False,
                        "Error": "",
                        "StartedAt": "2022-04-26T15:54:45.981734261Z",
                        "ExitCode": 0
                    },
                    "Config": {
                        "Tty": False,
                        "Hostname": "skydive01.novalocal",
                        "Env": [
                            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                        ],
                        "Domainname": "",
                        "StdinOnce": False,
                        "Image": "skydive:v0.28.0",
                        "Cmd": [
                            "analyzer",
                            "-c",
                            "/etc/skydive/skydive.yml"
                        ],
                        "WorkingDir": "",
                        "Labels": {},
                        "AttachStdin": False,
                        "User": "",
                        "Volumes": {
                            "/var/lib/skydive": {},
                            "/etc/skydive/skydive.yml": {}
                        },
                        "ExposedPorts": {
                            "8082/tcp": {}
                        },
                        "OnBuild": None,
                        "AttachStderr": False,
                        "Entrypoint": [
                            "/usr/local/bin/skydive"
                        ],
                        "AttachStdout": False,
                        "OpenStdin": False
                    },
                    "HostsPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hosts",
                    "Image": "sha256:b369c109fc2634db304c113cd9ae5386dcfdbee12a37abed3b0544a2a3e83d38",
                    "Args": [
                        "analyzer",
                        "-c",
                        "/etc/skydive/skydive.yml"
                    ],
                    "Driver": "overlay2",
                    "Path": "/usr/local/bin/skydive",
                    "HostnamePath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hostname",
                    "RestartCount": 0,
                    "Name": "/skydive-analyzer",
                    "Created": "2022-02-21T11:57:10.201558481Z",
                    "ExecIDs": None,
                    "GraphDriver": {
                        "Data": {
                            "LowerDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0-init/diff:"
                                        "/var/lib/docker/overlay2/c3341d451baed12e57e850b43b2c6205849a00e"
                                        "3697aa31c62872c74318c84c6/diff:/var/lib/docker/overlay2/7a056e9d"
                                        "541e437c2baecb9469f65e25a5434cc1f6195c743ec27a0ce729f458/diff:"
                                        "/var/lib/docker/overlay2/73c276c089c4c664867fac16d2b79904449b992"
                                        "8bf8f2fdadb08743f4dcb0570/diff",
                            "WorkDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/work",
                            "MergedDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/merged",
                            "UpperDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/diff"
                        },
                        "Name": "overlay2"
                    },
                    "Mounts": [
                        {
                            "RW": True,
                            "Source": "/etc/skydive/skydive.yml",
                            "Destination": "/etc/skydive/skydive.yml",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        },
                        {
                            "RW": True,
                            "Source": "/var/lib/skydive",
                            "Destination": "/var/lib/skydive",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        }
                    ],
                    "ProcessLabel": "",
                    "NetworkSettings": {
                        "Bridge": "",
                        "GlobalIPv6PrefixLen": 0,
                        "LinkLocalIPv6Address": "",
                        "HairpinMode": False,
                        "IPAddress": "",
                        "SecondaryIPAddresses": None,
                        "SandboxID": "e4dcc47facee23c3ebc096c0f8113bfe13a1b7458afeb7bca9377f756cd52d2a",
                        "SandboxKey": "/var/run/docker/netns/default",
                        "GlobalIPv6Address": "",
                        "Gateway": "",
                        "LinkLocalIPv6PrefixLen": 0,
                        "EndpointID": "",
                        "SecondaryIPv6Addresses": None,
                        "MacAddress": "",
                        "IPPrefixLen": 0,
                        "IPv6Gateway": "",
                        "Networks": {
                            "host": {
                                "NetworkID": "efe5541c0d38ec7e32ddd9e836e96497f0dfddce03630245bb96032dadc1c5fe",
                                "MacAddress": "",
                                "GlobalIPv6PrefixLen": 0,
                                "Links": None,
                                "GlobalIPv6Address": "",
                                "IPAddress": "",
                                "Gateway": "",
                                "DriverOpts": None,
                                "IPPrefixLen": 0,
                                "EndpointID": "ba283edb832a5cee669fc1fcfcee56331ff46dea1cce4ad680fadb1434300039",
                                "IPv6Gateway": "",
                                "IPAMConfig": None,
                                "Aliases": None
                            }
                        },
                        "Ports": {}
                    },
                    "AppArmorProfile": "",
                    "ResolvConfPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/resolv.conf",
                    "LogPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/60aec879332b18e43681ae2e-json.log",
                    "HostConfig": {
                        "CpuPeriod": 0,
                        "MemorySwappiness": None,
                        "AutoRemove": False,
                        "MemorySwap": 0,
                        "PortBindings": None,
                        "BlkioDeviceReadIOps": None,
                        "Capabilities": None,
                        "UsernsMode": "",
                        "UTSMode": "",
                        "ConsoleSize": [
                            0,
                            0
                        ],
                        "CpusetMems": "",
                        "Dns": [],
                        "Memory": 0,
                        "PidsLimit": None,
                        "CgroupParent": "",
                        "Privileged": False,
                        "IOMaximumIOps": 0,
                        "LogConfig": {
                            "Type": "json-file",
                            "Config": {
                                "max-size": "20m",
                                "max-file": "1"
                            }
                        },
                        "NanoCpus": 0,
                        "CpusetCpus": "",
                        "PidMode": "",
                        "DnsSearch": [],
                        "BlkioWeight": 0,
                        "RestartPolicy": {
                            "MaximumRetryCount": 0,
                            "Name": "unless-stopped"
                        },
                        "OomScoreAdj": 0,
                        "BlkioDeviceReadBps": None,
                        "VolumeDriver": "",
                        "ReadonlyRootfs": False,
                        "CpuShares": 0,
                        "PublishAllPorts": False,
                        "MemoryReservation": 0,
                        "BlkioWeightDevice": None,
                        "CpuPercent": 0,
                        "NetworkMode": "host",
                        "BlkioDeviceWriteBps": None,
                        "Isolation": "",
                        "GroupAdd": None,
                        "ReadonlyPaths": [
                            "/proc/bus",
                            "/proc/fs",
                            "/proc/irq",
                            "/proc/sys",
                            "/proc/sysrq-trigger"
                        ],
                        "CpuRealtimeRuntime": 0,
                        "Devices": None,
                        "BlkioDeviceWriteIOps": None,
                        "VolumesFrom": None,
                        "Binds": [
                            "/var/lib/skydive/:/var/lib/skydive:rw",
                            "/etc/skydive/skydive.yml:/etc/skydive/skydive.yml:rw"
                        ],
                        "CpuQuota": 0,
                        "KernelMemory": 0,
                        "Cgroup": "",
                        "ExtraHosts": None,
                        "Runtime": "runc",
                        "Ulimits": None,
                        "CapDrop": None,
                        "DnsOptions": [],
                        "Links": None,
                        "ShmSize": 67108864,
                        "CpuRealtimePeriod": 0,
                        "IpcMode": "private",
                        "MaskedPaths": [
                            "/proc/asound",
                            "/proc/acpi",
                            "/proc/kcore",
                            "/proc/keys",
                            "/proc/latency_stats",
                            "/proc/timer_list",
                            "/proc/timer_stats",
                            "/proc/sched_debug",
                            "/proc/scsi",
                            "/sys/firmware"
                        ],
                        "ContainerIDFile": "",
                        "SecurityOpt": None,
                        "CapAdd": None,
                        "CpuCount": 0,
                        "DeviceCgroupRules": None,
                        "KernelMemoryTCP": 0,
                        "OomKillDisable": False,
                        "DeviceRequests": None,
                        "IOMaximumBandwidth": 0
                    },
                    "MountLabel": "",
                    "Id": "60aec879332b18e43681ae2e"
                },
                {
                    "Platform": "linux",
                    "State": {
                        "Status": "running",
                        "Pid": 5415,
                        "OOMKilled": False,
                        "Dead": False,
                        "Paused": False,
                        "Running": True,
                        "FinishedAt": "2022-04-26T15:54:39.214694889Z",
                        "Restarting": False,
                        "Error": "",
                        "StartedAt": "2022-04-26T15:54:45.981734261Z",
                        "ExitCode": 0
                    },
                    "Config": {
                        "Tty": False,
                        "Hostname": "skydive01.novalocal",
                        "Env": [
                            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                        ],
                        "Domainname": "",
                        "StdinOnce": False,
                        "Image": "skydive:v0.27.0",
                        "Cmd": [
                            "analyzer",
                            "-c",
                            "/etc/skydive/skydive.yml"
                        ],
                        "WorkingDir": "",
                        "Labels": {},
                        "AttachStdin": False,
                        "User": "",
                        "Volumes": {
                            "/var/lib/skydive": {},
                            "/etc/skydive/skydive.yml": {}
                        },
                        "ExposedPorts": {
                            "8082/tcp": {}
                        },
                        "OnBuild": None,
                        "AttachStderr": False,
                        "Entrypoint": [
                            "/usr/local/bin/skydive"
                        ],
                        "AttachStdout": False,
                        "OpenStdin": False
                    },
                    "HostsPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hosts",
                    "Image": "sha256:b369c109fc2634db304c113cd9ae5386dcfdbee12a37abed3b0544a2a3e83d38",
                    "Args": [
                        "analyzer",
                        "-c",
                        "/etc/skydive/skydive.yml"
                    ],
                    "Driver": "overlay2",
                    "Path": "/usr/local/bin/skydive",
                    "HostnamePath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/hostname",
                    "RestartCount": 0,
                    "Name": "/skydive-analyzer",
                    "Created": "2022-02-21T11:57:10.201558481Z",
                    "ExecIDs": None,
                    "GraphDriver": {
                        "Data": {
                            "LowerDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0-init/diff:"
                                        "/var/lib/docker/overlay2/c3341d451baed12e57e850b43b2c6205849a00e"
                                        "3697aa31c62872c74318c84c6/diff:/var/lib/docker/overlay2/7a056e9d"
                                        "541e437c2baecb9469f65e25a5434cc1f6195c743ec27a0ce729f458/diff:"
                                        "/var/lib/docker/overlay2/73c276c089c4c664867fac16d2b79904449b992"
                                        "8bf8f2fdadb08743f4dcb0570/diff",
                            "WorkDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/work",
                            "MergedDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/merged",
                            "UpperDir": "/var/lib/docker/overlay2/0921fa45079d79f5ecb9ef8670e0/diff"
                        },
                        "Name": "overlay2"
                    },
                    "Mounts": [
                        {
                            "RW": True,
                            "Source": "/etc/skydive/skydive.yml",
                            "Destination": "/etc/skydive/skydive.yml",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        },
                        {
                            "RW": True,
                            "Source": "/var/lib/skydive",
                            "Destination": "/var/lib/skydive",
                            "Propagation": "rprivate",
                            "Mode": "rw",
                            "Type": "bind"
                        }
                    ],
                    "ProcessLabel": "",
                    "NetworkSettings": {
                        "Bridge": "",
                        "GlobalIPv6PrefixLen": 0,
                        "LinkLocalIPv6Address": "",
                        "HairpinMode": False,
                        "IPAddress": "",
                        "SecondaryIPAddresses": None,
                        "SandboxID": "e4dcc47facee23c3ebc096c0f8113bfe13a1b7458afeb7bca9377f756cd52d2a",
                        "SandboxKey": "/var/run/docker/netns/default",
                        "GlobalIPv6Address": "",
                        "Gateway": "",
                        "LinkLocalIPv6PrefixLen": 0,
                        "EndpointID": "",
                        "SecondaryIPv6Addresses": None,
                        "MacAddress": "",
                        "IPPrefixLen": 0,
                        "IPv6Gateway": "",
                        "Networks": {
                            "host": {
                                "NetworkID": "efe5541c0d38ec7e32ddd9e836e96497f0dfddce03630245bb96032dadc1c5fe",
                                "MacAddress": "",
                                "GlobalIPv6PrefixLen": 0,
                                "Links": None,
                                "GlobalIPv6Address": "",
                                "IPAddress": "",
                                "Gateway": "",
                                "DriverOpts": None,
                                "IPPrefixLen": 0,
                                "EndpointID": "ba283edb832a5cee669fc1fcfcee56331ff46dea1cce4ad680fadb1434300039",
                                "IPv6Gateway": "",
                                "IPAMConfig": None,
                                "Aliases": None
                            }
                        },
                        "Ports": {}
                    },
                    "AppArmorProfile": "",
                    "ResolvConfPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/resolv.conf",
                    "LogPath": "/var/lib/docker/containers/60aec879332b18e43681ae2e/60aec879332b18e43681ae2e-json.log",
                    "HostConfig": {
                        "CpuPeriod": 0,
                        "MemorySwappiness": None,
                        "AutoRemove": False,
                        "MemorySwap": 0,
                        "PortBindings": None,
                        "BlkioDeviceReadIOps": None,
                        "Capabilities": None,
                        "UsernsMode": "",
                        "UTSMode": "",
                        "ConsoleSize": [
                            0,
                            0
                        ],
                        "CpusetMems": "",
                        "Dns": [],
                        "Memory": 0,
                        "PidsLimit": None,
                        "CgroupParent": "",
                        "Privileged": False,
                        "IOMaximumIOps": 0,
                        "LogConfig": {
                            "Type": "json-file",
                            "Config": {
                                "max-size": "20m",
                                "max-file": "1"
                            }
                        },
                        "NanoCpus": 0,
                        "CpusetCpus": "",
                        "PidMode": "",
                        "DnsSearch": [],
                        "BlkioWeight": 0,
                        "RestartPolicy": {
                            "MaximumRetryCount": 0,
                            "Name": "unless-stopped"
                        },
                        "OomScoreAdj": 0,
                        "BlkioDeviceReadBps": None,
                        "VolumeDriver": "",
                        "ReadonlyRootfs": False,
                        "CpuShares": 0,
                        "PublishAllPorts": False,
                        "MemoryReservation": 0,
                        "BlkioWeightDevice": None,
                        "CpuPercent": 0,
                        "NetworkMode": "host",
                        "BlkioDeviceWriteBps": None,
                        "Isolation": "",
                        "GroupAdd": None,
                        "ReadonlyPaths": [
                            "/proc/bus",
                            "/proc/fs",
                            "/proc/irq",
                            "/proc/sys",
                            "/proc/sysrq-trigger"
                        ],
                        "CpuRealtimeRuntime": 0,
                        "Devices": None,
                        "BlkioDeviceWriteIOps": None,
                        "VolumesFrom": None,
                        "Binds": [
                            "/var/lib/skydive/:/var/lib/skydive:rw",
                            "/etc/skydive/skydive.yml:/etc/skydive/skydive.yml:rw"
                        ],
                        "CpuQuota": 0,
                        "KernelMemory": 0,
                        "Cgroup": "",
                        "ExtraHosts": None,
                        "Runtime": "runc",
                        "Ulimits": None,
                        "CapDrop": None,
                        "DnsOptions": [],
                        "Links": None,
                        "ShmSize": 67108864,
                        "CpuRealtimePeriod": 0,
                        "IpcMode": "private",
                        "MaskedPaths": [
                            "/proc/asound",
                            "/proc/acpi",
                            "/proc/kcore",
                            "/proc/keys",
                            "/proc/latency_stats",
                            "/proc/timer_list",
                            "/proc/timer_stats",
                            "/proc/sched_debug",
                            "/proc/scsi",
                            "/sys/firmware"
                        ],
                        "ContainerIDFile": "",
                        "SecurityOpt": None,
                        "CapAdd": None,
                        "CpuCount": 0,
                        "DeviceCgroupRules": None,
                        "KernelMemoryTCP": 0,
                        "OomKillDisable": False,
                        "DeviceRequests": None,
                        "IOMaximumBandwidth": 0
                    },
                    "MountLabel": "",
                    "Id": "60aec879332b18e43681ae2e"
                }
            ]
        }
    }

    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = PluginToTest(_action_module, task_vars)

    result = plugin.run(args, None, None)

    assert result == expected_result
