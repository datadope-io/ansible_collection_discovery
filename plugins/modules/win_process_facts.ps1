#!powershell

# Copyright: (c) 2022, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic

$spec = @{
    options = @{
        date_format = @{ type = 'str'; default = '%c' }
        extended_data = @{ type = 'bool'; default = $false }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$date_format = $module.Params.date_format
$extended_data = $module.Params.extended_data

# Structure of the response the script will return
$ansibleFacts = @{
    processes = @()
}

# Format the given date with the given format (or Date and time - abbreviated by default)
function Format-Date {
    param (
        $date
    )

    if ($null -ne $date) {
        $date = Get-Date $date -UFormat $date_format
    }

    return $date
}

# Get the owner of the given process
function Get-Owner {
    param (
        $process
    )

    $owner = $null

    try {
        $process_owner = Invoke-CimMethod -InputObject $process -MethodName GetOwner
        if ($null -ne $process_owner.User -and $null -ne $process_owner.Domain) {
            $owner = $process_owner.Domain + '\' + $process_owner.User
        }
    }
    catch {
        $module.warn("Unable to gather owner for process $($process.ProcessId): $($_.Exception.Message)")
    }

    return $owner
}

try {
    # Retrieve the information of the processes
    Get-CimInstance -ClassName Win32_Process | ForEach-Object {
        $process_data = @{
            cmdline = $_.CommandLine
            pid = $_.ProcessId.ToString()
            ppid = $_.ParentProcessId.ToString()
            user = Get-Owner $_
        }

        if ($extended_data) {
            $process_data += @{
                cs_creation_class_name = $_.CSCreationClassName
                cs_name = $_.CSName
                caption = $_.Caption
                creation_class_name = $_.CreationClassName
                creation_date = Format-Date $_.CreationDate
                description = $_.Description
                executable_path = $_.ExecutablePath
                execution_state = $_.ExecutionState
                handle = $_.Handle
                handle_count = $_.HandleCount
                handles = $_.Handles
                install_date = Format-Date $_.InstallDate
                kernel_mode_time = $_.KernelModeTime
                maximum_working_set_size = $_.MaximumWorkingSetSize
                minimum_working_set_size = $_.MinimumWorkingSetSize
                name = $_.Name
                os_creation_class_name = $_.OSCreationClassName
                os_name = $_.OSName
                other_operation_count = $_.OtherOperationCount
                other_transfer_count = $_.OtherTransferCount
                ps_computer_name = $_.PSComputerName
                page_faults = $_.PageFaults
                page_file_usage = $_.PageFileUsage
                path = $_.Path
                peak_page_file_usage = $_.PeakPageFileUsage
                peak_virtual_size = $_.PeakVirtualSize
                peak_working_set_size = $_.PeakWorkingSetSize
                priority = $_.Priority
                private_page_count = $_.PrivatePageCount
                process_name = $_.ProcessName
                quota_non_paged_pool_usage = $_.QuotaNonPagedPoolUsage
                quota_paged_pool_usage = $_.QuotaPagedPoolUsage
                quota_peak_non_paged_pool_usage = $_.QuotaPeakNonPagedPoolUsage
                quota_peak_paged_pool_usage = $_.QuotaPeakPagedPoolUsage
                read_operation_count = $_.ReadOperationCount
                read_transfer_count = $_.ReadTransferCount
                session_id = $_.SessionId
                status = $_.Status
                termination_date = Format-Date $_.TerminationDate
                thread_count = $_.ThreadCount
                user_mode_time = $_.UserModeTime
                vm = $_.VM
                virtual_size = $_.VirtualSize
                ws = $_.WS
                windows_version = $_.WindowsVersion
                working_set_size = $_.WorkingSetSize
                write_operation_count = $_.WriteOperationCount
                write_transfer_count = $_.WriteTransferCount
            }
        }

        $ansibleFacts.processes += $process_data
    }
}
catch {
    $module.FailJson("An error occurred while retrieving process facts: $($_.Exception.Message)", $_)
}

$module.Result.ansible_facts = $ansibleFacts
$module.ExitJson()
