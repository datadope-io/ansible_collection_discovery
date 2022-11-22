# snmp_facts -- Add SNMP device info to ansible_facts.

## Synopsis

Provides information about a device through the SNMP protocol by providing a template with the OIDs configured.

## Parameters

### host (True, str, None)
Set to target SNMP server (normally C({{ inventory_hostname }})).

### port (False, int, 161)
SNMP UDP port number.

### timeout (False, int, 10)
Response timeout in seconds.

### retries (False, int, 1)
Maximum number of request retries, 1 retries means just a single request.

### version (True, str, None)
SNMP Version to use, C(v2), C(v2c) or C(v3).

Choices: ['v2c', 'v2', '2c', '2', 'v3', '3']

### community (False, str, None)
The SNMP community string, required if I(version) is C(v2c).

### security_level (False, str, None)
Authentication level, required if I(version) is C(v3).

Choices: [ noAuthnoPriv, authNoPriv, authPriv ]

### username (False, str, None)
Username for SNMPv3, required if I(version) is C(v3).

### integrity (False, str, None)
Hashing algorithm, required if I(version) is C(v3).

Choices: [ md5, sha ]

### authkey (False, str, None)
Authentication key, required if I(version) is C(v3).

### privacy (False, str, None)
Encryption algorithm, required if I(level) is C(authPriv).

Choices: [ aes, des ]

### privkey (False, str, None)
Encryption key, required if I(level) is C(authPriv).

### context_name (False, str, None)
Specifies an SNMP context by its name, a case-sensitive string of 1 to 32 characters.

### context_engine_id (False, str, None)
Unique SNMP Engine ID for the administrative domain.

### sysobject_ids (False, str, None)
Dictionary of template definitions by brand, model and device type for discovered sysObjectId.

If not defined, brand, model and device type will not be discovered.

Requires template_content if not defined.

### templates_path (False, str, None)
Path where template files are located.

## Template definition

### Scalar object
Defined a key with the name of the attribute, whose value is a dictionary specifying the OID to be queried and the optional post-processing to be applied to the obtained query response.

```yaml
example_template:
  sysDescr:
    oid: 1.3.6.1.2.1.1.1.0
    post_process: decode_hex
```

### Tabular object
Define a key with the name of the list to be queried, with a dictionary as its value specifying that it is of type list, the base OID to be queried, and a list of dictionaries defined in the same way as scalar objects.

The OID to be queried will be the concatenation of the base OID and the one specified for each entry if it starts with the character ".". Otherwise, the specified OID in the entry will be queried.

Optional post-processing can also be applied for each entry in a list.

```yaml
example_template:
  interfaces:
    type: list
    oid: 1.3.6.1.2.1.2.2.1
    entries:
      ifIndex:
        oid: "1.3.6.1.2.1.2.2.1.1"
      ifPhysAddress:
        oid: ".6"
        post_process: decode_mac
```

### Supported post-processed

* decode_hex: Decodes hexadecimal values.
* decode_mac: Decode the MAC if it starts with `x0`.
* lookup_adminstatus: Resolves the value associated with the numeric identifier for the ifAdminStatus object.
* lookup_operstatus: Resolves the value associated with the numeric identifier for the ifOperStatus object.

### Dependencies between tabular objects
Tabular objects can be related across different tables by their index. The generation of dependencies requires a prior study of the tables to be queried.

The following two cases are supported:
- Both tables share the same indices to relate attributes of the same entity (rows).
- One table indicates the relational indices of the rows in another table by querying an entry (columns).

The table on which a dependency is indicated will merge the attributes from the source table if their records share the same index.

The output from a source table can be omitted, as well as omitting the output of an attribute in the destination table.

#### - Tables with same index (type index):
```yaml
example_template:
  table01:
    type: list
    omit: true
    oid: 1.3.6.1.2.1.31.1.1.1
    entries:
      ifName:
        oid: ".1"
  table02:
    type: list
    dependencies:
      - table: table01
        index:
          type: index
    oid: 1.3.6.1.2.1.2.2.1
    entries:
      ifDescr:
        oid: ".2"
```
##### Output:
```json
{
  "snmp": {
    "table02": [
      {
        "ifName": "name_01",
        "ifDescr": "descr_01"
      },
      {
        "ifName": "name_02",
        "ifDescr": "descr_02"
      }]
   }
}
```

#### - Index table by entry (type value):
```yaml
example_template:
  table01:
    type: list
    omit: true
    oid: 1.3.6.1.2.1.2.2.1
    entries:
      ifPhysAddress:
        oid: ".6"
  table02:
    type: list
    dependencies:
      - table: table01
        index:
          type: value
          name: ipAdEntIfIndex
    oid: 1.3.6.1.2.1.4.20.1
    entries:
      ipAdEntAddr:
        oid: ".1"
      ipAdEntIfIndex:
        oid: ".2"
        omit: false
```
##### Output:
```json
{
  "snmp": {
    "table02": [
      {
        "ifPhysAddress": "physAddr_01",
        "ipAdEntAddr": "entAddr",
        "ipAdEntIfIndex": "01"
      },
      {
        "ifPhysAddress": "physAddr_02",
        "ipAdEntAddr": "entAddr",
        "ipAdEntIfIndex": "02"
      }]
   }
}
```

## Examples

```yaml
# Get SNMP device info
- name: Get SNMP device info
  datadope.discovery.snmp_facts: {}
```

## Return Values

### ansible_facts (always, dict)
Facts to add to ansible_facts by generic template:

* snmp (always, dict): Dict of device info.

  * sysDescr (always, str): A textual description of the entity.

  * sysObjectId (always, str): The vendor's authoritative identification of the network management subsystem contained in the entity.

  * sysUpTime (always, str): The time (in hundredths of a second) since the network management portion of the system was last re-initialized.

  * sysContact (always, str): The textual identification of the contact person for this managed node.

  * sysName (always, str): An administratively-assigned name for this managed node.

  * sysLocation (always, str): The physical location of this node.

  * interfaces (if available, list of dict):
          An entry containing management information applicable to a particular interface.

    * ifIndex (if available, str):
            A unique value, greater than zero, for each interface.

    * ifDescr (if available, str):
            A textual string containing information about the interface.

    * ifType (if available, str):
            The type of interface.

    * ifMtu (if available, str):
            The size of the largest packet which can be sent/received on the interface, specified in octets.

    * ifSpeed (if available, str):
            An estimate of the interface's current bandwidth in bits per second.

    * ifPhysAddress (if available, str):
            The interface's address at its protocol sub-layer. This object normally contains a MAC address.

    * ifAdminStatus (if available, str):
            The desired state of the interface.

    * ifOperStatus (if available, str):
            The current operational state of the interface.

  * if_mib (if available, list of dict):
          An entry containing additional management information applicable to a particular interface.

    * ifName (if available, str):
            The textual name of the interface.

    * ifHighSpeed (if available, str):
            An estimate of the interface's current bandwidth in units of 1,000,000 bits per second.

    * ifAlias (if available, str):
            This object is an 'alias' name for the interface as specified by a network manager.

  * ips (if available, list of dict):
          The addressing information for one of this entity's IPv4 addresses.

    * ipAdEntAddr (if available, str):
            The IPv4 address to which this entry's addressing information pertains.

    * ipAdEntIfIndex (if available, str):
            The index value which uniquely identifies the interface to which this entry is applicable.

    * ipAdEntNetMask (if available, str):
            The subnet mask associated with the IPv4 address of this entry.

  * serial_numbers (if available, list of dict):
          Information about a particular physical entity.

    * entPhysicalSerialNum (if available, str):
            The vendor-specific serial number string for the physical entity.

    * entPhysicalClass (if available, str):
            An indication of the general hardware type of the physical entity.

    * entPhysicalName (if available, str):
            The textual name of the physical entity.

# License

GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.

# Authors

- Datadope (@datadope-io)
