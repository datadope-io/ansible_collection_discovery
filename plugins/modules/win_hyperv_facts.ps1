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
    virtual_machines = @()
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

function Get-SerialNumber {
    param (
        $vm_name
    )

    return Get-CimInstance -Namespace root\virtualization\v2 -class Msvm_VirtualSystemSettingData -Filter "ElementName = '$($vm_name)'" |
        Select-Object -ExpandProperty BIOSSerialNumber
}

# Get the hostname of the given ip address
function Get-Hostname {
    param (
        $address
    )

    $hostname = $null

    try {
        $hostname = [System.Net.Dns]::GetHostByAddress($address).Hostname
    }
    catch {
        $module.warn("Unable to get hostname for address $($address)")
    }

    return $hostname
}

try {
    # Retrieve the information of the processes
    Get-VM | ForEach-Object {
        $vm = @{
            id = $_.VMId
            name = $_.VMName
            serial = Get-SerialNumber $_.VMName
            hard_drives = @()
            hostname = $null
            network_adapters = @()
            path = $_.Path
            creation_time = Format-Date $_.CreationTime
            processor_count = $_.ProcessorCount
            memory = $_.MemoryStartup
            min_memory = $_.MemoryMinimum
            max_memory = $_.MemoryMaximum
            state = $_.State
            hypervisor = "Hyper-V"
        }

        $_ | Select-Object -ExpandProperty NetworkAdapters | ForEach-Object {
            $vm.network_adapters += @{
                name = $_.Name
                is_management_os = $_.IsManagementOs
                switch_name = $_.SwitchName
                mac_address = $_.MacAddress
                status = $_.Status
                ip_addresses = $_.IPAddresses
            }
        }

        try {
            Get-VHD -VMId $_.VMId | ForEach-Object {
                $hard_drive = @{
                    attached = $_.Attached
                    computer_name = $_.ComputerName
                    disk_identifier = $_.DiskIdentifier
                    file_size = $_.FileSize
                    minimum_size = $_.MinimumSize
                    parent_path = $_.ParentPath
                    path = $_.Path
                    size = $_.Size
                }

                if ($extended_data) {
                    $hard_drive += @{
                        address_abstraction_type = $_.AddressAbstractionType
                        alignment = $_.Alignment
                        block_size = $_.BlockSize
                        disk_number = $_.DiskNumber
                        fragmentation_percentage = $_.FragmentationPercentage
                        is_pmem_compatible = $_.IsPMEMCompatible
                        logical_sector_size = $_.LogicalSectorSize
                        number = $_.Number
                        physical_sector_size = $_.PhysicalSectorSize
                        vhd_format = $_.VhdFormat
                        vhd_type = $_.VhdType
                    }
                }

                $vm.hard_drives += $hard_drive
            }
        }
        catch {
            $module.warn("An error occurred gathering the information of a Hyper-V disk: $($_.Exception.Message)")
        }

        foreach ($network_adapter in $vm.network_adapters) {
            foreach ($ip_address in $network_adapter.ip_addresses) {
                $ip_hostname = Get-Hostname $ip_address
                if ($null -ne $ip_hostname) {
                    $vm.hostname = $ip_hostname
                    break
                }
            }
            if ($null -ne $vm.hostname) {
                break
            }
        }

        if ($extended_data) {
            $vm += @{
                parent_checkpoint_id = $_.ParentCheckpointId
                parent_checkpoint_name = $_.ParentCheckpointName
                checkpoint_file_location = $_.CheckpointFileLocation
                configuration_location = $_.ConfigurationLocation
                guest_state_path = $_.GuestStatePath
                smart_paging_file_in_use = $_.SmartPagingFileInUse
                smart_paging_file_path = $_.SmartPagingFilePath
                snapshop_file_location = $_.SnapshotFileLocation
                automatic_start_action = $_.AutomaticStartAction
                automatic_start_delay = $_.AutomaticStartDelay
                automatic_stop_action = $_.AutomaticStopAction
                automatic_critical_error_action = $_.AutomaticCriticalErrorAction
                automatic_critical_error_action_timeout = $_.AutomaticCriticalErrorActionTimeout
                automatic_checkpoints_enabled = $_.AutomaticCheckpointsEnabled
                cpu_usage = $_.CPUUsage
                memory_assigned = $_.MemoryAssigned
                memory_demand = $_.MemoryDemand
                memory_status = $_.MemoryStatus
                numa_aligned = $_.NumaAligned
                numa_nodes_count = $_.NumaNodesCount
                numa_socket_count = $_.NumaSocketCount
                heartbeat = $_.Heartbeat
                integration_services_state = $_.IntegrationServicesState
                integration_services_version = $_.IntegrationServicesVersion
                uptime = $_.Uptime
                operational_status = $_.OperationalStatus
                primary_operational_status = $_.PrimaryOperationalStatus
                secondary_operational_status = $_.SecondaryOperationalStatus
                status_descriptions = $_.StatusDescriptions
                primary_status_description = $_.PrimaryStatusDescription
                secondary_status_description = $_.SecondaryStatusDescription
                status = $_.Status
                replication_health = $_.ReplicationHealth
                replication_mode = $_.ReplicationMode
                replication_state = $_.ReplicationState
                resource_metering_enabled = $_.ResourceMeteringEnabled
                checkpoint_type = $_.CheckpointType
                enhanced_session_transport_type = $_.EnhancedSessionTransportType
                groups = $_.Groups
                version = $_.Version
                virtual_machine_type = $_.VirtualMachineType
                virtual_machine_sub_type = $_.VirtualMachineSubType
                guest_state_isolation_type = $_.GuestStateIsolationType
                notes = $_.Notes
                com_ports = $_.ComPorts
                dvd_drives = $_.DVDDrives
                fibre_channel_host_bus_adapters = $_.FibreChannelHostBusAdapters
                floppy_drive = $_.FloppyDrive
                remote_fx_adapter = $_.RemoteFxAdapter
                vm_integration_service = $_.VMIntegrationService
                dynamic_memory_enabled = $_.DynamicMemoryEnabled
                battery_passthrough_enabled = $_.BatteryPassthroughEnabled
                generation = $_.Generation
                is_clustered = $_.IsClustered
                parent_snapshot_id = $_.ParentSnapshotId
                parent_snapshot_name = $_.ParentSnapshotName
                size_of_system_files = $_.SizeOfSystemFiles
                guest_controlled_cache_types = $_.GuestControlledCacheTypes
                low_memory_mapped_io_space = $_.LowMemoryMappedIoSpace
                high_memory_mapped_io_space = $_.HighMemoryMappedIoSpace
                high_memory_mapped_io_base_address = $_.HighMemoryMappedIoBaseAddress
                lock_on_disconnect = $_.LockOnDisconnect
                computer_name = $_.ComputerName
                is_deleted = $_.IsDeleted
            }
        }

        $ansibleFacts.virtual_machines += $vm
    }
}
catch {
    $module.FailJson("An error occurred while retrieving Hyper-V information: $($_.Exception.Message)", $_)
}

$module.Result.ansible_facts = $ansibleFacts
$module.ExitJson()
