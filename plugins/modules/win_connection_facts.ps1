#!powershell

# Copyright: (c) 2024, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic

$spec = @{
    options = @{}
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$ansibleFacts = @{
    connections = @()
}

function Get-GroupedConnectionsByProcess {
    param (
        $connections,
        $processes
    )

    $grouped_connections = @{}

    foreach ($connection in $connections) {
        # Check if the process died between connection and process gathering
        if ($processes.ContainsKey($connection.pid)) {
            $process = $processes[$connection.pid]
        }
        else {
            continue
        }

        if (-not $grouped_connections.ContainsKey($connection.pid)) {
            $grouped_connections[$connection.pid] = @{
                'conn' = @()
                'listen' = @()
                'meta' = @{
                    'cmdline' = $process.cmdline
                    'host' = $process.hostname.ToLower()
                    'process_name' = $process.exe
                }
            }
        }

        if ($connection['conn']) {
            $grouped_connections[$connection.pid].conn += $connection.conn
        }

        if ($connection['listen']) {
            $grouped_connections[$connection.pid].listen += $connection.listen
        }
    }

    return $grouped_connections.Values
}

function Get-ProcessData {
    $processes = @{}
    $hostname = (Get-CimInstance -ClassName Win32_ComputerSystem).Name

    foreach ($process in Get-CimInstance -ClassName Win32_Process) {
        $cmdline = $process.CommandLine
        $exe = $process.ExecutablePath

        # Ignore processes without valid data
        if ($null -eq $cmdline -or $null -eq $exe) {
            continue
        }

        $processes[$process.ProcessId.ToString()] = @{
            cmdline = $cmdline
            exe = (Get-Item $exe).BaseName
            hostname = $hostname
        }
    }

    return $processes
}

function Get-ActiveConnection {
    $connections = @()

    $stateMap = @{
        1 = 'CLOSED'
        2 = 'LISTEN'
        3 = 'SYN_SENT'
        4 = 'SYN_RECV'
        5 = 'ESTABLISHED'
        6 = 'FIN_WAIT1'
        7 = 'FIN_WAIT2'
        8 = 'CLOSE_WAIT'
        9 = 'CLOSING'
        10 = 'LAST_ACK'
        11 = 'TIME_WAIT'
        12 = 'DELETE_TCB'
        100 = 'BOUND'
        0 = 'NONE'
    }

    foreach ($conn in Get-NetTCPConnection) {
        $connections += @{
            pid = [string]$conn.OwningProcess
            status = $stateMap[[int]$conn.State]
            listen = if ($conn.LocalPort -ne 0) { "$($conn.LocalAddress):$($conn.LocalPort)" } else { '' }
            conn = if ($conn.RemotePort -ne 0) { "$($conn.RemoteAddress):$($conn.RemotePort)" } else { '' }
        }
    }

    return $connections
}

try {
    $connections = Get-ActiveConnection
    $processes = Get-ProcessData

    $ansibleFacts.connections = Get-GroupedConnectionsByProcess $connections $processes
}
catch {
    $module.FailJson("An error occurred while retrieving information: $($_.Exception.Message)", $_)
}

$module.Result.ansible_facts = $ansibleFacts
$module.ExitJson()
