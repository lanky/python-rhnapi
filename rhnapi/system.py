#!/usr/bin/env python
# -*- coding: utf-8 -*-
# and abstraction of the "system" namespace
# from the RHN API for satellite 5.1.0
# used to manipulate registered systems

# all these methods require an RHN session, from rhnapi
# (import rhnapi will do this for you)

# global translations if required:

ent_names = { 'monitoring_entitled'              : 'monitoring',
              'provisioning_entitled'            : 'provisioning',
              'management_entitled'              : 'management',
              'virtualization_platform_entitled' : 'virtualization platform',
              'virtualization_host_entitled'     : 'virtualization',
            }

# --------------------------------------------------------------------------------- #

def addEntitlements(rhn, server_id, ent_list):
    """
    API: system.addEntitlements

    usage: addEntitlements(rhn, server_id, ent_list)

    description:
    Adds the list of entitlements to a given server ID

    returns:
    Bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID to add entitlements to
    entsList(list/str)       - a list of entitlement labels to add
                               entitlements that already exist are ignored.
    """
    try:
        return rhn.session.system.addEntitlements(rhn.key, server_id, ent_list) == 1
    except Exception, E:
        return rhn.fail(E, "add entitlements %s to server ID %d (%s)" % (','.join(entslist) , server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def addNote(rhn, server_id, note):
    """
    API: system.addNote

    usage: addNote(rhn, server_id, note)

    Add a note to an existing server_id

    returns: 
    Bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID
    note(str)                - the note to add
    """
    try:
        return rhn.session.system.addNote(rhn.key, server_id, note) == 1
    except Exception, E:
        return rhn.fail(E, "add note to server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def applyErrata(rhn, server_id, errata):
    """
    API: system.applyErrata

    usage: applyErrata(rhn, server_id, errata)

    Applies the specifed list of errata to a server

    returns:
    Bool, or throws exception

    parameters:
    rhn                       - an authenticated RHN session
    server_id(int)            - server ID
    errata(list/int)          - list of erratum IDs to apply
    """
    try:
        return rhn.session.system.applyErrata(rhn.key, server_id, errataList) == 1
    except Exception, E:
        return rhn.fail(E, "apply errata to server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def comparePackages(rhn, server_id1, server_id2):
    """
    API: system.comparePackages

    usage: comparePackages(rhn, server_id1, server_id2)

    description:
    Compares installed package lists on 2 servers

    returns: list of dict, one per package
            { 'package_name_id' : int
              'package_name' : strs
              'this_system' : str (version on server1)
              'other_system' : str (version on server2)
              'comparison' : int }
        where the comparison integer means:
            * 0 - No difference.
            * 1 - Package on this system only.
            * 2 - Newer package version on this system.
            * 3 - Package on other system only.
            * 4 - Newer package version on other system.

    parameters:
    rhn                  - an authenticated RHN session
    server_id1(int)      - server ID
    second_id2(int)      - server ID
    """
    try:
        return rhn.session.system.comparePackages(rhn.key, server_id1, server_id2)
    except Exception, E:
        return rhn.fail(E, "compare packages on servers %d (%s) and %d (%s)" % (server_id1, getServerName(rhn, server_id1), server_id2, getServerName(rhn, server_id2)))

# --------------------------------------------------------------------------------- #

def comparePackageProfile(rhn, server_id, profile_label):
    """
    API: system.comparePackageProfile
    
    usage: comparePackageProfile(rhn, server_id, profile_label)
    
    description:
    Compares a system's package list against a saved package profile.
    
    returns: list of dict, one per package
            { 'package_name_id' : int
              'package_name' : strs
              'this_system' : str (version on specified system)
              'other_system' : str (version in package profile)
              'comparison' : int }
        where the comparison integer means:
            * 0 - No difference.
            * 1 - Package on this system only.
            * 2 - Newer package version on this system.
            * 3 - Package on other system only.
            * 4 - Newer package version on other system.

    returns: list of dict, one per package (for the union of all pkgs on system
    and in profile)
    
    parameters:
    rhn                  - an authenticated RHN session
    server_id(int)       - server ID
    profile_label(str)   - label of a saved package profile
    """
    try:
        return rhn.session.system.comparePackageProfile(rhn.key, server_id, profile_label)
    except Exception, E:
        return rhn.fail(E, 'compare packages on server %d (%s) to package profile %s' % (server_id, getServerName(rhn, server_id), profile_label))

# --------------------------------------------------------------------------------- #

def convertToFlexEntitlement(rhn, system_list, chan_family):
    """
    API: system.convertToFlexEntitlement

    usage: convertToFlexEntitlement(rhn, system_list, chan_label)

    description:
    Converts the given list of systems for a given channel family to use
    the flex entitlement.

    returns:
    int (number of converted systems)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    system_list(list/int)    - list of system ID numbers
    chan_family(str)          - channel family label
    """
    try:
        return rhn.session.system.convertToFlexEntitlement(rhn.key, system_list, chan_family)
    except Exception, E:
        return rhn.fail(E, 'convert systems to use flex entitlement for channel family %s' % chan_family)

# --------------------------------------------------------------------------------- #

def createPackageProfile(rhn, server_id, label, description):
    """
    API: system.createPackageProfile

    usage: createPackageProfile(rhn, server_id, label, description)

    description:
    Create a new package profile for a given server_id.
    parameters:
    rhn                   - an authenticated RHN session
    server_id(int)        - server ID number
    label(str)            - label for new package profile
    description(str)      - a description of the profile
    """
    try:
        rhn.session.system.createPackageProfile(rhn.key, server_id, label, description)
    except Exception, E:
        return rhn.fail(E, "create package profile %s for server_id %d (%s)" % (label, server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def createSystemRecord(rhn, server_id, kslabel):
    """
    API: system.createSystemRecord
    
    usage: createSystemRecord(rhn, server_id, kslabel)
    
    description:
    Creates a cobbler system record with the specified kickstart label
    
    returns: True, or throws exception
    
    parameters:
    rhn                  - an authenticated RHN session
    server_id(int)       - server ID
    """
    try:
        return rhn.session.system.createSystemRecord(rhn.key, server_id, kslabel) == 1
    except Exception, E:
        return rhn.fail(E, 'create cobbler system record for server ID %d (%s)' % (server_id, getSystemName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def deleteCustomValues(rhn, server_id, label_list):
    """
    API: system.deleteCustomValues
                  
    usage: deleteCustomValues(rhn, server_id, label_list)
                  
    description:
    delete the given custom values from the chosen system record.
                  
    returns: True, or throws exception
                  
    parameters:
    rhn                  - an authenticated RHN session
    server_id(int)       - server ID
    label_list(list/str) - custom value name/label (or list of)
    """
    if not isinstance(label_list, list):
        label_list = [ label_list ]
    try:
        return rhn.session.system.deleteCustomValues(rhn.key, server_id, label_list) == 1
    except Exception, E:
        return rhn.fail(E, 'delete one or more of custom values [%s] from server ID %d (%s)' % (','.join(label_list), server_id, getSystemName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def deleteNote(rhn, server_id, note_id):
    """
    API: system.deleteNote
            
    usage: deleteNote(rhn, server_id, note_id)
            
    description:
    deletes the given note from the specified server record
    
    returns: True, or throws exception
            
    parameters:
    rhn                  - an authenticated RHN session
    server_id(int)       - server ID
    note_id(int)         - note ID
    """
    try:
        return rhn.session.system.deleteNote(rhn.key, server_id, note_id) == 1
    except Exception, E:
        return rhn.fail(E, 'delete note %d from server %d (%s)' % (note_id, server_id, getSystemName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def deleteNotes(rhn, server_id):
    """
    API: system.deleteNotes
        
    usage: deleteNotes(rhn, server_id)
        
    description:
    deletes ALL notes from the given server record
            
    returns: True, or throws exception 
        
    parameters:
    rhn                  - an authenticated RHN session
    server_id            - server ID
    """
    try:
        return rhn.session.system.deleteNotes(rhn, server_id) == 1
    except Exception, E:
        return rhn.fail(E, 'delete all notes from server id %d (%s)' % (server_id, getSystemName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def deletePackageProfile(rhn, profile_id):
    """
    API: system.deletePackageProfile
        
    usage: deletePackageProfile(rhn, profile_id)
        
    description:
    delete the specified package profile
        
    returns: True, or throws exception
        
    parameters:
    rhn                  - an authenticated RHN session
    profile_id(int)      - saved package profile ID
    """
    try:
        return rhn.session.system.deletePackageProfile(rhn, profile_id) == 1
    except Exception, E:
        return rhn.fail(E, 'delete package profile ID %d' % profile_id)


# --------------------------------------------------------------------------------- #

def deleteSystem(server_cert):
    """
    API: system.deleteSystem
    
    usage: deleteSystem(rhn, server_cert)
    
    description:
    Delete an individual system using its client certificate.
    Does not require an RHN session, so can be used directly from the client system
    This is often used for re-registering a server after installation.
    
    returns: True, or throws exception
    
    parameters:
    server_cert(str)         - the server certificate (/etc/sysconfig/rhn/systemid) content (not path)
    """
    try:
        return rhn.session.system.deleteSystems(rhn.key, server_cert) == 1
    except Exception, E:
        return rhn.fail(E, "delete the following server: %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def deleteSystems(rhn, system_list):
    """
    API: system.deleteSystems
    
    usage: deleteSystems(rhn, system_list)
    
    description:
    Delete systems given a list of system ids
    
    parameters:
    rhn                      - an authenticated RHN session
    system_list([int])        - list of server_ids
    """
    try:
        return rhn.session.system.deleteSystems(rhn.key, systemlist) == 1
    except Exception, E:
        return rhn.fail(E, "delete one or more of systems: [ %s ]" % (",".join([ str(x) for x in systemlist ])))


# --------------------------------------------------------------------------------- #

def downloadSystemId(rhn, server_id):
    """
    API: system.downloadSystemId
    
    usage: downloadSystemId(rhn, server_id)
        
    description:
    downloads the server_id file (/etc/sysconfig/rhn/systemid) for a given server_id.
    
    returns: string (contents of systemid file)
    
    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID number
    """
    try:
        rhn.session.system.downloadSystemId(rhn.key, ServerID)
    except Exception, E:
        return rhn.fail(E, "download the server_id for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getBaseChannel(rhn, server_id):
    """
    API: none, special case of system.getSubscribedBaseChannel

    usage: getBaseChannel(rhn, server_id)
    
    description:
    returns the label of the given system's base channel
    
    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getSubscribedBaseChannel(rhn.key, server_id)['label']
    except Exception, E:
        return rhn.fail(E, "retrieve Subscribed Base Channel information for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getConnectionPath(rhn, server_id):
    """
    API: system.getConnectionPath
        
    usage: getConnectionPath(rhn, server_id)
        
    description:
    Get the list of proxies that the given system connects through in order to reach the server.
        
    returns: list of dict, one per proxy
            {
            'position' : (int) position in list, 1 being nearest the system
            'id'       : (int) proxy system id
            'hostname' : (str) proxy hostname
            }
        
    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID number
    """
    try:
        return rhn.session.system.getConnectionPath(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, 'get list of proxies for server id %d (%s)' % (server_id, getSystemName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

#### system information methods ####
def getCpu(rhn, server_id):
    """
    API: system.getCpu
    
    usage: getCpu(rhn, server_id)
    
    description:
    returns CPU information for a given server
    
    returns: dict
            {
            "cache"     : (str)
            "family"    : (str)
            "mhz"       : (str)
            "flags"     : (str)
            "model"     : (str)
            "vendor"    : (str)
            "arch"      : (str)
            "stepping"  : (str)
            "count"     : (str)
            }
    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getCpu(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve CPU information for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getCustomValues(rhn, server_id):
    """
    API: system.getCustomValues
    
    usage: getCustomValues(rhn, server_id)
    
    description:
    returns CPU information for a given server
    
    returns: dict: { 'custom info label' : data }
    
    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getCustomValues(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve Custom Values set for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getDetails(rhn, server_id):
    """
    API: system.getDetails
    
    usage: getDetails(rhn, server_id)
    
    description:
    gets detailed information about the chosen server, including location, OS, entitlements etc
    
    returns: dict
            { 'auto_update' : bool, 'release' : str, 'address1' : str, 'address2' : str, 'city' : str,
              'country' : str, 'state' : str, 'building' : str, 'rack' : str, 'room' : str, 
              'description' : str, 'hostname' : str, 'last_boot' : dateTime.iso8601, 'lock_status' : bool,
              'id' : int, 'profile_name' : str,
              'base_entitlement' : str, one of ['enterprise_entitled' 'sw_mgr_entitled' ]
              'addon_entitlements' : [str]  - [ 'monitoring_entitled', 'provisioning_entitled', 
                                                'virtualization_host', 'virtualization_host_platform' ]
              'osa_status' : str (one of 'unknown', 'offline', 'online']
            }
    
    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getDetails(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve detailed information for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))


# --------------------------------------------------------------------------------- #

def getDevices(rhn, server_id):
    """
    API: system.getdevices
    
    usage: getDevices(rhn, server_id)
    
    description:
    lists devices for the given system
    
    returns: list of dict, one per device:
            { 'device' : str,
              'device_class' : str,
              'driver' : str,
              'description' : str,
              'bus' : str,
              'pcitype' : str
            }
            
    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getDevices(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve device list for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getDmi(rhn, server_id):
    """
    API: system.getDmi
    
    usage: getDmi(rhn, server_id)
    
    description:
    returns DMI information (BIOS Vendor etc etc)
    returns: dict
             { 'vendor'       : str,
               'system'       : str,
               'product'      : str,
               'asset'        : str,
               'board'        : str,
               'bios_release' : str,
               'bios_vendor'  : str,
               'bios_version' : str
             }
             
    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getDmi(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve DMI information for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getEntitlements(rhn, server_id):
    """
    API: system.getEntitlements
    
    usage: getEntitlements(rhn, server_id)
    
    description:
    gets the list of entitlements for a given server ID

    returns: list of string (entitlement labels)

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID to add entitlements to
    """
    try:
        return rhn.session.system.getEntitlements(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, 'list entitlements for system ID %d' % (server_id))

# --------------------------------------------------------------------------------- #

def getEventHistory(rhn, server_id):
    """
    API: system.getEventHistory
        
    usage: getEventHistory(rhn, server_id)
            
    description:
    Returns a list history items associated with the system, ordered from newest to oldest.
    Note that the details may be empty for events that were scheduled against the system
    (as compared to instant).
    For more information on such events, see the system.listSystemEvents operation. 
            
    returns: list of dict, one per history event
            { 'completed' : dateTime.iso8601,
              'summary' : str,
              'details' : str
            }
            
    parameters:
    rhn                  - an authenticated RHN session
    server_id(int)           - server ID to add entitlements to
    """
    try:
        return rhn.session.system.getEventHistory(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, 'get even history for server ID %d (%s)' % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getId(rhn, server_name):
    """
    API: system.getId
    
    usage: getId(rhn, server_name)
    
    description
    look up a system ID for a given name. There may be more than one of these, as
    profile names are not guaranteed to be unique.
    
    returns: list of dict, one per matching system ID
            { 'id' : int,
              'name' : str,
              'last_checkin' : dateTime.iso8601
            }
    
    parameters:
    rhn                      - an authenticated RHN session
    server_name(str)         - server name (often hostname)
    """
    try:
        return rhn.session.system.getId(rhn.key, server_name)
    except Exception, E:
        return rhn.fail(E, "get system id(s) for server %s" % (server_name))


# --------------------------------------------------------------------------------- #

def getLastCheckin(rhn, server_id):
    """
    API: none, custom method

    usage: getLastCheckin(rhn, server_id)
    
    description:
    returns an xmlrpclib.DateTime object representing the system"s last known
    checkin date, for use in comparisons.
    

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return getName(rhn, server_id)['last_checkin']
    except Exception, E:
        return rhn.fail(E, "get last check-in sate for server_id %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getMemory(rhn, server_id):
    """
    API: system.getMemory

    usage: getMemory(rhn, server_id)

    description:
    returns Memory information for a given server

    returns: dict:
        { 'ram' : (int) physical memory in Mb
          'swap' : (int) swap space in Mb
        }

    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getMemory(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve Memory information for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getName(rhn, server_id):
    """
    API: system.getName
        
    usage: getName(rhn, server_id)
        
    description:
    Get system name and last check in information for the given system ID.
            
    returns: dict
            { 'id' : int,
              'name' : str,
              'last_checkin' : dateTime.iso8601
            }
        
    parameters:
    rhn                  - an authenticated RHN session
    """
    try:
        return rhn.session.system.getName(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, 'get Name and last checkin for server ID %d' % server_id)

# --------------------------------------------------------------------------------- #

def getNetwork(rhn, server_id):
    """
    API : system.getNetwork

    usage: getNetwork(rhn, server_id)
    
    description:
    returns IP address and hostname for the given server

    returns: dict
        { 'ip' : (str) IP Address
          'hostname' : (str) Hostname
        }

    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getNetwork(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve Network information for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getNetworkDevices(rhn, server_id):
    """
    API: system.getNetworkDevices

    usage: getNetworkDevices(rhn, server_id)
    
    description:
    returns NetworkDevices information for a given server

    returns: list of dict, one per interface
        { 'ip' : (str)
          'interface' : (str)
          'netmask' : (str)
          'hardware_address' : (str)
          'module' : (str)
          'broadcast' : (str)
        }
        
    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getNetworkDevices(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve Network Device information for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getRegistrationDate(rhn, server_id):
    """
    API: system.getRegistrationDate

    usage: getRegistrationDate(rhn, server_id)
    
    description:
    Returns the date the system was registered.

    returns: DateTime.iso8601

    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getRegistrationDate(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve the Registration Date for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getRelevantErrata(rhn, server_id):
    """
    API: system.getRelevantErrata

    usage:
    getRelevantErrata(rhn, server_id)

    description:
    getRelevantErrata(rhn, server_id)

    returns: list of dict, one per erratum
        { 'id' : (int) Erratum ID
          'date' : (str) date the erratum was created
          'advisory_synopsis': (str)
          'advisory_type' : (str)
          'advisory_name' : (str)
        }

    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getRelevantErrata(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "get relevant errata for server ID (%d) (%s)" % (server_id, getServerName(rhn, server_id)))


# --------------------------------------------------------------------------------- #

def getRelevantErrataByType(rhn, server_id, advisory_type):
    """
    API: system.getRelevantErrataByType

    usage:
    getRelevantErrata(rhn, server_id, advisory_type)

    description:
    getRelevantErrata(rhn, server_id)

    returns: list of dict, one per erratum
        { 'id' : (int) Erratum ID
          'date' : (str) date the erratum was created
          'advisory_synopsis': (str)
          'advisory_type' : (str)
          'advisory_name' : (str)
        }

    params:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID number
    advisory_type(str)       - type of advisory. One of ['Security Advisory', 'Product Enhancement Advisory', 'Bug Fix Advisory' ] 
    """
    try:
        return rhn.session.system.getRelevantErrata(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "get relevant errata of type %s for server ID (%d) (%s)" % ( advisory_type, server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getRelevantSecurityErrata(rhn, server_id):
    """
    API: none, custom method
    returns getRelevantErrataByType with a 'Security Advisory' argument
    """
    try:
        return getRelevantErrataByType(rhn.key, server_id, advisory_type = 'Security Advisory')
    except Exception, E:
        return rhn.fail(E, "get security errata for server ID (%d) (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getRelevantBugfixErrata(rhn, server_id):
    """
    API: none, custom method
    returns getRelevantErrataByType with a 'Bug Fix Advisory' argument
    """
    try:
        return getRelevantErrataByType(rhn.key, server_id, advisory_type = 'Bug Fix Advisory')
    except Exception, E:
        return rhn.fail(E, "get security errata for server ID (%d) (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getRelevantEnhancementErrata(rhn, server_id):
    """
    API: none, custom method
    returns getRelevantErrataByType with a 'Product Enhancement Advisory' argument
    """
    try:
        return getRelevantErrataByType(rhn.key, server_id, advisory_type = 'Product Enhancement Advisory')
    except Exception, E:
        return rhn.fail(E, "get security errata for server ID (%d) (%s)" % (server_id, getServerName(rhn, server_id)))

# -------------------------------------------------------------------- #

def getRunningKernel(rhn, server_id):
    """
    API: system.getRunningKernel

    usage: getRunningKernel(rhn, server_id)
    
    description:
    Returns the running kernel of the given system.

    returns: string
    
    params:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID number
    """
    try:
        return rhn.session.system.getRunningKernel(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve running kernel information for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getScriptResults(rhn, action_id):
    """
    API: system.getScriptResults

    usage: getScriptResults(rhn, action_id)

    description:
    Fetch results from a script execution. Returns an empty list if no results are yet available.

    returns: list of dict
        { 'serverId'   : (int)
          'startDate'  : (DateTime)
          'stopDate'   : (DateTime)
          'returnCode' : (int)
          'output'     : (str)
        }
    
    params:
    rhn                      - an authenticated RHN session
    action_id(int)           - Id for the scheduled action that runs the script.
    """
    try:
        return rhn.session.system.getScriptResults(rhn.key, action_id)
    except Exception, E:
        return rhn.fail(E, "retrieve results for script ID %d" % action_id)

# --------------------------------------------------------------------------------- #

def getServerName(rhn, server_id):
    """
    API: none, custom method

    usage: getServerName(rhn, server_id)

    description:    
    lookup the profile name for a specific server

    returns:
    string (profile label for given server ID)

    params:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID
    """
    try:
        return rhn.session.system.getName(rhn.key, int(server_id))['name']
    except Exception, E:
        return rhn.fail(E, "find a profile name for server ID %d " % server_id)

# --------------------------------------------------------------------------------- #

def getSubscribedBaseChannel(rhn, server_id):
    """
    API: getSubscribedBaseChannel

    usage: getSubscribedBaseChannel(rhn, server_id)

    description:
    returns details of the base channel for a given server

    returns: dict
        {'arch_name': (str)
         'checksum_label': (str),
         'description': (str),
         'end_of_life': (str),
         'gpg_key_fp': (str)
         'gpg_key_id': (str)
         'gpg_key_url': (str)
         'id': (int),
         'label': (str)
         'last_modified': (DateTime)
         'name': (str)
         'parent_channel_label': (str)
         'summary': (str)
         'yumrepo_label': (str)
         'yumrepo_last_sync': (str)
         'yumrepo_source_url': (str)
        }

    params:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID number
    """
    try:
        return rhn.session.system.getSubscribedBaseChannel(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve base channel information for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getUnscheduledErrata(rhn, server_id):
    """
    API: system.getScheduledErrata

    usage: getUnscheduledErrata(rhn, server_id)

    description:
    Provides an array of errata that are applicable to a given system.

    returns: list of dict, one per erratum
        { 'id' : (int) Erratum ID
          'date' : (str) date the erratum was created
          'advisory_synopsis': (str)
          'advisory_type' : (str)
          'advisory_name' : (str)
        }
    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getUnscheduledErrata(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve Unscheduled Errata information for server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def getVariables(rhn, server_id):
    """
    API: system.getVariables

    usage: getVariables(rhn, server_id)

    description:
    Lists kickstart variables set in the system record for the specified server.
    Note: This call assumes that a system record exists in cobbler for the given system and will raise an XMLRPC fault if that is not the case.
    To create a system record over xmlrpc use system.createSystemRecord
    To create a system record in the Web UI please go to System -> -> Provisioning -> Select a Kickstart profile -> Create Cobbler System Record.

    returns: dict
        {'netboot_enabled' : (bool)
         'kickstart_variables': (list of dict)
            [ {'key' : (str),
               'value' : (str or int) }
               ...
            ]
        }

    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.getVariables(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve kickstart variables for server  ID %d (%s)" % (server_id, getServerName(rhn, server_id))) 

# --------------------------------------------------------------------------------- #

def isNvreInstalled(rhn, server_id, name, version, release, epoch = None):
    """
    API: system.isNvreInstalled

    usage: isNvreInstalled(rhn, server_id, pName, pVersion, pRelease, pEpoch = "")

    description:
    Check if the package with the given NVRE is installed on given system

    params:   (* = optional)
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID number
    name(str)                - name of the RPM package
    version(str)             - RPM package version
    release(str)             - RPM package release
    epoch(str)*              - RPM package epoch (if there is one)

    """
    pkgstr = '-'.join([name, version, release])
    try:
        if epoch is not None:
            return rhn.session.system.isNvreInstalled(rhn.key, server_id, name, version, release, epoch) == 1
        else:
            return rhn.session.system.isNvreInstalled(rhn.key, server_id, name, version, release) == 1
    except Exception, E:
        return rhn.fail(E, "determine if the given package %s is installed on server ID %d (%s)" %(pkgstr, server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def listActivationKeys(rhn, server_id):
    """
    API: system.listActivationKeys

    usage: listActivationKeys(rhn, server_id)

    description: 
    List the activation keys the system was registered with.
    An empty list will be returned if an activation key was not used during registration.

    returns: list of activation keys (hex strings)

    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.listActivationKeys(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "List activation keys used to register server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def listActiveSystems(rhn):
    """
    API: system.listActiveSystems

    usage: listActiveSystems(rhn)
    
    description:
    returns a list of active systems for the logged-in user

    returns: list of dict, one per active system
         {'id': (int),
          'last_checkin': (DateTime),
          'name': (str)
         }
    params:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.listActiveSystems(rhn.key)
    except Exception, E:
        return rhn.fail(E, "list active systems for user %s" % (rhn.login))

# --------------------------------------------------------------------------------- #

def listAdministrators(rhn, server_id):
    """
    API: system.listAdministrators

    usage: listAdministrators(rhn, server_id)
    
    description:
    Returns a list of users which can administer the system

    returns: list of dict, one per user
        {'login_uc': (str) uppercased login,
         'login': (str),
         'enabled': (bool),
         'id': (int)
        }
    
    params:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.listAdministrators(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "retrieve Administrator list for server_id %d" % (server_id))

# --------------------------------------------------------------------------------- #

def listBaseChannels(rhn, server_id):
    """
    API: system.listBaseChannels

    usage: listBaseChannels(rhn, server_id)

    description:
    lists the available base channels - RH originals and clones of them!

    returns: list of dict, one per channel
        {
        "id"           : Base Channel ID.
        "name"         : Name of channel.
        "label"        : Label of Channel
        "current_base" : 1 indicates it is the current base channel

        }

    params:
    rhn - an authenticated RHN session
    server_id(int) - the server_id to investigate
    """
    try:
        return rhn.session.system.listBaseChannels(rhn.key, server_id)
    except Exception, E:
        return rhn.fail("E", "list Base Channels available to server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def listChildChannels(rhn, server_id):
    """
    API: system.listChildChannels

    usage: listChildChannels(rhn, server_id)

    description:
    Returns a list of subscribable child channels.
    This only shows channels the system is *not* currently subscribed to. 

    returns: list of dict, one per available child channel
        {   "id" : (int) channel id
            "name" : channel name
            "label" : channel label
            "summary" : channel summary
            "has_license" : 
            "gpg_key_url" :
        }
        
    params:
    rhn - an authenticated RHN session
    server_id(int) - the server_id to investigate
    """
    try:
        return rhn.session.system.listChildChannels(rhn.key, server_id)
    except Exception, E:
        return rhn.fail("E", "list Child Channels available to Server ID %d (%s)" % (server_id), getServerName(rhn, server_id))

# --------------------------------------------------------------------------------- #

def listDuplicatesByHostname(rhn):
    """
    API: system.listDuplicatesByHostname

    usage: listDuplicatesByHostname(rhn)

    description:
    List duplicate systems by Hostname

    returns: list of dict, one per group of dupes (per hostname)
        {'hostname': (str)
         'systems' : (list of dict)
          [ { 'id' : (int)
              'last_checkin' (DateTime)
          ]
        }

    params:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.listDuplicatesByHostname(rhn.key)
    except Exception, E:
        return rhn.fail(E, "list duplicate servers by hostname")

# --------------------------------------------------------------------------------- #

def listDuplicatesByIp(rhn):
    """
    API: system.listDuplicatesByIp

    usage: listDuplicatesByIp(rhn)

    description:
    List duplicate systems by IP Address

    returns: list of dict, one per group of dupes (per hostname)
        {'ip': (str)
         'systems' : (list of dict)
          [ { 'id' : (int)
              'last_checkin' (DateTime)
            }
          ]
        }

    params:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.listDuplicatesByIp(rhn.key)
    except Exception, E:
        return rhn.fail(E, "list duplicate servers by IP Address")

# --------------------------------------------------------------------------------- #

def listDuplicatesByMac(rhn):
    """
    API: system.listDuplicatesByMac

    usage: listDuplicatesByMac(rhn)

    description:
    List duplicate systems by Mac

    returns: list of dict, one per group of dupes (per hostname)
        {'mac': (str)
         'systems' : (list of dict)
          [ { 'id' : (int)
              'last_checkin' (DateTime)
          ]
        }

    params:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.listDuplicatesByMac(rhn.key)
    except Exception, E:
        return rhn.fail(E, "list duplicate servers by MAC Address")

# --------------------------------------------------------------------------------- #

def listEligibleFlexGuests(rhn):
    """
    API: system.listEligibleFlexGuests

    usage: listEligibleFlexGuests(rhn)

    description:
    List eligible flex guests accessible to the user 

    returns: list of dict, one per channel family
        { "id" : (int)
        "label" : (str)
        "name" : (str)
        "systems": [ int ]
        }

    params:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.listEligibleFlexGuests(rhn.key)
    except Exception, E:
        return rhn.fail(E, "list eligible flex guests")

# --------------------------------------------------------------------------------- #

def listFlexGuests(rhn):
    """
    API: system.listFlexGuests

    usage: listFlexGuests(rhn)

    description:
    List  flex guests accessible to the user 

    returns: list of dict, one per channel family
        { "id" : (int)
        "label" : (str)
        "name" : (str)
        "systems": [ int ]
        }

    params:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.listFlexGuests(rhn.key)
    except Exception, E:
        return rhn.fail(E, "list flex guests")

# --------------------------------------------------------------------------------- #

def listGroups(rhn, server_id):
    """
    API: system.listGroups

    usage: listGroups(rhn, server_id)
    
    description:
    lists the available groups for a given server_id

    returns: list of dict, one per system group
        {
        "id"                : (int) server group id
        "subscribed"        : (int) 1 if the given server is subscribed to this server group, 0 otherwise
        "system_group_name" : (str) Name of the server group
        "sgid"              : (int) server group id (Deprecated)
        }

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.listGroups(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "list available groups for server ID %d (%s) " % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def listInactiveSystems(rhn, days = None):
    """
    API: system.listInactiveSystems

    usage: listInactiveSystems(rhn, days)

    description:
    Lists systems that have been inactive for the default period of inactivity,
    or for the given number of days.
    
    returns: list of dict, one per system
        { 
        'id' : (int) server id
        'last_checkin' : DateTime
        'name' : (str) server profile name
        }

    params (* = optional)
    rhn                    - authenticated, active rhnapi.rhnSession() object
    *days(int)             - number of days before a system is considered inactive
                             defaults to system-wide setting if omitted.
    """
    try:
        if days is not None:
            return rhn.session.system.listInactiveSystems(rhn.key, days)
        else:
            return rhn.session.system.listInactiveSystems(rhn.key)
    except Exception, E:
        if days is not None:
            return rhn.fail(E, 'list systems inactive for %d days' % days)
        else:
            return rhn.fail(E, 'list inactive systems')

# --------------------------------------------------------------------------------- #

def listLatestAvailablePackage(rhn, server_ids, package_name):
    """
    API: system.listLatestAvailablePackage

    usage: listLatestAvailablePackage(rhn, server_ids, package_name)

    description:
    Get the latest available version of a package for each system 

    returns: list of dict, one per system
        {
        'id'      : (int) server ID
        'name'    : (str) server name
        'package' : {
                    'id'      : (int) package id
                    'name'    : 
                    'version' :
                    'release' :
                    'epoch'   :
                    'arch'    :
                    }

        }

    params:
    rhn(rhnSession)             - authenticated, active rhnapi.rhnSession object
    server_ids(list)            - list of int, server IDs
    package_name(str)           - the package name to look for
    """
    try:
        return rhn.session.system.listLatestAvailablePackage(rhn.key, server_ids, package_name)
    except Exception, E:
        return rhn.fail(E, 'list latest versions of %s for the given lits of servers' % package_name)

# --------------------------------------------------------------------------------- #

def listLatestInstallablePackages(rhn, server_id):
    """
    API: system.listLatestInstallablePackages

    usage: listLatestInstallablePackages(rhn, server_id)
    
    description:
    lists the latest installable packages for a  given server_id

    returns: list of dict, one per installable package
        {
        "name"
        "version"
        "release"
        "epoch"
        "id"
        "arch_label"
        }
    
    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.listLatestInstallablePackages(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "list latest installable packages for server id %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def listLatestUpgradeablePackages(rhn, server_id):
    """
    API: system.listLatestUpgradeablePackages

    usage: listLatestUpgradeablePackages(rhn, server_id)
    
    description:
    lists the latest upgradeable packages for a  given server_id
    
    returns: list of dict, one per package:
        {
        "name"
        "arch"
        "from_version"
        "from_release"
        "from_epoch"
        "to_version"
        "to_release"
        "to_epoch"
        "to_package_id"
        }

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.listLatestUpgradeablePackages(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "list latest Upgradeable packages for server_id %d (%s) " % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def listNewerInstalledPackages(rhn, server_id, pkg_name, pkg_ver, pkg_rel, pkg_epoch = ""):
    """
    API: system.listNewerInstalledPackages

    usage: listNewerInstalledPackages(rhn, server_id, pkg_name, pkg_ver, pkg_rel, pkg_epoch)

    description:    
    Given a package name, version, release, and epoch, returns the list of packages
    installed on the system with the same name that are newer.

    returns: list of dict, one per package
        {
        "name"
        "version"
        "release"
        "epoch"
        }
    
    parameters: (* = optional)
    rhn                     - an authenticated RHN session
    server_id(int)          - server ID number
    pkg_name(str)           - package name
    pkg_ver(str)            - package version
    pkg_rel(str)            - package release
    *pkg_epoch(str)         - package epoch
    """
    try:
        return rhn.session.system.listNewerInstalledPackages(rhn, server_id, pkg_name, pkg_ver, pkg_rel, pkg_epoch)
    except Exception, E:
        return rhn.fail(E, "List installed packages newer than %s" % ("-", join([pkg_name, pkg_ver, pkg_rel, pkg_epoch])))

# --------------------------------------------------------------------------------- #

def listNotes(rhn, server_id):
    """
    API: system.listNotes

    usage: listNotes(rhn, server_id)

    description:
    Provides a list of notes associated with a system. 

    returns: list of dict, one per note
        {
        "id"        : (int) note ID
        "subject"   : (str) Subject of the note
        "note"      : (str) Contents of the note
        "system_id" : (str) The id of the system associated with the note
        "creator"   : (str) Creator of the note
        }
    
    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.listNotes(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, 'list notes for system %d (%s)'%(server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def listOlderInstalledPackages(rhn, server_id, pkg_name, pkg_ver, pkg_rel, pkg_epoch = "" ):
    """
    API: system.listOlderInstalledPackages

    usage: listOlderInstalledPackages(rhn, server_id, server_id, pkg_name, pkg_ver, pkg_rel, pkg_epoch)
    
    description:
    Given a package name, version, release, and epoch, returns the list of packages
    installed on the system with the same name that are older.
    
    returns: list of dict, one per package
        {
        "name"
        "version"
        "release"
        "epoch"
        }
    
    parameters: (* = optional)
    rhn                     - an authenticated RHN session
    server_id(int)          - server ID number
    pkg_name(str)           - package name
    pkg_ver(str)            - package version
    pkg_rel(str)            - package release
    *pkg_epoch(str)         - package epoch
    """
    try:
        return rhn.session.system.listOlderInstalledPackages(rhn, server_id, server_id, pkg_name, pkg_ver, pkg_rel, pkg_epoch)
    except Exception, E:
        return rhn.fail(E, "List installed packages older than %s on server %d (%s)" % (
            "-".join([server_id, pkg_name, pkg_ver, pkg_rel, pkg_epoch]), server_id, getSystemName))

# --------------------------------------------------------------------------------- #

def listOutOfDateSystems(rhn):
    """
    API: system.listOutOfDateSystems

    usage: listOutOfDateSystems(rhn)

    description:
    Returns list of systems needing package updates
    
    returns: list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.listOutOfDateSystems(rhn.key)
    except Exception, E:
        return rhn.fail(E, "get a list of out of date systems")

# --------------------------------------------------------------------------------- #

def listPackageProfiles(rhn):
    """
    API: system.listPackageProfiles

    usage: listPackageProfiles(rhn)

    description:
    List the package profiles for this organization

    returns: list of dict, one per profile
        {
        'id'
        'name'
        'channel'
        }

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.listPackageProfiles(rhn.key)
    except Exception, E:
        return rhn.fail(E, "list package profiles for your organization" )

# --------------------------------------------------------------------------------- #

def listPackages(rhn, server_id):
    """
    API: system.listPackages

    usage: listPackages(rhn, server_id)

    description:
    List the installed packages for a given system    

    returns: list of dict, one per installed package
        {
        "name"
        "version"
        "release"
        "epoch"
        "arch"
        "installtime" - returned only if known
        }

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.listPackages(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "Get a list of installed packages for server %d" % (server_id))

# --------------------------------------------------------------------------------- #

def listPackagesFromChannel(rhn, server_id, chanlabel):
    """
    API: system.listPackagesFromChannel

    usage: listPackagesFromChannel(rhn, server_id, chanlabel)

    List the installed packages for a given system that are from a specific channel.

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    chanlabel(str)              - Channel label
    """
    try:
        return rhn.session.system.listPackagesFromChannel(rhn, server_id, chanlabel)
    except Exception, E:
        return rhn.fail(E, "Get a list of installed packages for server %d from channel %s" % (server_id, chanlabel))


# --------------------------------------------------------------------------------- #

def listSubscribableBaseChannels(rhn, server_id):
    """
    API: system.listSubscribableBaseChannels

    usage: listSubscribableBaseChannels(rhn, server_id)

    description:
    lists the available base channels - RH originals and clones of them!

    returns: list of dict, one per channel
        {
        "id"           : Base Channel ID.
        "name"         : Name of channel.
        "label"        : Label of Channel
        "current_base" : 1 indicates it is the current base channel

        }

    params:
    rhn - an authenticated RHN session
    server_id(int) - the server_id to investigate
    """
    try:
        return rhn.session.system.listSubscribableBaseChannels(rhn.key, server_id)
    except Exception, E:
        return rhn.fail("E", "list Base Channels available to server ID %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def listSubscribableChildChannels(rhn, server_id):
    """
    API: system.listSubscribableChildChannels

    usage: listSubscribableChildChannels(rhn, server_id)

    description:
    Returns a list of subscribable child channels.
    This only shows channels the system is *not* currently subscribed to. 

    returns: list of dict, one per available child channel
        {   "id" : (int) channel id
            "name" : channel name
            "label" : channel label
            "summary" : channel summary
            "has_license" : 
            "gpg_key_url" :
        }
        
    params:
    rhn - an authenticated RHN session
    server_id(int) - the server_id to investigate
    """
    try:
        return rhn.session.system.listSubscribableChildChannels(rhn.key, server_id)
    except Exception, E:
        return rhn.fail("E", "list Child Channels available to Server ID %d (%s)" % (server_id), getServerName(rhn, server_id))

# --------------------------------------------------------------------------------- #

def listSubscribedChildChannels(rhn, server_id):
    """
    API: system.listSubscribedChildChannels

    usage: listSubscribedChildChannels(rhn, server_id)

    description:
    List the child channels a system is subscribed to

    returns: list of dict, each representing a channel
        {
        "id", "name", "label", "arch_name", "summary",
        "description", "checksum_label", "last_modified",
        "maintainer_name", "maintainer_email", "maintainer_phone",
        "support_policy", "gpg_key_url" "gpg_key_id",
        "gpg_key_fp", "yumrepo_source_url", "yumrepo_label",
        "yumrepo_last_sync", "end_of_life", "parent_channel_label"
        }

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.listSubscribedChildChannels(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "list subscribed child channels for server %d" % (server_id))

# --------------------------------------------------------------------------------- #

def listSystemEvents(rhn, server_id):
    """
    API: system.listSystemEvents

    usage: listSystemEvents(rhn, server_id)

    description:
    List all system events for given server.
    This is *all* events for the server since it was registered.
    This may require the caller to filter the results to fetch the
    specific events they are looking for

    returns: list of dict, one per event.
    The dict structure is enormous and complex...
    {
    "name"              : (str) Name of this action.
    "scheduler_user"    : (str) who scheduled this?
    "id"                : (int) Id of this action.
    "version"           : (str) Version of action.
    "failed_count"      : (int) Number of times action failed.
    "action_type"       : (str)
    "modified_date"     : (DateTime) Date modified.
    "created_date"      : (DateTime) Date created.
    "earliest_action"   : (DateTime) Earliest date this action will occur.
    "successful_count"  : (int) Number of times action was successful.
    "archived"          : (int) If this action is archived. (1 or 0)
    "prerequisite"      : (str) Prerequisite action. (optional)
    "completed_date"    : (str) The date/time the event was completed. (optional)
    "pickup_date"       : (str) The date/time the action was picked up. (optional)
    "result_msg"        : (str) The result string after the action executes at the client machine. (optional)
    "additional_info"   : list of dict, as below:
                        {
                        "detail" : The detail provided depends on the specific event.
                        "result" : The result (if included) depends on the specific event.
                        }
    }

    ** deprecated keys, which may also be in output:
    "modified" (Deprecated by modified_date)
    "created"  (Deprecated by created_date)
    "completion_time" (Deprecated by completed_date)
    "pickup_time" (Deprecated by pickup_date)

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    """
    try:
        return rhn.session.system.listSystemEvents(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, "Get a list of system events for server %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def listSystems(rhn, rhnuser = None):
    """
    API: system.listSystems

    usage: listUserSystems(rhn, rhnuser)

    description:
    lists the systems registered / managed by a given username.
    org admins get all registered systems    

    returns: list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters:
    rhn             - an authenticated RHN session
    rhnuser         - RHN user account
    """
    if rhnuser == None:
        rhnuser = rhn.login
    try:
        return rhn.session.system.listUserSystems(rhn.key, rhnuser)
    except Exception, E:
        return rhn.fail(E, "list systems for user %s" % (rhnuser))

# --------------------------------------------------------------------------------- #

def listSystemsWithPackageId(rhn, package_id):
    """
    API: system.listSystemsWithPackage

    usage: listSystemsWithPackageId(rhn, package_id)

    description:
    Lists the systems that have the given installed package (identified by its RHN packageId)

    returns: list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters:
    rhn                     - an authenticated RHN session
    package_id(int)         - package ID number
    """
    try:
        return rhn.session.system.listSystemsWithPackage(rhn.key, package_id)
    except Exception, E:
        return rhn.fail(E,'list systems with package ID %d installed' % package_id)

# --------------------------------------------------------------------------------- #

def listSystemsWithPackage(rhn, package_name, package_ver, package_release):
    """
    API: system.listSystemsWithPackage

    usage: listSystemsWithPackage(rhn, package_name, package_ver, package_release)

    description:
    Lists the systems with the given package installed (identified by name, version and release)

    returns: list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters:
    rhn                     - an authenticated RHN session
    package_name(str)       - package name
    package_ver(str)        - package version
    package_rel(str)        - package release
    """
    try:
        return rhn.session.system.listSystemsWithPackage(rhn.key, package_name, package_ver, package_release)
    except Exception, E:
        return rhn.fail(E,'list systems with package "%s-%s-%s" installed' % (package_name, package_ver, package_rel))

# --------------------------------------------------------------------------------- #

def listUngroupedSystems(rhn):
    """
    API: system.listUngroupedSystems

    usage: listUngroupedSystems(rhn)
    
    description:
    List systems that are not members of any system group

    
    returns: list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.listUngroupedSystems(rhn.key)
    except Exception, E:
        return rhn.fail(E, "list systems which are not in any system groups" % (server_id))

# --------------------------------------------------------------------------------- #

def listUserSystems(rhn, rhnuser = None):
    """
    API: system.listUserSystems

    usage: listUserSystems(rhn, rhnuser)

    description:
    lists the systems registered / managed by a given username.
    org admins get all registered systems.
    If no username is supplied, this will behave exactly the same as system.listSystems

    returns: list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters: (* = optional)
    rhn                     - an authenticated RHN session
    *rhnuser                - RHN user account
    """
    try:
        if rhnuser is None:
            return rhn.session.system.listUserSystems(rhn.key)
        else:
            return rhn.session.system.listUserSystems(rhn.key, rhnuser)
    except Exception, E:
        if rhnuser is None:
            rhnuser = rhn.login
        return rhn.fail(E, "list systems for user %s" % (rhnuser))

# --------------------------------------------------------------------------------- #

def listVirtualGuests(rhn, virthost_sid):
    """
    API: system.listVirtualGuests

    usage: listVirtualGuests(rhn, virthost_sid)

    description:
    Lists the virtual guests for agiven virtual host 

    returns: list of dict, one per virtual guest
        {
        'id'           : (int) serverid
        'name'         : (str) profilename
        'last_checkin' : (DateTime)
        'uuid'         : (str) VM uuid
        'guest_name'   : (str) VM name, from the virtual host
        }

    parameters:
    rhn                      - an authenticated RHN session
    virthost_sid(int)        - package ID number
    """
    try:
        return rhn.session.system.listVirtualGuests(rhn.key, virthost_sid)
    except Exception, E:
        return rhn.fail(E,'list virtual guests on host with sid %d' % (virthost_sid))

# --------------------------------------------------------------------------------- #

def listVirtualHosts(rhn):
    """
    API: system.listVirtualHosts

    usage: listVirtualHosts(rhn)

    description:
    Lists the virtual hosts visible to the logged-in user 

    returns: list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters:
    rhn                     - an authenticated RHN session
    """
    try:
        return rhn.session.listVirtualHosts(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list virtual hosts')

# --------------------------------------------------------------------------------- #

def obtainReactivationKey(rhn, server_cert_or_id):
    """
    API: system.obtainReactivationKey

    usage: obtainReactivationKey(rhn, server_cert_or_id)

    description:
    obtains a reactivation key for an existing system
    
    returns: string (the reactivation key)

    parameters:
    rhn                      - an authenticated RHN session
    server_cert_or_id        - either an int (serverID) or a string (content of systemid file)
    """
    try:
        return rhn.session.system.obtainReactivationKey(rhn.key, server_cert_or_id)
    except Exception, E:
        if isinstance(server_cert_or_id, str):
            return rhn.fail(E, 'get reactivation key using systemid file')
        else:
            return rhn.fail(E, "Get a reactivation key for server %d" % (server_cert_or_id))

# --------------------------------------------------------------------------------- #

def provisionSystem(rhn, server_id, kslabel, earliest_start=None):
    """
    API: system.provisionSystem
    
    usage: provisionSystem(rhn, server_id, kslabel, *earliest_start)

    description:
    provision the given system using the specified kickstart profile
    The optional 'earliest_start' parameter can specify a time after which the
    provisioning will take place.

    returns: bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)          - server id
    kslabel(str)            - kickstart profile label
    earliest_start(str)     - earliest occurence. This is a string in iso8601 format
                              "%Y%m%dT%H:%M:%S", e.g. 20110401T11:12:35
    """
    try:
        if earliest_start is not None:
            return isinstance(rhn.session.system.provisionSystem(rhn.key, server_id, kslabel, earliest_start), int)
        else:
            return isinstance(rhn.session.system.provisionSystem(rhn.key, server_id, kslabel), int)
    except Exception, E:
        return rhn.fail(E, 'provision system id %d (%s)' % ( server_id, getServerName(rhn, server_id) ))
    pass

# --------------------------------------------------------------------------------- #

def provisionVirtualGuest(rhn, server_id, guest_name, kslabel, **kwargs):
    """
    API: system.provisionVirtualGuest

    usage: provisionVirtualGuest(rhn, server_id, guest_name, kslabel, **kwargs)

    description:
    Provision a guest on the host specified. Defaults to: memory=256MB, vcpu=1, storage=2048MB
    This schedules the guest for creation and will begin the provisioning process when
    the host checks in or if OSAD is enabled will begin immediately.

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID number
    guest_name(str)          - profile name for the new guest
    kslabel(str)             - kickstart profile to use for the new guest
    plus one or more of the following keyword arguments (defaults below)
    *memoryMb(int)           - RAM in Mb for the new guest (default 256)
    *vcpus(int)              - number of vcpus (default 1)
    *storageMb(int)          - Amount of storage to assign (default 2048)
    """
    vmsettings = { 'memoryMb' : 256, 'vcpus' : 1, 'storageMb' : 2048 }
    try:
        vmsettings.update(kwargs)
        return rhn.session.system.provisionVirtualGuest(rhn.key, server_id, guest_name, kslabel, **vmsettings) == 1
    except Exception, E:
        return rhn.fail(E, "provision new VM %s on server %s" %(guest_name, getServerName(server_id)))

# --------------------------------------------------------------------------------- #

def removeEntitlements(rhn, server_id, ents_list):
    """
    API: system.removeEntitlements

    usage: removeEntitlements(rhn, server_id, ents_list)
    
    description:
    downloads the server_id file (/etc/sysconfig/rhn/systemid) for a given server_id.
    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID number
    ents_list([str])         - list of entitlement labels to remove
    """
    try:
        return rhn.session.system.removeEntitlements(rhn.key, server_id, entitlementList) == 1
    except Exception, E:
        return rhn.fail(E, "remove entitlements from server_id %d" % (server_id))

# --------------------------------------------------------------------------------- #

def scheduleApplyErrata(rhn, server_ids, errata_ids, apply_after=None):
    """
    API: system.schedeluApplyErrata

    usage: scheduleApplyErrata(rhn, server_ids, errata_ids, apply_after=None)

    description:
    schedule the an 'apply errata' action for the given system or list of systems

    returns: bool, or throws exception

    parameters: (* = optinal)
    rhn                             - rhnsession object
    server_id(int or list of)       - the server (or servers) to apply the action to
    errata_ids(list of int)         - list or errata IDs to apply
    *apply_after(DateTime.iso8601)   - earliest date this can occur
    """
    # handle the multiple parameter combinations
    try:
        if not isinstance(server_ids, list):
            server_ids = [ server_ids ]
        if apply_after is None:
            return rhn.session.system.scheduleApplyErrata(rhn.key, server_ids, errata_ids) == 1
        else:
            return rhn.session.system.scheduleApplyErrata(rhn.key, server_ids, errata_ids, apply_after) == 1
    except Exception, E:
        return rhn.fail(E, 'schedule application of errata [%s] for server id(s) [%s]' %(','.join(errata_ids), ''.join(map(str,server_ids))))

# --------------------------------------------------------------------------------- #

def scheduleGuestAction(rhn, guest_id, guest_state, apply_date):
    """
    API: system.scheduleGuestAction

    usage: scheduleGuestAction(rhn, guest_id, guest_state, apply_date)

    description:
    Schedules a guest action for the specified virtual guest for a given date/time.
    If the date/time is omitted, action is scheduled ASAP

    returns: bool, or throws Exception

    parameters:
    rhn                             - an authenticated RHN session
    guest_id(int)                   - System id of virtual guest
    guest_state(str)                - state of guest, one of ['start', 'suspend', 'resume', 'restart', 'shutdown']
    *apply_date(DateTime iso8601)   - time to schedule the action (imeediately, if not specified)
    """
    try:
        if apply_date is not None:
            return isinstance(rhn.session.system.scheduleGuestAction(rhn.key, guest_id, guest_state, apply_date), int)
        else:
            return isinstance(rhn.session.system.scheduleGuestAction(rhn.key, guest_id, guest_state), int)
    except Exception, E:
        return rhn.fail(E, 'schedule guest %s for guest id %s' %(guest_state, str(guest_id)))
            
# --------------------------------------------------------------------------------- #

def scheduleHardwareRefresh(rhn, server_id, apply_after):
    """
    API: system.scheduleHardwareRefresh

    usage: scheduleHardwareRefresh(rhn, server_id, apply_after)
    
    description:
    downloads the server_id file (/etc/sysconfig/rhn/systemid) for a given server_id.

    returns: bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID number
    apply_after(DateTime)    - earliest date for update (iso 8601 format)
    """
    try:
        return rhn.session.system.scheduleHardwareRefresh(rhn.key, server_id, apply_after) == 1
    except Exception, E:
        return rhn.fail(E, "schedule hardware refresh for server id %d (%s)" % (server_id, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def schedulePackageInstall(rhn, server_id, package_ids, apply_after):
    """
    API: system. schedulePackageInstall

    usage: schedulePackageInstall(rhn, server_id, apply_after)
    
    description:
    Schedule package installation for a system
    
    returns: bool, or throws exception

    parameters:
    rhn                       - an authenticated RHN session
    server_id(int)            - server ID number
    package_ids([int])        - list of package IDs to install
    apply_after(dateTime)     - earliest date for installation.
    """
    try:
        return rhn.session.system.schedulePackageInstall(rhn.key, server_id, package_ids, apply_after) == 1
    except Exception, E:
        return rhn.fail(E, " install packages [%s] on server %d (%s)" % (''.join(map(str, package_ids)),
                                                                         server_id,
                                                                         getServerName(rhn, server_id)) )

# --------------------------------------------------------------------------------- #

def schedulePackageRefresh(rhn, server_id, apply_after):
    """
    API: system schedulePackageRefresh

    usage: schedulePackageRefresh(rhn, server_id, apply_after)
    
    description:
    schedules  a package profile refresh for the given server id

    returns: bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    apply_after(dateTime)     - earliest date this will occur
    """
    try:
        return isinstance(rhn.session.system.schedulePackageRefresh(rhn.key, server_id, apply_after), int)
    except Exception, E:
        return rhn.fail(E, "remove entitlements for server %d (%s)" % (server_id))

# --------------------------------------------------------------------------------- #

def schedulePackageRemove(rhn, server_id, package_ids, apply_after):
    """
    API: system.schedulePackageRemove

    usage: schedulePackageRemove(rhn, server_id, apply_after)
    
    description:
    schedule the removal of a (list of) packages from the given system
    
    returns: bool, or throws exception

    parameters:
    rhn                       - an authenticated RHN session
    server_id(int)            - server ID number
    package_ids([int])        - list of package ids to remove
    apply_after(dateTime)     - earliest date this will occur
    """
    try:
        if not isinstance(package_ids, list):
            package_ids = [ package_ids ]
        return rhn.session.system.schedulePackageRemove(rhn.key, server_id, package_ids, apply_after) == 1
    except Exception, E:
        return rhn.fail(E, "remove package ids [%s] from server %d (%s)" % ( ','.join(map(str, package_ids),
                                                                            server_id,
                                                                            getServerName(rhn, server_id))))

# --------------------------------------------------------------------------------- #

def scheduleReboot(rhn, server_id, apply_after):
    """
    usage: scheduleReboot(rhn, server_id, apply_after)    

    schedule a reboot for the given server_id

    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    apply_after(dateTime)     - earliest date for installation.
    """
    try:
        rhn.session.system.scheduleReboot(rhn.key, int(server_id), apply_after)
    except Exception, E:
        return rhn.fail(E, "schedule a reboot for server ID %d" % (server_id))

# --------------------------------------------------------------------------------- #

def scheduleScriptRun(rhn, server_ids, user_name, group_name, timeout, script, apply_after=None):
    """
    API: system.scheduleScriptRun
    
    usage: scheduleScriptRun(rhn, system_ids, user_name, group_name, timeout, script, apply_after=None)

    description:
    Schedule a script to run on the given server id (or list of).

    returns: bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    server_ids([int])       - server id (or list of)
    user_name(str)          - username that script should use
    group_name(str)         - group name that script should use
    timeout(int)            - timeout in seconds
    script(str)             - script content
    apply_after(DateTime)   - earliest date/time for script run (ios8601 format)
    """
    if not isinstance(server_ids, list):
        server_ids = [ server_ids ]
    args = [ server_ids, user_name, group_name, timeout, script ]
    if apply_after is not None:
        args.append(apply_after)
    try:
        return isinstance(rhn.session.system.scheduleScriptRun(rhn.key, *args), int)

    except Exception, E:
        return rhn.fail(E,'' % ())

# --------------------------------------------------------------------------------- #
def scheduleSyncPackagesWithSystem(rhn, target_sid, source_sid, package_ids, apply_after):
    """
    API: system.scheduleSyncPackagesWithSystem

    usage: scheduleSyncPackagesWithSystem(rhn, target_sid, source_sid, package_ids, apply_after)

    description:
    schedules a package synchronisation from a source server to a target, for the given list
    of package ids
    
    returns:
   
    parameters:
    rhn                     - an authenticated RHN session
    target_sid(int)         - the server ID to synchronise
    source_sid(int)         - the source server ID
    package_id([int])       - list of package IDs to synchronise
    apply_after(DateTime)   - when to perform the sync
    """
    try:
        return rhn.session.system.scheduleSyncPackagesWithSystem(rhn.key, target_sid, source_sid, package_ids, apply_after) == 1
    except Exception, E:
        return rhn.fail(E,'schedule package sync from server %d to server %d' % (source_sid, target_sid))

# --------------------------------------------------------------------------------- #

def searchByName(rhn, server_regex):
    """
    API: system.searchByName

    usage: searchByName(rhn, server_regex)

    description:
    search for systems whose profile names match the provided regular expression
    http://download.oracle.com/javase/1.4.2/docs/api/java/util/regex/Pattern.html
     - similar to extended regex

    returns: list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters:
    rhn                     - an authenticated RHN session
    server_regex(str)       - regular expression to match server names
    """
    try:
        return rhn.session.system.searchByName(rhn.key, server_regex)
    except Exception, E:
        return rhn.fail(E,'search for servers matching regex "%s"' % (server_regex))
# --------------------------------------------------------------------------------- #

def setBaseChannel(rhn, server_id, chan_label):
    """
    API: system.setBaseChannel

    usage: setBaseChannel(rhn, server_id, chan_label)

    description:
    changes the specified system's subscribed base channel

    returns: bool, or throws exceptions

    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)          - server id to change
    chan_label(str)         - new base channel label
    """
    try:
        return rhn.session.system.setBaseChannel(rhn.key, server_id, chan_label) == 1
    except Exception, E:
        return rhn.fail(E,'set base channel for server ID %d to %s' % (server_id, chan_label))

# --------------------------------------------------------------------------------- #
def setChildChannels(rhn, server_id, chan_list):
    """
    API: system.setChildChannels

    usage: setChildChannels(rhn, server_id, chan_list)

    description:
    set the list of subscribed base channels for the given system
    the labels provided must be children of the system's subscribed base channel.

    returns: bool, or thows exception

    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)          - server ID to change
    chan_list([str])        - list of child channel labels
    """
    try:
        return rhn.session.setChildChannels(rhn.key, server_id, chan_list) == 1
    except Exception, E:
        return rhn.fail(E,'subscribe system %d to child channels [%s]' % (server_id, ','.join(chan_list)))

def setCustomValues(rhn, server_id, details):
    """
    API: system.setCustomValues

    usage: setCustomValues(rhn, server_id, details)
    where details is a a dict... { 'varname' : value,...}

    description:
    set custom details for a server

    returns: bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server ID number
    details(dict)             - dict of keys and values to set.
    """
    try:
        return rhn.session.system.setCustomValues(rhn.key, server_id, details) == 1
    except Exception, E:
        return rhn.fail(E, "set custom details for server ID %d" % (server_id) )

# --------------------------------------------------------------------------------- #

def setCustomValues2(rhn, server_id, **kwargs):
    """
    API: system.setCustomValues

    usage: setCustomValues(rhn, server_id, **kwargs)
    where kwargs is a list of key=value pairs
    e.g. test=wibble,hostname=bob.example.com
    
    Only works for keys without spaces in their labels.
    (but then you shouldn't be putting spaces in there anyway!)
    
    description:
    set custom details for a server

    returns: bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID number
    **kwargs                 - list of key=value pairs
    """
    try:
        return rhn.session.system.setCustomValues(rhn.key, server_id, kwargs) == 1
    except Exception, E:
        return rhn.fail(E, "set custom details for server %s" % (getServerName(rhn, server_id)) )

# --------------------------------------------------------------------------------- #
def setDetails(rhn, server_id, **kwargs):
    """
    API: system.setDetails

    usage: setDetails(rhn, name=val, name=val, name=val...)
    where only the required values are needed, but must be provided as NAME=value pairs
    string "profile_name" - System's profile name
    string "base_entitlement" - System's base entitlement label. (enterprise_entitled or sw_mgr_entitled)
    boolean "auto_errata_update" - True if system has auto errata updates enabled
    string "description" - System description
    string "address1" - System's address line 1.
    string "address2" - System's address line 2.
    string "city"
    string "state"
    string "country"
    string "building"
    string "room"
    string "rack"

    description:
    set the details for an existing RHN system profile

    returns: bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)          - the server to change
    plus a list of name=value pairs
    kwargs will be created as a dict of the name=value pairs
    """
    try:
        return rhn.session.system.setDetails(rhn.key, server_id, kwargs)
    except Exception, E:
        return rhn.fail(E,'set details for server id %d' % (server_id))

# --------------------------------------------------------------------------------- #

def setGroupMembership(rhn, server_id, group_id, is_member=1):
    """
    API: system.setGroupMembership

    usage: setGroupMembership(rhn, server_id, group_id, is_member=1)

    description:
    adds or removes the given server id to/from the given groupid
    
    returns: bool, or throws exception
    
    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)          - server to manage
    group_id(int)           - server group id
    is_member(int)          - whether the server should be a member of the
                              group or not. 1=yes, 0=no. default is 1(yes)
    """
    try:
        return rhn.session.system.setGroupMembership(rhn.key, server_id, group_id, is_member) == 1
    except Exception, E:
        return rhn.fail(E,'set group membership for server id %d' % (server_id))

# --------------------------------------------------------------------------------- #
def setGuestCpus(rhn, guest_id, num_cpus):
    """
    API: system.setGuestCpus

    usage: setGuestCpus(rhn, guest_id, num_cpus)

    description:
    set the number of virtual CPUs for the given virtual guest

    returns: bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    guest_id(int)           - server ID for virtual guest
    num_cpus(int)           - number of virtual CPUs to assign
    """
    try:
        return isinstance(rhn.session.system.setGuestCpus(rhn.key, guest_id, num_cpus), int)
    except Exception, E:
        return rhn.fail(E,'set CPUs to %d for virtual guest id %d' % (num_cpus, guest_id))

# --------------------------------------------------------------------------------- #

def setGuestMemory(rhn, guest_id, memory_mb):
    """
    API: system.getGuestMemory

    usage: setGuestMemory(rhn, guest_id, memory_mb)

    description:
    set the amount of memory for the given virtual server

    returns: bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session

    """
    try:
        return isinstance(rhn.session.system.setGuestMemory(rhn.key, guest_id, memory_mb), int)
    except Exception, E:
        return rhn.fail(E,'set memory for virtual guest %d to %d Mb' % (guest_id, memory_mb))

# --------------------------------------------------------------------------------- #

def setLockStatus(rhn, server_id, lock_status):
    """
    API: system.setLockStatus

    usage: setLockStatus(rhn, server_id, lock_status)

    description:
    locks or unlocks a given system ID

    returns: bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)          - server ID
    lock_status(int)        - whether system is locked (0=no, 1=yes)
    """
    try:
        return rhn.session.system.setlockStatus(rhn.key, server_id, lock_status) == 1
    except Exception, E:
        return rhn.fail(E,'lock or unlock server %d ' % (server_id))

# --------------------------------------------------------------------------------- #

def setProfileName(rhn, server_id, server_name):
    """
    API: system.setProfileName

    usage: setProfileName(rhn, server_id, server_name)

    description:
    renames a system profile

    returns: bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)          - server ID
    server_name(str)        - new profile name
    """
    try:
        return rhn.session.system.setProfileName(rhn.key, server_id, server_name) == 1
    except Exception, E:
        return rhn.fail(E,'rename server id %d to %s' % (server_id, server_name))

# --------------------------------------------------------------------------------- #

def setVariables(rhn, server_id, netboot_enabled, var_list):
    """
    API: system.setVariables

    usage: setVariables(rhn, server_id, netboot_enabled, var_list)

    description:
    Sets a list of kickstart variables in the cobbler system record for the specified server. 
    Note: This call assumes that a system record exists in cobbler for the given system
    and will raise an XMLRPC fault if that is not the case.
    To create a system record over xmlrpc use system.createSystemRecord

    returns: bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)          - server id
    netboot_enabled(bool)   - is PXE boot enabled for this server?
    var_list([dict])        - list of dicts, one per name : value pair
    """
    try:
        return rhn.session.system.setVariables (rhn.key, server_id, netboot_enabled, var_list) == 1
    except Exception, E:
        return rhn.fail(E,'set variables for server %d' % (server_id))
# --------------------------------------------------------------------------------- #

def upgradeEntitlement(rhn, server_id, ent_name):
    """
    API: system.upgradeEntitlement

    usage: upgradeEntitlement(rhn, server_id, ent_name

    description:
    Adds an entitlement to a given server. 

    returns: bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)         - server ID number
    ent_name(str)          - entitlement name to add. one of [ 'enterprise_entitled',
                             'provisioning_entitled', 'monitoring_entitled',
                             'nonlinux_entitled', 'virtualization_host',
                             'virtualization_host_platform']
    """
    try:
        return rhn.session.system.upgradeEntitlement(rhn.key, server_id, ent_name) == 1
    except Exception, E:
        return rhn.fail(E,'add entitlement %s to server id %d' % (ent_name, server_id))
        
# --------------------------------------------------------------------------------- #

def whoRegistered(rhn, server_id):
    """
    API: system.whoRegistered

    usage: whoRegistered(rhn, server_id)

    description:
    Returns information about the user who registered the system

    returns: dict

    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)         - server ID number
    """
    try:
        return rhn.session.system.whoRegistered(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E,'discover user who registered server id %d' % (server_id))

# --------------------------------------------------------------------------------- #

# system.config namespace

# --------------------------------------------------------------------------------- #

def addConfigChannels(rhn, server_ids, config_channels, add_to_top):        
    """
    API: system.config.addChannels

    usage: addConfigChannels(rhn, server_ids, config_channels, add_to_top)

    description:
    Given a list of servers and configuration channels, appends the configuration channels
    to either the top or the bottom (whichever you specify) of a system's subscribed configuration channels list.
    The ordering of the configuration channels provided in the add list is maintained while adding.
    If one of the configuration channels in the 'add' list has been previously subscribed
    by a server, the subscribed channel will be re-ranked to the appropriate place. 

    returns: bool, or throws exception

    parameters:
    rhn                         - an authenticated RHN session
    server_ids(list/int)        - list of server IDs
    config_channels(list/str)   - list of channel labels
    add_to_top(bool)            - whether to add the channels in order to the top or bottom
                                  of the subscribed channel list.
    """
    if not isinstance(server_ids, list):
        server_ids = [ server_ids ]
    if not isinstance(config_channels, list):
        config_channels = [ config_channels ]
    try:
        return rhn.session.system.config.addChannels(rhn.key, server_ids, config_channels, add_to_top) == 1
    except Exception, E:
        return rhn.fail(E, 'add config channel(s) [%s] to server(s) [%s]'%(','.join(config_channels),
            ','.join([getServerName(rhn, x) for x in server_ids ])))

# --------------------------------------------------------------------------------- #

def createOrUpdatePath(rhn, server_id, path, isdir = False, local = 1, **kwargs):
    """
    API: system.config.createOrUpdatePath

    usage: createOrUpdatePath(rhn, server_id, path, directory = False, local = 0, **kwargs)
    where kwargs is a list of key=value pairs (see parameters below)

    description:
    create or update a configuration file either in a system's local override channel or sandbox

    returns: bool, or throws exception (depends on RHN debug setting)

    parameters (* = optional)
    rhn                         - an authenticated RHN session.
    path(str)                   - the absolute path on the target system, including filename.
    isdir(bool)                 - this is a directory, not a file
    local(int)                  - commit this file to the local override channel (1) or sandbox(0)

    plus a selection of the following key=value arguments. (*=optional)
    owner(str)                      - the owner of the file once deployed.
    group(str)                      - the group associated with the file once deployed.
    permissions(str)                - octal permissions for the deployed file (e.g. 0644)
    * contents(str)                 - the contents of the file (ignored for directories)
                                      while this will work without content, it's not the best idea.
    * contents_enc64(bool)          - contents are base64 encoded (for binary files)
    * selinux_ctx(str)              - SELinux context
    * macro_start_delimeter(str)    - string used to indicate beginning of macro expressions. Leave empty for default
    * macro_end_delimeter(str)      - string used to indicate the end of macro expressions. Leave empty for default.
    * revision(int)                 - revison of updated file (auto-incremented)
    """
    try:
        return isinstance(rhn.session.system.config.createOrUpdatePath(rhn.key, server_id, path, isdir, kwargs, local), dict)
    except Exception, E:
        if local == 1:
            return rhn.fail(E, 'update path %s in system %s local override channel' %(path, getServerName(server_id)))
        else:
            return rhn.fail(E, 'update path %s in system %s sandbox' %(path, getServerName(server_id)))
            
# --------------------------------------------------------------------------------- #

def createOrUpdateSymlink(rhn, server_id, path, local = 1, **kwargs):
    """
    API: system.config.createOrUpdateSymlink

    usage: createOrUpdateSymlink(rhn, channel_label, path, **kwargs)
    where **kwargs is a list of key=value pairs (see parameters, below)

    Creates or Updates a new Symlink (file or directory) in a config channel

    returns: dict showing path information

    parameters (*=optional)
    rhn                     - an authenticated RHN session.
    server_id(int)          - server ID
    path(str)               - path on filesystem
    *local(int)             - commit this file to the local override channel (1) or sandbox(0)
                              (default is local override channel)

    plus one or more key-value pairs as follows (*=optional)
    target_path(str)        - the absolute path to the symlink's target
    *selinux_ctx(str)       - SELinux context for the symlink
    *revision(int)          - revison of updated file 
    """
    try:
        if rhn.debug:
            print rhn.key, server_id, path, kwargs, local
        return isinstance(rhn.session.system.config.createOrUpdateSymlink(rhn.key, server_id, path, kwargs, local), dict)
    except Exception, E:
        if local == 1:
            return rhn.fail(E, 'update symlink %s in system %s local override channel' %(path, getServerName(rhn, server_id)))
        else:
            return rhn.fail(E, 'update symlink %s in system %s sandbox' %(path, getServerName(rhn, server_id)))

# --------------------------------------------------------------------------------- #

def deleteConfigFiles(rhn, server_id, path_list, local=False):
    """
    API: system.config.deleteFiles

    usage: deleteFiles(rhn, server_id, fileList, localChannel=False)

    Deletes files from a local or sandbox channel of a server

    returns: bool, or throws exception.

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)           - server identifier
    path_list(list/str)      - path (or list of paths) to delete
    local(bool)              - delete from local channel(true) or sandbox(false).
                               False by default.
    """
    if not isinstance(path_list, list):
        path_list = [ path_list ]
    try:
        return rhn.session.system.config.deleteFiles(rhn.key, server_id, path_list, local) == 1
    except Exception, E:
        return rhn.fail(E, 'delete files from server')

# --------------------------------------------------------------------------------- #

def deployAllConfigChannels(rhn, server_ids, date = None):
    """
    usage: deployAll(rhn, systemIDList, date)

    Schedules a deploy action for all config channels on a given list of system IDs

    returns: bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    systemIDList(list/int)   - list of system IDs to work on
    date(str)                - earliest date for deploy action. in iso8601 format.
                               e.g. 20110505T11:48:56 (%Y%m%dT%H:%M:%S)
                               if omitted, defaults to current time/date
    """
    # encode a DateTime instance (defaults to local time)
    applyafter = rhn.encodeDate(date)
    if not isinstance(server_ids, list):
        server_ids = [ server_ids ]
    try:
        return rhn.session.system.config.deployAll(rhn.key, server_ids, applyafter) == 1
    except Exception, E:
        return rhn.fail(E, 'schedule the requested deploy action' )

# --------------------------------------------------------------------------------- #

def listConfigChannels(rhn, server_id):
    """
    usage: listChannels(rhn, server_id)

    Lists the config channels for a server order of rank

    returns: list of dicts, one per channel

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)            - server identifier
    """
    try:
        return rhn.session.system.config.listChannels(rhn.key, server_id)
    except Exception, E:
        return rhn.fail(E, 'list config channels for server %d' % server_id)

# --------------------------------------------------------------------------------- #

def listConfigFiles(rhn, server_id, local=1):
    """
    API: system.config.listFiles

    usage: listFiles(rhn, server_id, listLocal=1)

    descriptions
    Lists the configuration files for a server, either from config channels
    (including local overrides) or from the system's sandbox.

    returns: list of dicts, one per channel.

    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)          - RHN Server ID
    local(int)              - list files in system's local override channel (1)
                              or sandbox (0)
    """
    try:
        return rhn.session.system.config.listFiles(rhn.key, server_id, local)
    except Exception, E:
        return rhn.fail(E, 'list files on server id %d' % server_id)

# --------------------------------------------------------------------------------- #

def lookupConfigFileInfo(rhn, server_id, path_list, local=1):
    """
    usage: lookupFileInfo(rhn, server_id, fileList, searchLocal=1)

    Lists the package filenames affected by a given erratum

    returns: list of dicts, one per path.

    parameters:
    rhn                     - an authenticated RHN session
    server_id(int)          - integer ID of the server to query
    path_list(list/str)     - a list of paths to query
    local(int)              - search config channels + local override (1)
                              search sandbox (0)
    """
    if not isinstance(path_list, list):
        path_list = [ path_list ]
    try:
        return rhn.session.system.config.lookupFileInfo(rhn.key, server_id, path_list, local)
    except Exception, E:
        return rhn.fail(E, 'get file revision info for files [%s]' % ','.join(path_list))
     
# --------------------------------------------------------------------------------- #

def removeConfigChannels(rhn, server_ids, config_channels):
    """
    usage: removeChannels(rhn, serverList, channelList)

    Removes the given config channels from a list of servers

    returns: bool, or throws exception

    parameters:
    rhn                       - an authenticated RHN session
    server_ids(list/int)      - list of server IDs
    config_channels(list/str) - list of channel labels
    """
    if not isinstance(server_ids, list):
        server_ids = [ server_ids ]
    if not isinstance(config_channels, list):
        config_channels = [ config_channels ]
    try:
        return rhn.session.system.config.removeChannels(rhn.key, server_ids, config_channels) == 1
    except Exception, E:
        return rhn.fail(E, 'remove config channels [%s] from servers [%s]' %( ','.join(config_channels),
            ','.join([ getServername(x) for x in server_ids ])))

# --------------------------------------------------------------------------------- #

def setConfigChannels(rhn, server_ids, config_channels):
    """
    API: system.config.setChannels

    usage: setConfigChannels(rhn, server_ids, config_channels))

    description:
    replaces the existing config channels for each of the servers in server_ids
    config_channels should be in descending ranked order

    returns: bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    server_ids(list/int)      - list of server IDs
    config_channels(list/str) - list of channel labels
    """
    if not isinstance(server_ids, list):
        server_ids = [ server_ids ]
    if not isinstance(config_channels, list):
        config_channels = [ config_channels ]
    try:
        return rhn.session.system.config.setChannels(rhn.key, server_ids, config_channels) == 1
    except Exception, E:
        return rhn.fail(E, 'set config channels [%s] for servers [%s]' %( ','.join(config_channels),
            ','.join([ getServername(x) for x in server_ids ])))

# * system.custominfo namespace

def createCustomInfoKey(rhn, label, description):
    """
    API: system.custominfo.createKey

    usage: createCustomInfoKey(rhn, label, description)

    description:
    create a new key for storing custom information

    returns: bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    label(str)               - label for the new key
    description(str)         - description of the key
    """
    try:
        return rhn.session.system.custominfo.createKey(rhn.key, label, description) == 1
    except Exception, E:
        return rhn.fail(E, 'create new custom info key %s' % label)

def deleteCustomInfoKey(rhn, label):
    """
    API: system.custominfo.deleteKey

    usage: deleteCustomInfoKey(rhn, label)

    description:
    deletes a custom system information key.
    This will remove the key and any information stored in it for all systems

    returns: bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    label(str)               - label for the new key
    """
    try:
        return rhn.session.system.custominfo.deleteKey(rhn.key, label)
    except Exception, E:
        return rhn.fail(E, 'delete custom info key %s' % label)
    
def listAllCustomInfoKeys(rhn):
    """
    API: system.custominfo.listAllKeys

    usage: listAllCustomInfoKeys(rhn)

    description:
    List the custom information keys defined for the user's organization

    returns: list of dict (one per key)

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.custominfo.listAllKeys(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list all custom system information keys')

# --------------------------------------------------------------------------------- #
    
# -- system.provisioning.snapshot namespace -- #

def deleteSnapshot(rhn, snapshot_id):
    """
    API: system.provisioning.snapshot

    usage: deleteSnapshot(rhn, snapshot_id)

    description:
    deletes the snapshot with the given ID

    returns: bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    snapshot_id(int)         - label for the new key
    """
    try:
        return rhn.session.system.provisioning.snapshot.deleteSnapshot(rhn.key. snapshot_id) == 1
    except Exception, E:
        return rhn.fail(E, 'delete snapshot ID %d' % snapshot_id)

# --------------------------------------------------------------------------------- #

def deleteSystemSnapshots(rhn, server_id, **kwargs):
    """
    API: system.provisioning.snapshot.deleteSnapshots

    usage: deleteSnapshots(rhn, **kwargs)
    possible keyword arguments are:  startDate, endDate

    description:
    deletes all snapshots for a given server, optionally between 2 dates.
    If no dates are provided, ALL snapshots for thse given server are deleted.
    if startDate is provided without endDate, evrything after startDate is deleted.
    
    returns: bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)           - RHN server id
    optional extra arguments:
    iso8601 format is %Y%m%dT%H:%M:%S e.g. 20110506T11:12:13
    *startDate(str)          - iso8601 format date string
    *endDate(str)            - iso8601 format date string
    """
    # let's encode our date strings appropriately for XMLRPC
    if kwargs.has_key('startDate'):
        kwargs['startDate'] = rhn.encodeDate(kwargs['startDate'])
    if kwargs.has_key('endDate'):
        kwargs['endDate'] = rhn.encodeDate(kwargs['endDate'])

    try:
        return rhn.session.system.provisioning.snapshot.deleteSnapshots(rhn.key, server_id, kwargs) == 1
    except Exception, E:
        return rhn.fail(E, 'delete snapshots for system %s' % getServerName(rhn, server_id))

# --------------------------------------------------------------------------------- #

def deleteSnapshots(rhn, **kwargs):
    """
    API: system.provisioning.deleteSnapshots

    usage: deleteSnapshots(rhn, **kwargs)

    description:
    delete all system snaphots, for all servers, optionally between 2 dates.
    

    returns: bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    optional extra arguments:
    iso8601 format is %Y%m%dT%H:%M:%S e.g. 20110506T11:12:13
    *startDate(str)          - iso8601 format date string
    *endDate(str)            - iso8601 format date string
    """
    # let's encode our date strings appropriately for XMLRPC
    if kwargs.has_key('startDate'):
        kwargs['startDate'] = rhn.encodeDate(kwargs['startDate'])
    if kwargs.has_key('endDate'):
        kwargs['endDate'] = rhn.encodeDate(kwargs['endDate'])
    try:
        return rhn.session.system.provisioning.snapshot.deleteSnapshots(rhn.key, kwargs) == 1
    except Exception, E:
        return rhn.fail(E,  'delete system snapshots')

# --------------------------------------------------------------------------------- #
    
def listSnapshotConfigFiles(rhn, snapshot_id):    
    """
    API: system.provisioning.snapshot.listSnapshotConfigFiles

    usage: listSnapshotConfigFiles(rhn, snapshot_id)

    description:
    list the config files associated with a snapshot

    returns: list of dict, one per configuration file

    parameters:
    rhn                      - an authenticated RHN session
    snapshot_id(int)         - the snapshot ID
    """
    try:
        return rhn.sessions.system.provisioning.snapshot.listSnapshotConfigFiles(rhn.key, snapshot_id)
    except Exception, E:
        return rhn.fail(E, 'list config files for snapshot ID %d' % snapshot_id)

# --------------------------------------------------------------------------------- #

def listSnapshotPackags(rhn, snapshot_id):
    """
    API: system.provisioning.snapshot.listSnapshotPackages

    usage: listSnapshotPackags(rhn, snapshot_id)

    description:
    list the packages associated with a snapshot

    returns: list of dict, one per package

    parameters:
    rhn                      - an authenticated RHN session
    snapshot_id(int)         - snapshot ID
    """
    try:
        return rhn.session.system.provisioning.snapshot.listSnapshotPackages(rhn.key, snapshot_id)
    except Exception, E:
        return rhn.fail(E, 'list packages associated with snapshot ID %d' % snapshot_id)

# --------------------------------------------------------------------------------- #

def listSnapshots(rhn, server_id, **kwargs):
    """
    API: system.provisioning.snapshot.listSnapshots

    usage: listSnapshots(rhn, server_id, **kwargs)
    where optional keyword args are startDate and/or endDate

    description:
    list the snapshots associated with the given server ID. Start and end dates are optional.
    

    returns: list of dict, one per snapshot

    parameters:
    rhn                      - an authenticated RHN session
    server_id(int)           - server ID
    optional extra arguments:
    iso8601 format is %Y%m%dT%H:%M:%S e.g. 20110506T11:12:13
    *startDate(str)          - iso8601 format date string
    *endDate(str)            - iso8601 format date string
    """
    # let's encode our date strings appropriately for XMLRPC
    if kwargs.has_key('startDate'):
        kwargs['startDate'] = rhn.encodeDate(kwargs['startDate'])
    if kwargs.has_key('endDate'):
        kwargs['endDate'] = rhn.encodeDate(kwargs['endDate'])
    try:
        return rhn.session.system.provisioning.snapshot.listSnapshots(rhn.key, server_id, kwargs) == 1
    except Exception, E:
        return rhn.fail(E,  'list system snapshots for server %s' % getServerName(rhn, server_id))

# --------------------------------------------------------------------------------- #

# -- system.search namespace -- #

def searchDeviceDescriptions(rhn, search_string):
    """
    API: system.search.deviceDescription

    usage: searchDeviceDescriptions(rhn, search_string)

    description:
    list the systems matching the device description
    The search string is not case sensitive

    returns: list of dict, one per server.

    parameters:
    rhn                      - an authenticated RHN session
    search-string(str)       - string to search for
    """
    try:
        return rhn.session.system.search.deviceDescription(rhn.key, search_string)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching device description "%s"' % search_string)

# --------------------------------------------------------------------------------- #


def searchDeviceDriver(rhn, search_string):
    """
    API: system.search.deviceDriver

    usage: searchDeviceDriver(rhn, search_string)

    description:
    list the systems matching the device driver given
    The search string is not case sensitive

    returns: list of dict, one per server.

    parameters:
    rhn                      - an authenticated RHN session
    search-string(str)       - string to search for
    """
    try:
        return rhn.session.system.search.deviceDriver(rhn.key, search_string)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching device driver "%s"' % search_string)

# --------------------------------------------------------------------------------- #

def searchDeviceId(rhn, search_string):
    """
    API: system.search.deviceId

    usage: searchDeviceId(rhn, search_string)

    description:
    list the systems matching the device Id given
    The search string is not case sensitive

    returns: list of dict, one per server.

    parameters:
    rhn                      - an authenticated RHN session
    search-string(str)       - string to search for
    """
    try:
        return rhn.session.system.search.deviceId(rhn.key, search_string)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching device Id "%s"' % search_string)

# --------------------------------------------------------------------------------- #

def searchDeviceVendorId(rhn, search_string):
    """
    API: system.search.deviceVendorId

    usage: searchDeviceDescriptions(rhn, search_string)

    description:
    list the systems matching the device description
    The search string is not case sensitive

    returns: list of dict, one per server.

    parameters:
    rhn                      - an authenticated RHN session
    search-string(str)       - string to search for
    """
    try:
        return rhn.session.system.search.deviceVendorId(rhn.key, search_string)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching device VendorId "%s"' % search_string)

# --------------------------------------------------------------------------------- #

def searchHostname(rhn, search_string):
    """
    API: system.search.hostname

    usage: searchDeviceDescriptions(rhn, search_string)

    description:
    list the systems matching the hostname provided
    The search string is not case sensitive

    returns: list of dict, one per server.

    parameters:
    rhn                      - an authenticated RHN session
    search-string(str)       - string to search for
    """
    try:
        return rhn.session.system.search.hostname(rhn.key, search_string)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching device driver "%s"' % search_string)

# --------------------------------------------------------------------------------- #
        
def searchIp(rhn, search_string):
    """
    API: system.search.ip

    usage: searchip(rhn, search_string)

    description:
    list the systems matching the IP given
    The search string is not case sensitive

    returns: list of dict, one per server.

    parameters:
    rhn                      - an authenticated RHN session
    search-string(str)       - string to search for
    """
    try:
        return rhn.session.system.search.ip(rhn.key, search_string)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching IP Address "%s"' % search_string)

# --------------------------------------------------------------------------------- #

def searchNameAndDescription(rhn, search_string):
    """
    API: system.search.NameAndDescription

    usage: searchNameAndDescription(rhn, search_string)

    description:
    list the systems matching the NameAndDescription given
    The search string is not case sensitive

    returns: list of dict, one per server.

    parameters:
    rhn                      - an authenticated RHN session
    search-string(str)       - string to search for
    """
    try:
        return rhn.session.system.search.nameAndDescription(rhn.key, search_string)
    except Exception, E:
        return rhn.fail(E, 'search for systems whose name or description match "%s"' % search_string)
