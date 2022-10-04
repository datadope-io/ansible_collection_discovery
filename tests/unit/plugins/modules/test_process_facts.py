from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible.module_utils.six import iteritems
from ansible.module_utils.six.moves import builtins  # noqa
from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import MagicMock, patch
import ansible_collections.datadope.discovery.plugins.modules.process_facts as module_to_test
from .conftest import AnsibleExitJson


def test_main(ansible_module_patch):
    ansible_module = ansible_module_patch(ansible_args={},
                                          argument_spec=module_to_test.argument_spec,
                                          supports_check_mode=True)
    expected_result = [{'pid': '1', 'ppid': '0', 'cmdline': '/sbin/launchd'},
                       {'pid': '317', 'ppid': '1', 'cmdline': '/usr/libexec/logd'},
                       {'pid': '318', 'ppid': '1', 'cmdline': '/usr/libexec/UserEventAgent (System)'}]
    with pytest.raises(AnsibleExitJson) as result:
        with patch.object(module_to_test, 'setup_module_object', return_value=ansible_module) as mock_setup:
            with patch.object(module_to_test, 'get_os_processes', return_value=expected_result) as mock_process:
                with patch.object(module_to_test, 'validate_parameters', return_value=None) as mock_validate:
                    module_to_test.main()
    mock_validate.assert_called_once_with({})
    mock_process.assert_called_once_with(module=ansible_module)
    mock_setup.assert_called_once_with()
    assert result.value.args[0]['changed'] is False
    assert result.value.args[0]['ansible_facts']['processes'] == expected_result


def test_setup_module_object(module_args):
    ansible_args = {}
    module_args(ansible_args)
    module = module_to_test.setup_module_object()
    assert module.argument_spec == module_to_test.argument_spec
    assert module.supports_check_mode
    assert len(module.params) == 0


def test_validate_parameters(ansible_module_patch):
    ansible_module = ansible_module_patch(ansible_args={},
                                          argument_spec=module_to_test.argument_spec,
                                          supports_check_mode=True)
    # TODO WHEN IMPLEMENTED
    # Fails if exception as function returns nothing
    assert module_to_test.validate_parameters(ansible_module.params) is None


def test_get_os_processes_check_mode_true():
    ansible_module_mock = MagicMock(spec=module_to_test.AnsibleModule)
    ansible_module_mock.check_mode = True
    assert module_to_test.get_os_processes(ansible_module_mock) is None


def test_main_check_mode_true(ansible_module_patch):
    ansible_module = ansible_module_patch(ansible_args={},
                                          argument_spec=module_to_test.argument_spec,
                                          supports_check_mode=True)
    ansible_module.check_mode = True
    expected_result = None
    with pytest.raises(AnsibleExitJson) as result:
        with patch.object(module_to_test, 'setup_module_object', return_value=ansible_module) as mock_setup:
            with patch.object(module_to_test, 'get_os_processes', return_value=expected_result) as mock_process:
                with patch.object(module_to_test, 'validate_parameters', return_value=None) as mock_validate:
                    module_to_test.main()
    mock_validate.assert_called_once_with({})
    mock_process.assert_called_once_with(module=ansible_module)
    mock_setup.assert_called_once_with()
    assert result.value.args[0]['changed'] is False
    assert 'processes' not in result.value.args[0]['ansible_facts']


@patch('ansible_collections.datadope.discovery.plugins.modules.process_facts.get_os_processes_default')
@pytest.mark.parametrize(
    argnames=('platform', 'expected_function'),
    argvalues=[
        ('aix', 'get_os_processes_aix_mock'),
        ('hp-ux', 'get_os_processes_hpux_mock'),
        ('linux', 'get_os_processes_default_mock'),
        ('other', 'get_os_processes_default_mock'),
    ]
)
def test_function_to_execute_for_platform(get_os_processes_default_mock, platform, expected_function):
    get_os_processes_aix_mock = MagicMock()
    get_os_processes_hpux_mock = MagicMock()
    ansible_module_mock = MagicMock(spec=module_to_test.AnsibleModule)
    ansible_module_mock.check_mode = False
    ansible_module_mock.params = {}
    with patch.dict(module_to_test._PROCESS_SPECIFIC_IMPLEMENTATIONS, {
        'hp-ux': get_os_processes_hpux_mock,
        'aix': get_os_processes_aix_mock
    }):
        with patch('sys.platform', platform):
            module_to_test.get_os_processes(ansible_module_mock)
    func = locals()[expected_function]
    func.assert_called_once_with(ansible_module_mock)
    for f_name, f in iteritems(locals()):
        if f_name.startswith('get_os_processes') and f != func:
            assert not f.called


@patch('os.listdir')
@patch.object(builtins, 'open')
def test_get_ps_processes_default(open_mock, listdir_mock):
    processes_info = {
        "1": (b'/bin/sh\x00-c\x00/usr/local/bin/process1.sh\x00parameter1_1\x00parameter1_2\x00',
              'Name:\tpython\nUmask:\t0022\nState:\tR (running)\nTgid:\t1\nNgid:\t0\nPid:\t1\nPPid:\t10\nTracerPid:\t0'
              '\nUid:\t0\t0\t0\t0\nGid:\t0\t0\t0\t0\nFDSize:\t64\nGroups:\t \nNStgid:\t1\nNSpid:\t1\nNSpgid:\t1\n'
              'NSsid:\t1\nVmPeak:\t    8684 kB\nVmSize:\t    8684 kB\nVmLck:\t       0 kB\nVmPin:\t       0 kB\n'
              'VmHWM:\t    6488 kB\nVmRSS:\t    6488 kB\nRssAnon:\t    2868 kB\nRssFile:\t    3620 kB\n'
              'RssShmem:\t       0 kB\nVmData:\t    3024 kB\nVmStk:\t     132 kB\nVmExe:\t       4 kB\n'
              'VmLib:\t    4600 kB\nVmPTE:\t      52 kB\nVmSwap:\t       0 kB\nHugetlbPages:\t       0 kB\n'
              'CoreDumping:\t0\nTHP_enabled:\t1\nThreads:\t1\nSigQ:\t0/31367\nSigPnd:\t0000000000000000\n'
              'ShdPnd:\t0000000000000000\nSigBlk:\t0000000000000000\nSigIgn:\t0000000001001000\n'
              'SigCgt:\t0000000188000002\nCapInh:\t00000000a80425fb\nCapPrm:\t00000000a80425fb\n'
              'CapEff:\t00000000a80425fb\nCapBnd:\t00000000a80425fb\nCapAmb:\t0000000000000000\nNoNewPrivs:\t0\n'
              'Seccomp:\t2\nSeccomp_filters:\t1\nSpeculation_Store_Bypass:\tvulnerable\nCpus_allowed:\t1f\n'
              'Cpus_allowed_list:\t0-4\nMems_allowed:\t1\nMems_allowed_list:\t0\nvoluntary_ctxt_switches:\t134\n'
              'nonvoluntary_ctxt_switches:\t11\n'),
        "2": (b'/bin/sh\x00-c\x00/usr/local/bin/process2.sh\x00parameter2_1\x00parameter2_2\x00',
              'Name:\tpython\nUmask:\t0022\nState:\tR (running)\nTgid:\t1\nNgid:\t0\nPid:\t1\nPPid:\t20\nTracerPid:\t0'
              '\nUid:\t0\t0\t0\t0\nGid:\t0\t0\t0\t0\nFDSize:\t64\nGroups:\t \nNStgid:\t1\nNSpid:\t1\nNSpgid:\t1\n'
              'NSsid:\t1\nVmPeak:\t    8684 kB\nVmSize:\t    8684 kB\nVmLck:\t       0 kB\nVmPin:\t       0 kB\n'
              'VmHWM:\t    6488 kB\nVmRSS:\t    6488 kB\nRssAnon:\t    2868 kB\nRssFile:\t    3620 kB\n'
              'RssShmem:\t       0 kB\nVmData:\t    3024 kB\nVmStk:\t     132 kB\nVmExe:\t       4 kB\n'
              'VmLib:\t    4600 kB\nVmPTE:\t      52 kB\nVmSwap:\t       0 kB\nHugetlbPages:\t       0 kB\n'
              'CoreDumping:\t0\nTHP_enabled:\t1\nThreads:\t1\nSigQ:\t0/31367\nSigPnd:\t0000000000000000\n'
              'ShdPnd:\t0000000000000000\nSigBlk:\t0000000000000000\nSigIgn:\t0000000001001000\n'
              'SigCgt:\t0000000188000002\nCapInh:\t00000000a80425fb\nCapPrm:\t00000000a80425fb\n'
              'CapEff:\t00000000a80425fb\nCapBnd:\t00000000a80425fb\nCapAmb:\t0000000000000000\nNoNewPrivs:\t0\n'
              'Seccomp:\t2\nSeccomp_filters:\t1\nSpeculation_Store_Bypass:\tvulnerable\nCpus_allowed:\t1f\n'
              'Cpus_allowed_list:\t0-4\nMems_allowed:\t1\nMems_allowed_list:\t0\nvoluntary_ctxt_switches:\t134\n'
              'nonvoluntary_ctxt_switches:\t11\n'),
        "3": (b'/bin/sh\x00-c\x00/usr/local/bin/process3.sh\x00parameter3_1\x00parameter3_2\x00ca\xc3\xb1\xc3\xb3n\x00',
              'Name:\tpython\nUmask:\t0022\nState:\tR (running)\nTgid:\t1\nNgid:\t0\nPid:\t1\nPPid:\t30\nTracerPid:\t0'
              '\nUid:\t0\t0\t0\t0\nGid:\t0\t0\t0\t0\nFDSize:\t64\nGroups:\t \nNStgid:\t1\nNSpid:\t1\nNSpgid:\t1\n'
              'NSsid:\t1\nVmPeak:\t    8684 kB\nVmSize:\t    8684 kB\nVmLck:\t       0 kB\nVmPin:\t       0 kB\n'
              'VmHWM:\t    6488 kB\nVmRSS:\t    6488 kB\nRssAnon:\t    2868 kB\nRssFile:\t    3620 kB\n'
              'RssShmem:\t       0 kB\nVmData:\t    3024 kB\nVmStk:\t     132 kB\nVmExe:\t       4 kB\n'
              'VmLib:\t    4600 kB\nVmPTE:\t      52 kB\nVmSwap:\t       0 kB\nHugetlbPages:\t       0 kB\n'
              'CoreDumping:\t0\nTHP_enabled:\t1\nThreads:\t1\nSigQ:\t0/31367\nSigPnd:\t0000000000000000\n'
              'ShdPnd:\t0000000000000000\nSigBlk:\t0000000000000000\nSigIgn:\t0000000001001000\n'
              'SigCgt:\t0000000188000002\nCapInh:\t00000000a80425fb\nCapPrm:\t00000000a80425fb\n'
              'CapEff:\t00000000a80425fb\nCapBnd:\t00000000a80425fb\nCapAmb:\t0000000000000000\nNoNewPrivs:\t0\n'
              'Seccomp:\t2\nSeccomp_filters:\t1\nSpeculation_Store_Bypass:\tvulnerable\nCpus_allowed:\t1f\n'
              'Cpus_allowed_list:\t0-4\nMems_allowed:\t1\nMems_allowed_list:\t0\nvoluntary_ctxt_switches:\t134\n'
              'nonvoluntary_ctxt_switches:\t11\n')
    }
    expected_result = [{'pid': x,
                        'ppid': str(10 * int(x)),
                        'user': 'root'}
                       for x, y in iteritems(processes_info)]
    expected_result[0]['cmdline'] = '/bin/sh -c /usr/local/bin/process1.sh parameter1_1 parameter1_2'
    expected_result[1]['cmdline'] = '/bin/sh -c /usr/local/bin/process2.sh parameter2_1 parameter2_2'
    expected_result[2]['cmdline'] = '/bin/sh -c /usr/local/bin/process3.sh parameter3_1 parameter3_2 cañón'
    requested_filenames = []
    stream_mocks = []

    class StreamMock(MagicMock):
        def __init__(self, *args, **kwargs):
            super(StreamMock, self).__init__(*args, **kwargs)
            self.filename = None
            self.status = 'open'

        def _read(self):
            assert self.status == 'open', 'file read before opening'
            self.status = 'read'
            filename = self.filename
            data = filename.rsplit('/')
            pid = data[-2]
            type_ = data[-1]
            index = 0 if type_ == 'cmdline' else 1
            return processes_info[pid][index]

        def _close(self):
            assert self.status == 'read', 'file closed without reading'
            self.status = 'closed'
            return

        def _exit(self, *args, **kwargs):  # noqa
            assert self.status == 'read', 'file closed without reading'
            self.status = 'closed'
            return True

    def _open(filename, *args, **kwargs):  # noqa
        assert filename not in requested_filenames
        requested_filenames.append(filename)
        stream_mock = StreamMock()
        stream_mock.filename = filename
        stream_mock.read.side_effect = stream_mock._read  # Case no context manager is used
        stream_mock.close.side_effect = stream_mock._close
        stream_mock.__enter__.return_value.read.side_effect = stream_mock._read  # Case context manager is used
        stream_mock.__exit__.side_effect = stream_mock._exit
        stream_mocks.append(stream_mock)
        return stream_mock

    listdir_mock.return_value = list(processes_info.keys()) + ["other"]
    open_mock.side_effect = _open
    expected_open_calls = [('/proc/{0}/cmdline'.format(x), 'rb') for x in processes_info]
    expected_open_calls += [('/proc/{0}/status'.format(x),) for x in processes_info]
    result = module_to_test.get_os_processes_default(None)
    listdir_mock.assert_called_once_with('/proc')
    expected_open_files = len(processes_info) * 2
    assert open_mock.call_count == expected_open_files
    assert len(stream_mocks) == expected_open_files
    for expected_open_call in expected_open_calls:
        open_mock.assert_any_call(*expected_open_call)
    for mock in stream_mocks:
        assert mock.status == 'closed', 'found unclosed stream'
    assert result == expected_result


def test_get_ps_processes_hpux_nok():
    ansible_module_mock = MagicMock(spec=module_to_test.AnsibleModule)
    ansible_module_mock.run_command.return_value = (1, None, None)
    result = module_to_test.get_os_processes_hpux(ansible_module_mock)
    assert result == []


def test_get_ps_processes_hpux_ok():
    ps_command_stdout = """    1     0     root     /sbin/launchd
    317     1     root     /usr/libexec/logd
    318     1     root     /usr/libexec/UserEventAgent (System)
    """
    expected_result = [{'pid': '1', 'ppid': '0', 'user': 'root', 'cmdline': '/sbin/launchd'},
                       {'pid': '317', 'ppid': '1', 'user': 'root', 'cmdline': '/usr/libexec/logd'},
                       {'pid': '318', 'ppid': '1', 'user': 'root', 'cmdline': '/usr/libexec/UserEventAgent (System)'}]

    ansible_module_mock = MagicMock(spec=module_to_test.AnsibleModule)
    ansible_module_mock.run_command.return_value = (0, ps_command_stdout, "")
    result = module_to_test.get_os_processes_hpux(ansible_module_mock)
    assert result == expected_result


def test_get_ps_processes_aix_nok():
    ansible_module_mock = MagicMock(spec=module_to_test.AnsibleModule)
    ansible_module_mock.run_command.return_value = (1, None, None)
    result = module_to_test.get_os_processes_aix(ansible_module_mock)
    assert result == []


def test_get_ps_processes_aix_ok():
    ps_command_stdout = """    1     0     root     /sbin/launchd
    317     1     root     /usr/libexec/logd
    318     1     root     /usr/libexec/UserEventAgent (System)
    """
    expected_result = [{'pid': '1', 'ppid': '0', 'user': 'root', 'cmdline': '/sbin/launchd'},
                       {'pid': '317', 'ppid': '1', 'user': 'root', 'cmdline': '/usr/libexec/logd'},
                       {'pid': '318', 'ppid': '1', 'user': 'root', 'cmdline': '/usr/libexec/UserEventAgent (System)'}]

    ansible_module_mock = MagicMock(spec=module_to_test.AnsibleModule)
    ansible_module_mock.run_command.return_value = (0, ps_command_stdout, "")
    result = module_to_test.get_os_processes_aix(ansible_module_mock)
    assert result == expected_result
