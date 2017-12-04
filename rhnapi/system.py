#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the 'system' namespace
# and all its children / sub-namespaces
#
# Copyright (c) 2009-2014 Stuart Sears
#
# This file is part of python-rhnapi
#
# python-rhnapi is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# python-rhnapi is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with python-rhnapi. If not, see http://www.gnu.org/licenses/.

__author__ = "Stuart Sears"

ent_names = { 'monitoring_entitled'              : 'monitoring',
              'provisioning_entitled'            : 'provisioning',
              'management_entitled'              : 'management',
              'virtualization_platform_entitled' : 'virtualization platform',
              'virtualization_host_entitled'     : 'virtualization',
            }

# ---------------------------------------------------------------------------- #

def addEntitlements(rhn, serverid, entlist):
    """
    API:
    system.addEntitlements

    usage:
    addEntitlements(rhn, serverid, entlist)

    description:
    Adds the list of entitlements to a given server ID

    returns:
    Bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID to add entitlements to
    entlist(list/str)        - a list of entitlement labels to add
                               entitlements that already exist are ignored.
    """
    try:
        return rhn.session.system.addEntitlements(rhn.key, serverid, entlist) == 1
    except Exception, E:
        return rhn.fail(E, "add entitlements %s to server ID %d (%s)" % (','.join(entlist) , serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def addNote(rhn, serverid, note):
    """
    API:
    system.addNote

    usage:
    addNote(rhn, serverid, note)

    Add a note to an existing serverid

    returns: 
    Bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID
    note(str)                - the note to add
    """
    try:
        return rhn.session.system.addNote(rhn.key, serverid, note) == 1
    except Exception, E:
        return rhn.fail(E, "add note to server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def applyErrata(rhn, serverid, errlist):
    """
    API:
    system.applyErrata

    usage:
    applyErrata(rhn, serverid, errlist)

    Applies the specifed list of errata to a server

    Deprecated. To be replaced by scheduleApplyErrata

    returns:
    Bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID
    errlist(list/int)       - list of erratum IDs to apply
    """
    try:
        return rhn.session.system.applyErrata(rhn.key, serverid, errlist) == 1
    except Exception, E:
        return rhn.fail(E, "apply errata to server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def comparePackages(rhn, serverid1, serverid2):
    """
    API:
    system.comparePackages

    usage:
    comparePackages(rhn, serverid1, serverid2)

    description:
    Compares installed package lists on 2 servers

    returns:
    list of dict, one per package
            { 'pkgname_id' :
    int
              'pkgname' :
    strs
              'this_system' :
    str (version on server1)
              'other_system' :
    str (version on server2)
              'comparison' :
    int }
        where the comparison integer means:
            * 0 - No difference.
            * 1 - Package on this system only.
            * 2 - Newer package version on this system.
            * 3 - Package on other system only.
            * 4 - Newer package version on other system.

    parameters:
    rhn                 - an authenticated RHN session
    serverid1(int)      - first server ID
    serverid2(int)      - second server ID
    """
    try:
        return rhn.session.system.comparePackages(rhn.key, serverid1, serverid2)
    except Exception, E:
        return rhn.fail(E, "compare packages on servers %d (%s) and %d (%s)" % (serverid1, getName(rhn, serverid1), serverid2, getName(rhn, serverid2)))

# ---------------------------------------------------------------------------- #

def comparePackageProfile(rhn, serverid, pkgprofile):
    """
    API:
    system.comparePackageProfile
    
    usage:
    comparePackageProfile(rhn, serverid, pkgprofile)
    
    description:
    Compares a system's package list against a saved package profile.
    
    returns:
    list of dict, one per package
            { 'pkgname_id' :
    int
              'pkgname' :
    strs
              'this_system' :
    str (version on specified system)
              'other_system' :
    str (version in package profile)
              'comparison' :
    int }
        where the comparison integer means:
            * 0 - No difference.
            * 1 - Package on this system only.
            * 2 - Newer package version on this system.
            * 3 - Package on other system only.
            * 4 - Newer package version on other system.

    returns:
    list of dict, one per package (for the union of all pkgs on system
    and in profile)
    
    parameters:
    rhn                 - an authenticated RHN session
    serverid(int)       - server ID
    pkgprofile(str)     - label of a saved package profile
    """
    try:
        return rhn.session.system.comparePackageProfile(rhn.key, serverid, pkgprofile)
    except Exception, E:
        return rhn.fail(E, 'compare packages on server %d (%s) to package profile %s' % (serverid, getName(rhn, serverid), pkgprofile))

# ---------------------------------------------------------------------------- #

def convertToFlexEntitlement(rhn, serverids, chanfamily):
    """
    API:
    system.convertToFlexEntitlement

    usage:
    convertToFlexEntitlement(rhn, serverids, chanlabel)

    description:
    Converts the given list of systems for a given channel family to use
    the flex entitlement.

    returns:
    int (number of converted systems)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    serverids(list/int)    - list of system ID numbers
    chanfamily(str)          - channel family label
    """
    try:
        return rhn.session.system.convertToFlexEntitlement(rhn.key, serverids, chanfamily)
    except Exception, E:
        return rhn.fail(E, 'convert systems to use flex entitlement for channel family %s' % chanfamily)

# ---------------------------------------------------------------------------- #

def createPackageProfile(rhn, serverid, label, description):
    """
    API:
    system.createPackageProfile

    usage:
    createPackageProfile(rhn, serverid, label, description)

    description:
    Create a new package profile for a given serverid.
    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    label(str)              - label for new package profile
    description(str)        - a description of the profile
    """
    try:
        rhn.session.system.createPackageProfile(rhn.key, serverid, label, description)
    except Exception, E:
        return rhn.fail(E, "create package profile %s for serverid %d (%s)" % (label, serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def createSystemRecord(rhn, serverid, kslabel):
    """
    API:
    system.createSystemRecord
    
    usage:
    createSystemRecord(rhn, serverid, kslabel)
    
    description:
    Creates a cobbler system record with the specified kickstart label
    
    returns:
    True, or throws exception
    
    parameters:
    rhn                  - an authenticated RHN session
    serverid(int)       - server ID
    """
    try:
        return rhn.session.system.createSystemRecord(rhn.key, serverid, kslabel) == 1
    except Exception, E:
        return rhn.fail(E, 'create cobbler system record for server ID %d (%s)' % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def deleteCustomValues(rhn, serverid, custvals):
    """
    API:
    system.deleteCustomValues
                  
    usage:
    deleteCustomValues(rhn, serverid, custvals)
                  
    description:
    delete the given custom values from the chosen system record.
                  
    returns:
    True, or throws exception
                  
    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID
    custvals(list/str)      - custom value name/label (or list of)
    """
    if not isinstance(custvals, list):
        custvals = [ custvals ]
    try:
        return rhn.session.system.deleteCustomValues(rhn.key, serverid, custvals) == 1
    except Exception, E:
        val_list = ','.join(custvals)
        return rhn.fail(E, 'delete one or more of custom values [%s] from server ID %d (%s)' % (val_list, serverid, getName(rhn, serverid)))
        
# ---------------------------------------------------------------------------- #

def deleteGuestProfiles(rhn, serverid, guestlist):
    """
    API:
    system.deleteGuestProfiles

    usage:
    deleteGuestProfiles(rhn, serverid, guestlist)

    description:
    deletes the specified list of guest profiles for the specified host.

    returns:
    True, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID
    guestlist(list/str)     - list of guest names to delete
    """
    try:
        return  rhn.session.system.deleteGuestProfiles(rhn.key, serverid, guestlist) == 1
    except Exception, E:
        return rhn.fail(E, 'remove guest profiles from server %s' % getName(rhn, serverid) )

# ---------------------------------------------------------------------------- #

def deleteNote(rhn, serverid, noteid):
    """
    API:
    system.deleteNote
            
    usage:
    deleteNote(rhn, serverid, noteid)
            
    description:
    deletes the given note from the specified server record
    
    returns:
    True, or throws exception
            
    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID
    noteid(int)             - note ID
    """
    try:
        return rhn.session.system.deleteNote(rhn.key, serverid, noteid) == 1
    except Exception, E:
        return rhn.fail(E, 'delete note %d from server %d (%s)' % (noteid, serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def deleteNotes(rhn, serverid):
    """
    API:
    system.deleteNotes
        
    usage:
    deleteNotes(rhn, serverid)
        
    description:
    deletes ALL notes from the given server record
            
    returns:
    True, or throws exception 
        
    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID
    """
    try:
        return rhn.session.system.deleteNotes(rhn, serverid) == 1
    except Exception, E:
        return rhn.fail(E, 'delete all notes from server id %d (%s)' % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def deletePackageProfile(rhn, profileid):
    """
    API:
    system.deletePackageProfile
        
    usage:
    deletePackageProfile(rhn, profileid)
        
    description:
    delete the specified package profile
        
    returns:
    True, or throws exception
        
    parameters:
    rhn                  - an authenticated RHN session
    profileid(int)      - saved package profile ID
    """
    try:
        return rhn.session.system.deletePackageProfile(rhn, profileid) == 1
    except Exception, E:
        return rhn.fail(E, 'delete package profile ID %d' % profileid)

# ---------------------------------------------------------------------------- #

def deleteSystems(rhn, serverids):
    """
    API:
    system.deleteSystems
    
    usage:
    deleteSystems(rhn, serverids)
    
    description:
    Delete systems given a list of system ids
    
    parameters:
    rhn                     - an authenticated RHN session
    serverids([int])        - list of server IDs from RHN
    """
    try:
        return rhn.session.system.deleteSystems(rhn.key, serverids) == 1
    except Exception, E:
        return rhn.fail(E, "delete one or more of systems: [ %s ]" % (",".join([ str(x) for x in serverids ])))

# ---------------------------------------------------------------------------- #

def downloadSystemId(rhn, serverid):
    """
    API:
    system.downloadSystemId
    
    usage:
    downloadSystemId(rhn, serverid)
        
    description:
    downloads the serverid file (/etc/sysconfig/rhn/systemid) for a given serverid.
    
    returns:
    string (contents of systemid file)
    
    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)           - server ID number
    """
    try:
        return rhn.session.system.downloadSystemId(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "download the serverid for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getBaseChannel(rhn, serverid):
    """
    API:
    none, special case of system.getSubscribedBaseChannel

    usage:
    getBaseChannel(rhn, serverid)
    
    description:
    returns the label of the given system's base channel
    
    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getSubscribedBaseChannel(rhn.key, serverid)['label']
    except Exception, E:
        return rhn.fail(E, "retrieve Subscribed Base Channel information for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getChildChannels(rhn, serverid):
    """
    API:
    none, special case of system.listSubscribedChildChannels

    usage:
    getChildChannels(rhn, serverid)
    
    description:
    returns a list of labels of the system subscribed child channels
    
    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        print "Determining child channels subscribed for server %d" % serverid
        ccarray = rhn.session.system.listSubscribedChildChannels(rhn.key, serverid)
        return [ x['label'] for x in ccarray ]
    except Exception, E:
        return rhn.fail(E, "retrieve Subscribed Child Channel information for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getConnectionPath(rhn, serverid):
    """
    API:
    system.getConnectionPath
        
    usage:
    getConnectionPath(rhn, serverid)
        
    description:
    Get the list of proxies that the given system connects through in order to reach the server.
        
    returns:
    list of dict, one per proxy
            {
            'position' : (int) position in list, 1 being nearest the system
            'id'       : (int) proxy system id
            'hostname' : (str) proxy hostname
            }
        
    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    """
    try:
        return rhn.session.system.getConnectionPath(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, 'get list of proxies for server id %d (%s)' % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getCpu(rhn, serverid):
    """
    API:
    system.getCpu
    
    usage:
    getCpu(rhn, serverid)
    
    description:
    returns CPU information for a given server
    
    returns:
    dict
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
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getCpu(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve CPU information for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getCustomValues(rhn, serverid):
    """
    API:
    system.getCustomValues
    
    usage:
    getCustomValues(rhn, serverid)
    
    description:
    returns CPU information for a given server
    
    returns:
    dict: { 'custom info label' : data }
    
    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getCustomValues(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve Custom Values set for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getDetails(rhn, serverid):
    """
    API:
    system.getDetails
    
    usage:
    getDetails(rhn, serverid)
    
    description:
    gets detailed information about the chosen server, including location, OS, entitlements etc
    
    returns:
    dict
            { 'auto_update' : bool,
              'release' : str,
              'address1' : str,
              'address2' : str,
              'city' : str,
              'country' : str,
              'state' : str,
              'building' : str,
              'rack' : str,
              'room' : str, 
              'description' : str,
              'hostname' : str,
              'last_boot' : dateTime.iso8601,
              'lock_status' : bool,
              'id' : int,
              'profile_name' : str,
              'base_entitlement' :     str, one of ['enterprise_entitled' 'sw_mgr_entitled' ]
              'addon_entitlements' : [str]  - [ 'monitoring_entitled', 'provisioning_entitled', 
                                                'virtualization_host', 'virtualization_host_platform' ]
              'osa_status' : str (one of 'unknown', 'offline', 'online']
            }
    
    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getDetails(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve detailed information for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getDevices(rhn, serverid):
    """
    API:
    system.getdevices
    
    usage:
    getDevices(rhn, serverid)
    
    description:
    lists devices for the given system
    
    returns:
    list of dict, one per device:
            { 'device' : str,
              'device_class' : str,
              'driver' : str,
              'description' : str,
              'bus' : str,
              'pcitype' : str
            }
            
    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getDevices(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve device list for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getDmi(rhn, serverid):
    """
    API:
    system.getDmi
    
    usage:
    getDmi(rhn, serverid)
    
    description:
    returns DMI information (BIOS Vendor etc etc)
    returns:
    dict
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
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getDmi(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve DMI information for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getEntitlements(rhn, serverid):
    """
    API:
    system.getEntitlements
    
    usage:
    getEntitlements(rhn, serverid)
    
    description:
    gets the list of entitlements for a given server ID

    returns:
    list of string (entitlement labels)

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)           - server ID to add entitlements to
    """
    try:
        return rhn.session.system.getEntitlements(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, 'list entitlements for system ID %d' % (serverid))

# ---------------------------------------------------------------------------- #

def getEventHistory(rhn, serverid):
    """
    API:
    system.getEventHistory
        
    usage:
    getEventHistory(rhn, serverid)
            
    description:
    Returns a list history items associated with the system, ordered from newest to oldest.
    Note that the details may be empty for events that were scheduled against the system
    (as compared to instant).
    For more information on such events, see the system.listSystemEvents operation. 
            
    returns:
    list of dict, one per history event
            { 'completed' : dateTime.iso8601,
              'summary' : str,
              'details' : str
            }
            
    parameters:
    rhn                  - an authenticated RHN session
    serverid(int)           - server ID to add entitlements to
    """
    try:
        return rhn.session.system.getEventHistory(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, 'get even history for server ID %d (%s)' % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getId(rhn, servername):
    """
    API:
    system.getId
    
    usage:
    getId(rhn, servername)
    
    description
    look up a system ID for a given name. There may be more than one of these, as
    profile names are not guaranteed to be unique.
    
    returns:
    list of dict, one per matching system ID
            { 'id' : int,
              'name' : str,
              'last_checkin' : dateTime.iso8601
            }
    
    parameters:
    rhn                      - an authenticated RHN session
    servername(str)         - server name (often hostname)
    """
    try:
        return rhn.session.system.getId(rhn.key, servername)
    except Exception, E:
        return rhn.fail(E, "get system id(s) for server %s" % (servername))

# ---------------------------------------------------------------------------- #

def getLastCheckin(rhn, serverid):
    """
    API:
    none, custom method

    usage:
    getLastCheckin(rhn, serverid)
    
    description:
    returns an xmlrpclib.DateTime object representing the system"s last known
    checkin date, for use in comparisons.
    

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return getName(rhn, serverid)['last_checkin']
    except Exception, E:
        return rhn.fail(E, "get last check-in sate for serverid %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getMemory(rhn, serverid):
    """
    API:
    system.getMemory

    usage:
    getMemory(rhn, serverid)

    description:
    returns Memory information for a given server

    returns:
    dict:
        { 'ram' : (int) physical memory in Mb
          'swap' : (int) swap space in Mb
        }

    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getMemory(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve Memory information for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getName(rhn, serverid):
    """
    API:
    system.getName
        
    usage:
    getName(rhn, serverid)
        
    description:
    Get system name and last check in information for the given system ID.
            
    returns:
    dict
            { 'id' : int,
              'name' : str,
              'last_checkin' : dateTime.iso8601
            }
        
    parameters:
    rhn                     - an authenticated RHN session
    """
    try:
        return rhn.session.system.getName(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, 'get Name and last checkin for server ID %d' % serverid)

# ---------------------------------------------------------------------------- #

def getNetwork(rhn, serverid):
    """
    API :
    system.getNetwork

    usage:
    getNetwork(rhn, serverid)
    
    description:
    returns IP address and hostname for the given server

    returns:
    dict
        { 'ip' : (str) IP Address
          'hostname' : (str) Hostname
        }

    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getNetwork(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve Network information for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getNetworkDevices(rhn, serverid):
    """
    API:
    system.getNetworkDevices

    usage:
    getNetworkDevices(rhn, serverid)
    
    description:
    returns NetworkDevices information for a given server

    returns:
    list of dict, one per interface
        { 'ip' : (str)
          'interface' : (str)
          'netmask' : (str)
          'hardware_address' : (str)
          'module' : (str)
          'broadcast' : (str)
        }
        
    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getNetworkDevices(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve Network Device information for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getRegistrationDate(rhn, serverid):
    """
    API:
    system.getRegistrationDate

    usage:
    getRegistrationDate(rhn, serverid)
    
    description:
    Returns the date the system was registered.

    returns:
    DateTime.iso8601

    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getRegistrationDate(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve the Registration Date for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getRelevantErrata(rhn, serverid):
    """
    API:
    system.getRelevantErrata

    usage:
    getRelevantErrata(rhn, serverid)

    description:
    getRelevantErrata(rhn, serverid)

    returns:
    list of dict, one per erratum
        { 'id' : (int) Erratum ID
          'date' : (str) date the erratum was created
          'advisory_synopsis': (str)
          'errtype' : (str)
          'advisory_name' : (str)
        }

    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getRelevantErrata(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "get relevant errata for server ID (%d) (%s)" % (serverid, getName(rhn, serverid)))


# ---------------------------------------------------------------------------- #

def getRelevantErrataByType(rhn, serverid, errtype):
    """
    API:
    system.getRelevantErrataByType

    usage:
    getRelevantErrata(rhn, serverid, errtype)

    description:
    getRelevantErrata(rhn, serverid)

    returns:
    list of dict, one per erratum
        { 'id' : (int) Erratum ID
          'date' : (str) date the erratum was created
          'advisory_synopsis': (str)
          'errtype' : (str)
          'advisory_name' : (str)
        }

    params:
    rhn                      - an authenticated RHN session
    serverid(int)           - server ID number
    errtype(str)       - type of advisory. One of ['Security Advisory', 'Product Enhancement Advisory', 'Bug Fix Advisory' ] 
    """
    try:
        return rhn.session.system.getRelevantErrata(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "get relevant errata of type %s for server ID (%d) (%s)" % ( errtype, serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getRelevantSecurityErrata(rhn, serverid):
    """
    API:
    none, custom method
    returns getRelevantErrataByType with a 'Security Advisory' argument
    """
    try:
        return getRelevantErrataByType(rhn.key, serverid, errtype = 'Security Advisory')
    except Exception, E:
        return rhn.fail(E, "get security errata for server ID (%d) (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getRelevantBugfixErrata(rhn, serverid):
    """
    API:
    none, custom method
    returns getRelevantErrataByType with a 'Bug Fix Advisory' argument
    """
    try:
        return getRelevantErrataByType(rhn.key, serverid, errtype = 'Bug Fix Advisory')
    except Exception, E:
        return rhn.fail(E, "get security errata for server ID (%d) (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getRelevantEnhancementErrata(rhn, serverid):
    """
    API:
    none, custom method
    returns getRelevantErrataByType with a 'Product Enhancement Advisory' argument
    """
    try:
        return getRelevantErrataByType(rhn.key, serverid, errtype = 'Product Enhancement Advisory')
    except Exception, E:
        return rhn.fail(E, "get security errata for server ID (%d) (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getRunningKernel(rhn, serverid):
    """
    API:
    system.getRunningKernel

    usage:
    getRunningKernel(rhn, serverid)
    
    description:
    Returns the running kernel of the given system.

    returns:
    string
    
    params:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    """
    try:
        return rhn.session.system.getRunningKernel(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve running kernel information for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getScriptActionDetails(rhn, actionid):
    """
    API:
    system.getScriptActionDetails

    usage:
    getScriptActionDetails(rhn, actionid)

    description:
    Returns script details for script run actions

    returns:
    dict,
        {
            "id" : (int)action id
            "content" : (str) script content
            "run_as_user" : (str) Run as user
            "run_as_group" : (str) Run as group
            "timeout" : (int) Timeout in seconds
            [
                # one entry for each server this script ran on, like this:
                {
                "serverId" : (int) ID of the server the script runs on.
                "startDate" : (dateTime.iso8601) Time script began execution.
                "stopDate" : (dateTime.iso8601) Time script stopped execution.
                "returnCode" : (int) Script execution return code.
                "output" : (str)Output of the script
                }

        }
    """
    try:
        return rhn.session.system.getScriptActionDetails(rhn.key, actionid)
    except Exception, E:
        return rhn.fail(E, 'get script action information for action ID %d' % actionid)

# ---------------------------------------------------------------------------- #

def getScriptResults(rhn, actionid):
    """
    API:
    system.getScriptResults

    usage:
    getScriptResults(rhn, actionid)

    description:
    Fetch results from a script execution. Returns an empty list if no results are yet available.

    returns:
    list of dict
        { 'serverId'   : (int)
          'startDate'  : (DateTime)
          'stopDate'   : (DateTime)
          'returnCode' : (int)
          'output'     : (str)
        }
    
    params:
    rhn                      - an authenticated RHN session
    actionid(int)           - Id for the scheduled action that runs the script.
    """
    try:
        return rhn.session.system.getScriptResults(rhn.key, actionid)
    except Exception, E:
        return rhn.fail(E, "retrieve results for script ID %d" % actionid)

# ---------------------------------------------------------------------------- #

def getSubscribedBaseChannel(rhn, serverid):
    """
    API:
    getSubscribedBaseChannel

    usage:
    getSubscribedBaseChannel(rhn, serverid)

    description:
    returns details of the base channel for a given server

    returns:
    dict
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
    serverid(int)           - server ID number
    """
    try:
        return rhn.session.system.getSubscribedBaseChannel(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve base channel information for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getUnscheduledErrata(rhn, serverid):
    """
    API:
    system.getScheduledErrata

    usage:
    getUnscheduledErrata(rhn, serverid)

    description:
    Provides an array of errata that are applicable to a given system.

    returns:
    list of dict, one per erratum
        { 'id' : (int) Erratum ID
          'date' : (str) date the erratum was created
          'advisory_synopsis': (str)
          'errtype' : (str)
          'advisory_name' : (str)
        }
    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getUnscheduledErrata(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve Unscheduled Errata information for server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def getVariables(rhn, serverid):
    """
    API:
    system.getVariables

    usage:
    getVariables(rhn, serverid)

    description:
    Lists kickstart variables set in the system record for the specified server.
    Note:
    This call assumes that a system record exists in cobbler for the given system and will raise an XMLRPC fault if that is not the case.
    To create a system record over xmlrpc use system.createSystemRecord
    To create a system record in the Web UI please go to System -> -> Provisioning -> Select a Kickstart profile -> Create Cobbler System Record.

    returns:
    dict
        {'netboot_enabled' : (bool)
         'kickstart_variables': (list of dict)
            [ {'key' : (str),
               'value' : (str or int) }
               ...
            ]
        }

    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.getVariables(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve kickstart variables for server  ID %d (%s)" % (serverid, getName(rhn, serverid))) 

# ---------------------------------------------------------------------------- #

def isNvreInstalled(rhn, serverid, name, version, release, epoch=None):
    """
    API:
    system.isNvreInstalled

    usage:
    isNvreInstalled(rhn, serverid, pName, pVersion, pRelease, pEpoch = "")

    description:
    Check if the package with the given NVRE is installed on given system

    params:   (* = optional)
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    name(str)               - name of the RPM package
    version(str)            - RPM package version
    release(str)            - RPM package release
    epoch(str)*             - RPM package epoch (if there is one)

    """
    pkgstr = '-'.join([name, version, release])
    try:
        if epoch is not None:
            return rhn.session.system.isNvreInstalled(rhn.key, serverid, name, version, release, epoch) == 1
        else:
            return rhn.session.system.isNvreInstalled(rhn.key, serverid, name, version, release) == 1
    except Exception, E:
        return rhn.fail(E, "determine if the given package %s is installed on server ID %d (%s)" %(pkgstr, serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def joinSystemGroup(rhn, serverid, grpid):
    """
    API:
    none, special case of system.setGroupMembership

    usage:
    joinSystemGroup(rhn, serverid, grpid)

    description:
    adds the given server id to/from the given groupid.
    
    returns:
    bool, or throws exception
    
    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server to manage
    grpid(int)              - server group id
    """
    try:
        return rhn.session.system.setGroupMembership(rhn.key, serverid, grpid, 1) == 1
    except Exception, E:
        return rhn.fail(E,'set group membership for server id %d' % (serverid))

# ---------------------------------------------------------------------------- #

def leaveSystemGroup(rhn, serverid, grpid):

    """
    API:
    none, special case of
    system.setGroupMembership

    usage:
    leaveSystemGroup(rhn, serverid, grpid)

    description:
    removes the given server id from the given groupid
    
    returns:
    bool, or throws exception
    
    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server to manage
    grpid(int)              - server group id
    """
    try:
        return rhn.session.system.setGroupMembership(rhn.key, serverid, grpid, 0 ) == 1
    except Exception, E:
        return rhn.fail(E,'set group membership for server id %d' % (serverid))

# ---------------------------------------------------------------------------- #

def listActivationKeys(rhn, serverid):
    """
    API:
    system.listActivationKeys

    usage:
    listActivationKeys(rhn, serverid)

    description: 
    List the activation keys the system was registered with.
    An empty list will be returned if an activation key was not used during registration.

    returns:
    list of activation keys (hex strings)

    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.listActivationKeys(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "List activation keys used to register server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def listActiveSystems(rhn):
    """
    API:
    system.listActiveSystems

    usage:
    listActiveSystems(rhn)
    
    description:
    returns a list of active systems for the logged-in user

    returns:
    list of dict, one per active system
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

# ---------------------------------------------------------------------------- #

def listAdministrators(rhn, serverid):
    """
    API:
    system.listAdministrators

    usage:
    listAdministrators(rhn, serverid)
    
    description:
    Returns a list of users which can administer the system

    returns:
    list of dict, one per user
        {'login_uc': (str) uppercased login,
         'login': (str),
         'enabled': (bool),
         'id': (int)
        }
    
    params:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.listAdministrators(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "retrieve Administrator list for serverid %d" % (serverid))

# ---------------------------------------------------------------------------- #

def listBaseChannels(rhn, serverid):
    """
    API:
    system.listBaseChannels

    usage:
    listBaseChannels(rhn, serverid)

    description:
    lists the available base channels - RH originals and clones of them!
    Deprecated - use system.listSubscribableBaseChannels instead

    returns:
    list of dict, one per channel
        {
        "id"           : Base Channel ID.
        "name"         : Name of channel.
        "label"        : Label of Channel
        "current_base" : 1 indicates it is the current base channel

        }

    params:
    rhn - an authenticated RHN session
    serverid(int) - the serverid to investigate
    """
    try:
        return rhn.session.system.listBaseChannels(rhn.key, serverid)
    except Exception, E:
        return rhn.fail("E", "list Base Channels available to server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def listChildChannels(rhn, serverid):
    """
    API:
    system.listChildChannels

    usage:
    listChildChannels(rhn, serverid)

    description:
    Returns a list of subscribable child channels.
    This only shows channels the system is *not* currently subscribed to. 
    Deprecated - use system.listSubscribableChildChannels instead

    returns:
    list of dict, one per available child channel
        {   "id" : (int) channel id
            "name" : channel name
            "label" : channel label
            "summary" : channel summary
            "has_license" : (str)
            "gpg_key_url" : (str)
        }
        
    params:
    rhn - an authenticated RHN session
    serverid(int) - the serverid to investigate
    """
    try:
        return rhn.session.system.listChildChannels(rhn.key, serverid)
    except Exception, E:
        return rhn.fail("E", "list Child Channels available to Server ID %d (%s)" % (serverid), getName(rhn, serverid))

# ---------------------------------------------------------------------------- #

def listDuplicatesByHostname(rhn):
    """
    API:
    system.listDuplicatesByHostname

    usage:
    listDuplicatesByHostname(rhn)

    description:
    List duplicate systems by Hostname

    returns:
    list of dict, one per group of dupes (per hostname)
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

# ---------------------------------------------------------------------------- #

def listDuplicatesByIp(rhn):
    """
    API:
    system.listDuplicatesByIp

    usage:
    listDuplicatesByIp(rhn)

    description:
    List duplicate systems by IP Address

    returns:
    list of dict, one per group of dupes (per hostname)
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

# ---------------------------------------------------------------------------- #

def listDuplicatesByMac(rhn):
    """
    API:
    system.listDuplicatesByMac

    usage:
    listDuplicatesByMac(rhn)

    description:
    List duplicate systems by Mac

    returns:
    list of dict, one per group of dupes (per hostname)
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

# ---------------------------------------------------------------------------- #

def listEligibleFlexGuests(rhn):
    """
    API:
    system.listEligibleFlexGuests

    usage:
    listEligibleFlexGuests(rhn)

    description:
    List eligible flex guests accessible to the user 

    returns:
    list of dict, one per channel family
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

# ---------------------------------------------------------------------------- #

def listFlexGuests(rhn):
    """
    API:
    system.listFlexGuests

    usage:
    listFlexGuests(rhn)

    description:
    List  flex guests accessible to the user 

    returns:
    list of dict, one per channel family
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

# ---------------------------------------------------------------------------- #

def listGroups(rhn, serverid):
    """
    API:
    system.listGroups

    usage:
    listGroups(rhn, serverid)
    
    description:
    lists the available groups for a given serverid

    returns:
    list of dict, one per system group
        {
        "id"                : (int) server group id
        "subscribed"        : (int) 1 if the given server is subscribed to this server group, 0 otherwise
        "system_grpname" : (str) Name of the server group
        "sgid"              : (int) server group id (Deprecated)
        }

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.listGroups(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "list available groups for server ID %d (%s) " % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def listInactiveSystems(rhn, days=None):
    """
    API:
    system.listInactiveSystems

    usage:
    listInactiveSystems(rhn, days)

    description:
    Lists systems that have been inactive for the default period of inactivity,
    or for the given number of days.
    
    returns:
    list of dict, one per system
        { 
        'id' : (int) server id
        'last_checkin' : DateTime.iso8601
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

# ---------------------------------------------------------------------------- #

def listLatestAvailablePackage(rhn, serverids, pkgname):
    """
    API:
    system.listLatestAvailablePackage

    usage:
    listLatestAvailablePackage(rhn, serverids, pkgname)

    description:
    Get the latest available version of a package for each system 

    returns:
    list of dict, one per system
        {
        'id'      : (int) server ID
        'name'    : (str) server name
        'package' : {
                    'id'      : (int) package id
                    'name'    : (str) package name
                    'version' : (str)
                    'release' : (str)
                    'epoch'   : (str)
                    'arch'    : (str)
                    }

        }

    params:
    rhn(rhnSession)             - authenticated, active rhnapi.rhnSession object
    serverids(list)            - list of int, server IDs
    pkgname(str)           - the package name to look for
    """
    try:
        return rhn.session.system.listLatestAvailablePackage(rhn.key, serverids, pkgname)
    except Exception, E:
        return rhn.fail(E, 'list latest versions of %s for the given lits of servers' % pkgname)

# ---------------------------------------------------------------------------- #

def listLatestInstallablePackages(rhn, serverid):
    """
    API:
    system.listLatestInstallablePackages

    usage:
    listLatestInstallablePackages(rhn, serverid)
    
    description:
    lists the latest installable packages for a given serverid

    returns:
    list of dict, one per installable package
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
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.listLatestInstallablePackages(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "list latest installable packages for server id %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def listLatestUpgradablePackages(rhn, serverid):
    """
    API:
    system.listLatestUpgradeablePackages

    usage:
    listLatestUpgradeablePackages(rhn, serverid)
    
    description:
    lists the latest upgradeable packages for a  given serverid
    
    returns:
    list of dict, one per package:
        {
        "name"
        "arch"
        "from_version"
        "from_release"
        "from_epoch"
        "to_version"
        "to_release"
        "to_epoch"
        "to_pkgid"
        }

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.listLatestUpgradablePackages(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "list latest Upgradeable packages for serverid %d (%s) " % (serverid, getName(rhn, serverid)))


def listLatestUpgradeablePackages(rhn, serverid):
    """
    Compatibility layer for listLatestUpgradablePackages
    :param rhn:
    :param serverid:
    :return:
    """
    return listLatestUpgradablePackages(rhn, serverid)

# ---------------------------------------------------------------------------- #

def listNewerInstalledPackages(rhn, serverid, pkgname, pkgver, pkgrel, pkgepoch=""):
    """
    API:
    system.listNewerInstalledPackages

    usage:
    listNewerInstalledPackages(rhn, serverid, pkgname, pkgver, pkgrel, pkgepoch)

    description:    
    Given a package name, version, release, and epoch, returns the list of packages
    installed on the system with the same name that are newer.

    returns:
    list of dict, one per package
        {
        "name"
        "version"
        "release"
        "epoch"
        }
    
    parameters: (* = optional)
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    pkgname(str)            - package name
    pkgver(str)             - package version
    pkgrel(str)             - package release
    *pkgepoch(str)          - package epoch
    """
    if pkgepoch.strip() != '':
        pkginfo = "%s:%s-%s-%s" %(pkgepoch, pkgname, pkgver, pkgrel)
    else:
        pkginfo = "%s-%s-%s" %(pkgname, pkgver, pkgrel)
    try:
        return rhn.session.system.listNewerInstalledPackages(rhn, serverid, pkgname, pkgver, pkgrel, pkgepoch)
    except Exception, E:
        return rhn.fail(E, "List installed packages newer than %s on server %d (%s) " % ( pkginfo, serverid, getName(rhn, serverid) ) )

# ---------------------------------------------------------------------------- #

def listNotes(rhn, serverid):
    """
    API:
    system.listNotes

    usage:
    listNotes(rhn, serverid)

    description:
    Provides a list of notes associated with a system. 

    returns:
    list of dict, one per note
        {
        "id"        : (int) note ID
        "subject"   : (str) Subject of the note
        "note"      : (str) Contents of the note
        "system_id" : (str) The id of the system associated with the note
        "creator"   : (str) Creator of the note
        }
    
    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.listNotes(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, 'list notes for system %d (%s)'%(serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def listOlderInstalledPackages(rhn, serverid, pkgname, pkgver, pkgrel, pkgepoch="" ):
    """
    API:
    system.listOlderInstalledPackages

    usage:
    listOlderInstalledPackages(rhn, serverid, serverid, pkgname, pkgver, pkgrel, pkgepoch)
    
    description:
    Given a package name, version, release, and epoch, returns the list of packages
    installed on the system with the same name that are older.
    
    returns:
    list of dict, one per package
        {
        "name"
        "version"
        "release"
        "epoch"
        }
    
    parameters: (* = optional)
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    pkgname(str)            - package name
    pkgver(str)             - package version
    pkgrel(str)             - package release
    *pkgepoch(str)          - package epoch
    """
    if pkgepoch.strip() != '':
        pkginfo = "%s:%s-%s-%s" %(pkgepoch, pkgname, pkgver, pkgrel)
    else:
        pkginfo = "%s-%s-%s" %(pkgname, pkgver, pkgrel)
    try:
        return rhn.session.system.listOlderInstalledPackages(rhn, serverid, serverid, pkgname, pkgver, pkgrel, pkgepoch)
    except Exception, E:
        return rhn.fail(E, "List installed packages older than %s on server %d (%s)" % (pkginfo, serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def listOutOfDateSystems(rhn):
    """
    API:
    system.listOutOfDateSystems

    usage:
    listOutOfDateSystems(rhn)

    description:
    Returns list of systems needing package updates
    
    returns:
    list of dict, one per system
        {
        'id'            : (int)
        'name'          : (str)
        'last_checkin'  : (DateTime.iso8601)
        }

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.listOutOfDateSystems(rhn.key)
    except Exception, E:
        return rhn.fail(E, "get a list of out of date systems")

# ---------------------------------------------------------------------------- #

def listPackageProfiles(rhn):
    """
    API:
    system.listPackageProfiles

    usage:
    listPackageProfiles(rhn)

    description:
    List the package profiles for this organization

    returns:
    list of dict, one per profile
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

# ---------------------------------------------------------------------------- #

def listPackages(rhn, serverid):
    """
    API:
    system.listPackages

    usage:
    listPackages(rhn, serverid)

    description:
    List the installed packages for a given system    

    returns:
    list of dict, one per installed package
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
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.listPackages(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "Get a list of installed packages for server %d" % (serverid))

# ---------------------------------------------------------------------------- #

def listPackagesFromChannel(rhn, serverid, chanlabel):
    """
    API:
    system.listPackagesFromChannel

    usage:
    listPackagesFromChannel(rhn, serverid, chanlabel)

    List the installed packages for a given system that are from a specific channel.

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    chanlabel(str)          - Channel label
    """
    try:
        return rhn.session.system.listPackagesFromChannel(rhn, serverid, chanlabel)
    except Exception, E:
        return rhn.fail(E, "Get a list of installed packages for server %d from channel %s" % (serverid, chanlabel))


# ---------------------------------------------------------------------------- #

def listSubscribableBaseChannels(rhn, serverid):
    """
    API:
    system.listSubscribableBaseChannels

    usage:
    listSubscribableBaseChannels(rhn, serverid)

    description:
    lists the available base channels - RH originals and clones of them!

    returns:
    list of dict, one per channel
        {
        "id"           : Base Channel ID.
        "name"         : Name of channel.
        "label"        : Label of Channel
        "current_base" : 1 indicates it is the current base channel

        }

    params:
    rhn                     - an authenticated RHN session
    serverid(int)           - the serverid to investigate
    """
    try:
        return rhn.session.system.listSubscribableBaseChannels(rhn.key, serverid)
    except Exception, E:
        return rhn.fail("E", "list Base Channels available to server ID %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def listSubscribableChildChannels(rhn, serverid):
    """
    API:
    system.listSubscribableChildChannels

    usage:
    listSubscribableChildChannels(rhn, serverid)

    description:
    Returns a list of subscribable child channels.
    This only shows channels the system is *not* currently subscribed to. 

    returns:
    list of dict, one per available child channel
        {   "id" : (int) channel id
            "name" : channel name
            "label" : channel label
            "summary" : channel summary
            "has_license" : 
            "gpg_key_url" :
        }
        
    params:
    rhn                     - an authenticated RHN session
    serverid(int)           - the serverid to investigate
    """
    try:
        return rhn.session.system.listSubscribableChildChannels(rhn.key, serverid)
    except Exception, E:
        return rhn.fail("E", "list Child Channels available to Server ID %d (%s)" % (serverid), getName(rhn, serverid))

# ---------------------------------------------------------------------------- #

def listSubscribedChildChannels(rhn, serverid):
    """
    API:
    system.listSubscribedChildChannels

    usage:
    listSubscribedChildChannels(rhn, serverid)

    description:
    List the child channels a system is subscribed to

    returns:
    list of dict, each representing a channel
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
    serverid(int)            - server ID number
    """
    try:
        return rhn.session.system.listSubscribedChildChannels(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "list subscribed child channels for server %d" % (serverid))

# ---------------------------------------------------------------------------- #

def listSystemEvents(rhn, serverid):
    """
    API:
    system.listSystemEvents

    usage:
    listSystemEvents(rhn, serverid)

    description:
    List all system events for given server.
    This is *all* events for the server since it was registered.
    This may require the caller to filter the results to fetch the
    specific events they are looking for

    returns:
    list of dict, one per event.
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
    "additional_info"   :
    list of dict, as below:
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
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    """
    try:
        return rhn.session.system.listSystemEvents(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, "Get a list of system events for server %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def listSystems(rhn, rhnuser=None):
    """
    API:
    system.listSystems

    usage:
    listUserSystems(rhn, rhnuser)

    description:
    lists the systems registered / managed by a given username.
    org admins get all registered systems    

    returns:
    list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser                 - RHN user account
    """
    if rhnuser == None:
        rhnuser = rhn.login
    try:
        return rhn.session.system.listUserSystems(rhn.key, rhnuser)
    except Exception, E:
        return rhn.fail(E, "list systems for user %s" % (rhnuser))

# ---------------------------------------------------------------------------- #

def listSystemsWithPackageId(rhn, pkgid):
    """
    API:
    system.listSystemsWithPackage

    usage:
    listSystemsWithPackageId(rhn, pkgid)

    description:
    Lists the systems that have the given installed package (identified by its RHN packageId)

    returns:
    list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters:
    rhn                     - an authenticated RHN session
    pkgid(int)              - package ID number
    """
    try:
        return rhn.session.system.listSystemsWithPackage(rhn.key, pkgid)
    except Exception, E:
        return rhn.fail(E,'list systems with package ID %d installed' % pkgid)

# ---------------------------------------------------------------------------- #

def listSystemsWithPackageNVR(rhn, pkgname, pkgver, pkgrel):
    """
    API:
    system.listSystemsWithPackage

    usage:
    listSystemsWithPackage(rhn, pkgname, pkgver, pkgrelease)

    description:
    Lists the systems with the given package installed (identified by name, version and release)

    returns:
    list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters:
    rhn                     - an authenticated RHN session
    pkgname(str)            - package name
    pkgver(str)             - package version
    pkgrel(str)             - package release
    """
    pkginfo = "%s-%s-%s" %(pkgname, pkgver, pkgrel)
    try:
        return rhn.session.system.listSystemsWithPackage(rhn.key, pkgname, pkgver, pkgrel)
    except Exception, E:
        return rhn.fail(E,'list systems with package "%s" installed' % pkginfo)

# ---------------------------------------------------------------------------- #

def listUngroupedSystems(rhn):
    """
    API:
    system.listUngroupedSystems

    usage:
    listUngroupedSystems(rhn)
    
    description:
    List systems that are not members of any system group

    
    returns:
    list of dict, one per system
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
        return rhn.fail(E, "list systems which are not in any system groups")

# ---------------------------------------------------------------------------- #

def listUserSystems(rhn, rhnuser=None):
    """
    API:
    system.listUserSystems

    usage:
    listUserSystems(rhn, rhnuser)

    description:
    lists the systems registered / managed by a given username.
    org admins get all registered systems.
    If no username is supplied, this will behave exactly the same as system.listSystems

    returns:
    list of dict, one per system
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

# ---------------------------------------------------------------------------- #

def listVirtualGuests(rhn, vhostid):
    """
    API:
    system.listVirtualGuests

    usage:
    listVirtualGuests(rhn, vhostid)

    description:
    Lists the virtual guests for a given virtual host ID

    returns:
    list of dict, one per virtual guest
        {
        'id'           : (int) serverid
        'name'         : (str) profilename
        'last_checkin' : (DateTime)
        'uuid'         : (str) VM uuid
        'guestname'   : (str) VM name, from the virtual host
        }

    parameters:
    rhn                     - an authenticated RHN session
    vhostid(int)            - Server ID for virtual host system
    """
    try:
        return rhn.session.system.listVirtualGuests(rhn.key, vhostid)
    except Exception, E:
        return rhn.fail(E,'list virtual guests on host with sid %d' % (vhostid))

# ---------------------------------------------------------------------------- #

def listVirtualHosts(rhn):
    """
    API:
    system.listVirtualHosts

    usage:
    listVirtualHosts(rhn)

    description:
    Lists the virtual hosts visible to the logged-in user 

    returns:
    list of dict, one per system
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

# ---------------------------------------------------------------------------- #

def obtainReactivationKey(rhn, server_cert_or_id):
    """
    API:
    system.obtainReactivationKey

    usage:
    obtainReactivationKey(rhn, server_cert_or_id)

    description:
    obtains a reactivation key for an existing system
    
    returns:
    string (the reactivation key)

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

# ---------------------------------------------------------------------------- #

def provisionSystem(rhn, serverid, kslabel, earliest_start=None):
    """
    API:
    system.provisionSystem
    
    usage:
    provisionSystem(rhn, serverid, kslabel, *earliest_start)

    description:
    provision the given system using the specified kickstart profile
    The optional 'earliest_start' parameter can specify a time after which the
    provisioning will take place.

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)          - server id
    kslabel(str)            - kickstart profile label
    earliest_start(str)     - earliest occurence. This is a string in iso8601 format
                              "%Y%m%dT%H:%M:%S", e.g. 20110401T11:12:35
    """
    try:
        if earliest_start is not None:
            return isinstance(rhn.session.system.provisionSystem(rhn.key, serverid, kslabel, earliest_start), int)
        else:
            return isinstance(rhn.session.system.provisionSystem(rhn.key, serverid, kslabel), int)
    except Exception, E:
        return rhn.fail(E, 'provision system id %d (%s)' % ( serverid, getName(rhn, serverid) ))

# ---------------------------------------------------------------------------- #

def provisionVirtualGuest(rhn, serverid, guestname, kslabel, **kwargs):
    """
    API:
    system.provisionVirtualGuest

    usage:
    provisionVirtualGuest(rhn, serverid, guestname, kslabel, **kwargs)

    description:
    Provision a guest on the host specified. Defaults to:
    memory=256MB, vcpu=1, storage=2048MB
    This schedules the guest for creation and will begin the provisioning process when
    the host checks in or if OSAD is enabled will begin immediately.

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    guestname(str)         - profile name for the new guest
    kslabel(str)            - kickstart profile to use for the new guest

    plus one or more of the following keyword arguments (defaults below)

    *memoryMb(int)          - RAM in Mb for the new guest (default 256)
    *vcpus(int)             - number of vcpus (default 1)
    *storageMb(int)         - Amount of storage to assign (default 2048)
    """
    vmsettings = { 'memoryMb' :
    256, 'vcpus' : 1, 'storageMb' : 2048 }
    try:
        vmsettings.update(kwargs)
        return rhn.session.system.provisionVirtualGuest(rhn.key, serverid, guestname, kslabel, **vmsettings) == 1
    except Exception, E:
        return rhn.fail(E, "provision new VM %s on server %s" %(guestname, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def removeEntitlements(rhn, serverid, entslist):
    """
    API:
    system.removeEntitlements

    usage:
    removeEntitlements(rhn, serverid, entslist)
    
    description:
    downloads the serverid file (/etc/sysconfig/rhn/systemid) for a given serverid.
    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)           - server ID number
    entslist([str])         - list of entitlement labels to remove
    """
    try:
        return rhn.session.system.removeEntitlements(rhn.key, serverid, entslist) == 1
    except Exception, E:
        return rhn.fail(E, "remove entitlements from serverid %d" % (serverid))

# ---------------------------------------------------------------------------- #

def scheduleApplyErrata(rhn, serverids, errataids, runafter=None):
    """
    API:
    system.schedeluApplyErrata

    usage:
    scheduleApplyErrata(rhn, serverids, errataids, runafter = None)

    description:
    schedule the an 'apply errata' action for the given system or list of systems

    returns:
    bool, or throws exception

    parameters: (* = optional)
    rhn                           - rhnsession object
    serverid(int or list of)      - the server (or servers) to apply the action to
    errataids(list of int)        - list or errata IDs to apply
    *runafter(DateTime.iso8601)   - earliest date this can occur
    """
    # handle the multiple parameter combinations
    try:
        if not isinstance(serverids, list):
            serverids = [ serverids ]
        if runafter is None:
            return rhn.session.system.scheduleApplyErrata(rhn.key, serverids, errataids) == 1
        else:
            return rhn.session.system.scheduleApplyErrata(rhn.key, serverids, errataids, runafter) == 1
    except Exception, E:
        return rhn.fail(E, 'schedule application of errata [%s] for server id(s) [%s]' %(','.join(errataids), ''.join(map(str,serverids))))

# ---------------------------------------------------------------------------- #

def scheduleGuestAction(rhn, guestid, guestaction, runafter=None):
    """
    API:
    system.scheduleGuestAction

    usage:
    scheduleGuestAction(rhn, guestid, guestaction, runafter)

    description:
    Schedules a guest action for the specified virtual guest for a given date/time.
    If the date/time is omitted, action is scheduled ASAP

    returns:
    bool, or throws Exception

    parameters:
    rhn                         - an authenticated RHN session
    guestid(int)                - System id of virtual guest
    guestaction(str)            - state of guest, one of ['start', 'suspend', 'resume', 'restart', 'shutdown']
    *runafter(DateTime iso8601) - time to schedule the action (imeediately, if not specified)
    """
    try:
        if runafter is not None:
            return isinstance(rhn.session.system.scheduleGuestAction(rhn.key, guestid, guestaction, runafter), int)
        else:
            return isinstance(rhn.session.system.scheduleGuestAction(rhn.key, guestid, guestaction), int)
    except Exception, E:
        return rhn.fail(E, 'schedule guest %s for guest id %s' %(guestaction, str(guestid)))
            
# ---------------------------------------------------------------------------- #

def scheduleHardwareRefresh(rhn, serverid, runafter):
    """
    API:
    system.scheduleHardwareRefresh

    usage:
    scheduleHardwareRefresh(rhn, serverid, runafter)
    
    description:
    schedule a hardware refresh for the given server id

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    runafter(DateTime)      - earliest date for update (iso 8601 format)
    """
    try:
        return rhn.session.system.scheduleHardwareRefresh(rhn.key, serverid, runafter) == 1
    except Exception, E:
        return rhn.fail(E, "schedule hardware refresh for server id %d (%s)" % (serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def schedulePackageInstall(rhn, serverid, pkgids, runafter):
    """
    API:
    system. schedulePackageInstall

    usage:
    schedulePackageInstall(rhn, serverid, runafter)
    
    description:
    Schedule package installation for a system
    
    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    pkgids([int])           - list of package IDs to install
    runafter(dateTime)      - earliest date for installation.
    """
    try:
        return rhn.session.system.schedulePackageInstall(rhn.key, serverid, pkgids, runafter) == 1
    except Exception, E:
        return rhn.fail(E, "Schedule the installation of packages [%s] on server %d (%s)" % (','.join(map(str, pkgids)),
                                                                         serverid,
                                                                         getName(rhn, serverid)) )

# ---------------------------------------------------------------------------- #

def schedulePackageRefresh(rhn, serverid, runafter):
    """
    API:
    system schedulePackageRefresh

    usage:
    schedulePackageRefresh(rhn, serverid, runafter)
    
    description:
    schedules  a package profile refresh for the given server id

    returns:
    bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    runafter(dateTime)     - earliest date this will occur
    """
    try:
        return isinstance(rhn.session.system.schedulePackageRefresh(rhn.key, serverid, runafter), int)
    except Exception, E:
        return rhn.fail(E, "remove entitlements for server %d (%s)" % (serverid))

# ---------------------------------------------------------------------------- #

def schedulePackageRemove(rhn, serverid, pkgids, runafter):
    """
    API:
    system.schedulePackageRemove

    usage:
    schedulePackageRemove(rhn, serverid, runafter)
    
    description:
    schedule the removal of a (list of) packages from the given system
    
    returns:
    bool, or throws exception

    parameters:
    rhn                       - an authenticated RHN session
    serverid(int)            - server ID number
    pkgids([int])        - list of package ids to remove
    runafter(dateTime)     - earliest date this will occur
    """
    try:
        if not isinstance(pkgids, list):
            pkgids = [ pkgids ]
        return rhn.session.system.schedulePackageRemove(rhn.key, serverid, pkgids, runafter) == 1
    except Exception, E:
        return rhn.fail(E, "Schedule the removal of package ids [%s] from server %d (%s)" % ( ','.join(map(str, pkgids),
                                                                            serverid,
                                                                            getName(rhn, serverid))))

# ---------------------------------------------------------------------------- #

def scheduleReboot(rhn, serverid, runafter):
    """
    API:
    system.scheduleReboot

    usage:
    scheduleReboot(rhn, serverid, runafter)    

    description:
    schedule a reboot for the given serverid

    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    runafter(dateTime)      - earliest date for reboot to occur
    """
    try:
        rhn.session.system.scheduleReboot(rhn.key, int(serverid), runafter)
    except Exception, E:
        return rhn.fail(E, "schedule a reboot for server ID %d" % (serverid))

# ---------------------------------------------------------------------------- #

def scheduleScriptRun(rhn, serverids, username, grpname, timeout, script, runafter=None):
    """
    API:
    system.scheduleScriptRun
    
    usage:
    scheduleScriptRun(rhn, serverids, username, grpname, timeout, script, runafter = None)

    description:
    Schedule a script to run on the given server id (or list of).

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverids([int])        - server id (or list of)
    username(str)           - username that script should use
    grpname(str)            - group name that script should use
    timeout(int)            - timeout in seconds
    script(str)             - script content
    runafter(DateTime)      - earliest date/time for script run (ios8601 format)
    """
    if not isinstance(serverids, list):
        serverids = [ serverids ]
    args = [ serverids, username, grpname, timeout, script ]
    if runafter is not None:
        args.append(runafter)
    try:
        return isinstance(rhn.session.system.scheduleScriptRun(rhn.key, *args), int)

    except Exception, E:
        return rhn.fail(E,'schedule script run on servers [%s]' % (','.join(serverids)))

# ---------------------------------------------------------------------------- #

def scheduleSyncPackagesWithSystem(rhn, serverid, sourceid, pkgids, runafter):
    """
    API:
    system.scheduleSyncPackagesWithSystem

    usage:
    scheduleSyncPackagesWithSystem(rhn, serverid, sourceid, pkgids, runafter)

    description:
    Schedules a package synchronisation from a source server to a target, for the given list
    of package ids
    
    returns:
    bool, or throws exception
   
    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - the server ID to synchronise
    sourceid(int)           - the source server ID
    pkgids([int])           - list of package IDs to synchronise
    runafter(DateTime)      - when to perform the sync
    """
    try:
        return rhn.session.system.scheduleSyncPackagesWithSystem(rhn.key, serverid, sourceid, pkgids, runafter) == 1
    except Exception, E:
        return rhn.fail(E,'schedule package sync from server %d to server %d' % (sourceid, serverid))

# ---------------------------------------------------------------------------- #

def searchByName(rhn, regex):
    """
    API:
    system.searchByName

    usage:
    searchByName(rhn, regex)

    description:
    search for systems whose profile names match the provided regular expression
    http://download.oracle.com/javase/1.4.2/docs/api/java/util/regex/Pattern.html
     - similar to extended regex

    returns:
    list of dict, one per system
        {
        'id'
        'name'
        'last_checkin'
        }

    parameters:
    rhn                     - an authenticated RHN session
    regex(str)       - regular expression to match server names
    """
    try:
        return rhn.session.system.searchByName(rhn.key, regex)
    except Exception, E:
        return rhn.fail(E,'search for servers matching regex "%s"' % (regex))

# ---------------------------------------------------------------------------- #

def setBaseChannel(rhn, serverid, chanlabel):
    """
    API:
    system.setBaseChannel

    usage:
    setBaseChannel(rhn, serverid, chanlabel)

    description:
    changes the specified system's subscribed base channel
    if a blank channel label is provided, the system is unsubscribed from all current channels

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server id to change
    chanlabel(str)          - new base channel label
    """
    try:
        return rhn.session.system.setBaseChannel(rhn.key, serverid, chanlabel) == 1
    except Exception, E:
        return rhn.fail(E,'set base channel for server ID %d to %s' % (serverid, chanlabel))

# ---------------------------------------------------------------------------- #

def setChildChannels(rhn, serverid, chanlist):
    """
    API:
    system.setChildChannels

    usage:
    setChildChannels(rhn, serverid, chanlist)

    description:
    set the list of subscribed base channels for the given system
    the labels provided must be children of the system's subscribed base channel.

    returns:
    bool, or thows exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)          - server ID to change
    chanlist([str])        - list of child channel labels
    """
    try:
        return rhn.session.system.setChildChannels(rhn.key, serverid, chanlist) == 1
    except Exception, E:
        return rhn.fail(E,'subscribe system %d to child channels [%s]' % (serverid, ','.join(chanlist)))

# ---------------------------------------------------------------------------- #

def setCustomValues(rhn, serverid, details):
    """
    API:
    system.setCustomValues

    usage:
    setCustomValues(rhn, serverid, details)
    where details is a a dict... { 'varname' :
    value,...}

    description:
    set custom details for a server

    returns:
    bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)            - server ID number
    details(dict)             - dict of keys and values to set.
    """
    try:
        return rhn.session.system.setCustomValues(rhn.key, serverid, details) == 1
    except Exception, E:
        return rhn.fail(E, "set custom details for server ID %d" % (serverid) )

# ---------------------------------------------------------------------------- #

def setCustomValuesByArg(rhn, serverid, **kwargs):
    """
    API:
    none, special case of 
    system.setCustomValues

    usage:
    setCustomIndValues(rhn, serverid, **kwargs)
    where kwargs is a list of key=value pairs
    e.g. test=wibble,hostname=bob.example.com
    
    Only works for keys without spaces in their labels.
    (but then you shouldn't be putting spaces in there anyway!)
    
    description:
    set custom details for a server using key=value parameters.
    simplifies the setting of one or two variables at a time.

    returns:
    bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)           - server ID number
    **kwargs                 - list of key=value pairs
    """
    try:
        return rhn.session.system.setCustomValues(rhn.key, serverid, kwargs) == 1
    except Exception, E:
        return rhn.fail(E, "set custom details for server %s" % (getName(rhn, serverid)) )

# ---------------------------------------------------------------------------- #

def setDetails(rhn, serverid, serverdetails):
    """
    API:
    system.setDetails

    usage:
    setDetails(rhn, serverid, serverdetails)

    description:
    set the details for an existing RHN system profile

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - the server to change
    serverdetails(dict)     - dictionary of name : value pairs as above

    where serverdetails is of the form:
    {
    "profile_name" (str)        : System's profile name,
    "base_entitlement" (str)    : 'enterprise_entitled' or 'sw_mgr_entitled',
    "auto_errata_update" (bool) : True if system has auto errata updates enabled,
    "description" (str)         : System description,
    "address1" (str)            : System's address line 1,
    "address2" (str)            : System's address line 2,
    "city" (str)                : city
    "state" (str)               : state
    "country" (str)             : country
    "building" (str)            : building
    "room" (str)                : room
    "rack" (str)                : rack
    }
    """
    try:
        return rhn.session.system.setDetails(rhn.key, serverid, serverdetails) == 1
    except Exception, E:
        return rhn.fail(E,'set details for server id %d' % (serverid))

# ---------------------------------------------------------------------------- #

def setDetailsByArg(rhn, serverid, **kwargs):
    """
    API:
    system.setDetails

    usage:
    setDetailsByArg(rhn, name=val, name=val, name=val...)
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

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)          - the server to change
    plus a list of name=value pairs
    kwargs will be created as a dict of the name=value pairs
    """
    try:
        return rhn.session.system.setDetails(rhn.key, serverid, kwargs) == 1
    except Exception, E:
        return rhn.fail(E,'set details for server id %d' % (serverid))

# ---------------------------------------------------------------------------- #

def setGroupMembership(rhn, serverid, grpid, grpmember=1):
    """
    API:
    system.setGroupMembership

    usage:
    setGroupMembership(rhn, serverid, grpid, grpmember = 1)

    description:
    adds or removes the given server id to/from the given groupid
    
    returns:
    bool, or throws exception
    
    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server to manage
    grpid(int)              - server group id
    grpmember(int)          - whether the server should be a member of the
                              group or not. 1=yes, 0=no. default is 1(yes)
    """
    try:
        return rhn.session.system.setGroupMembership(rhn.key, serverid, grpid, grpmember) == 1
    except Exception, E:
        return rhn.fail(E,'set group membership for server id %d' % (serverid))

# ---------------------------------------------------------------------------- #

def setGuestCpus(rhn, guestid, cpucount):
    """
    API:
    system.setGuestCpus

    usage:
    setGuestCpus(rhn, guestid, cpucount)

    description:
    set the number of virtual CPUs for the given virtual guest

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    guestid(int)            - server ID for virtual guest
    cpucount(int)           - number of virtual CPUs to assign
    """
    try:
        return isinstance(rhn.session.system.setGuestCpus(rhn.key, guestid, cpucount), int)
    except Exception, E:
        return rhn.fail(E,'set CPUs to %d for virtual guest id %d' % (cpucount, guestid))

# ---------------------------------------------------------------------------- #

def setGuestMemory(rhn, guestid, memqty):
    """
    API:
    system.getGuestMemory

    usage:
    setGuestMemory(rhn, guestid, memqty)

    description:
    set the amount of memory for the given virtual server

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    guestid(int)            - ID of guest system 
    memqty(int)             - quantity of RAM in Mb
    """
    try:
        return isinstance(rhn.session.system.setGuestMemory(rhn.key, guestid, memqty), int)
    except Exception, E:
        return rhn.fail(E,'set memory for virtual guest %d to %d Mb' % (guestid, memqty))

# ---------------------------------------------------------------------------- #

def setLockStatus(rhn, serverid, islocked):
    """
    API:
    system.setLockStatus

    usage:
    setLockStatus(rhn, serverid, islocked)

    description:
    locks or unlocks a given system ID

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID
    islocked(bool)          - whether system is locked
    """
    try:
        return rhn.session.system.setlockStatus(rhn.key, serverid, islocked) == 1
    except Exception, E:
        return rhn.fail(E,'lock or unlock server %d ' % (serverid))

# ---------------------------------------------------------------------------- #

def setProfileName(rhn, serverid, servername):
    """
    API:
    system.setProfileName

    usage:
    setProfileName(rhn, serverid, servername)

    description:
    renames a system profile

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)          - server ID
    servername(str)        - new profile name
    """
    try:
        return rhn.session.system.setProfileName(rhn.key, serverid, servername) == 1
    except Exception, E:
        return rhn.fail(E,'rename server id %d to %s' % (serverid, servername))

# ---------------------------------------------------------------------------- #

def setVariables(rhn, serverid, netboot, ksvars):
    """
    API:
    system.setVariables

    usage:
    setVariables(rhn, serverid, netboot, ksvars)

    description:
    Sets a list of kickstart variables in the cobbler system record for the specified server. 
    Note:
    This call assumes that a system record exists in cobbler for the given system
    and will raise an XMLRPC fault if that is not the case.
    To create a system record over xmlrpc use system.createSystemRecord

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server id
    netboot(bool)           - is PXE boot enabled for this server?
    ksvars([dict])          - list of dicts, one per name :
    value pair
    """
    try:
        return rhn.session.system.setVariables (rhn.key, serverid, netboot, ksvars) == 1
    except Exception, E:
        return rhn.fail(E,'set variables for server %d' % (serverid))

# ---------------------------------------------------------------------------- #

def setVariablesByArg(rhn, serverid, netboot, **kwargs):
    """
    API:
    none, special case of 
    system.setVariables

    usage:
    setVariablesByArg(rhn, serverid, netboot, key=value, key2=value2, ...)

    description:
    Sets a list of kickstart variables in the cobbler system record for the specified server. 

    Note:
    This call assumes that a system record exists in cobbler for the given system
    and will raise an XMLRPC fault if that is not the case.
    To create a system record over xmlrpc use system.createSystemRecord
    This does not support variable names with spaces in them.


    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server id
    netboot(bool)           - is PXE boot enabled for this server?
    plus key=value pairs for each variable you wish to set.
    """
    try:
        return rhn.session.system.setVariables (rhn.key, serverid, netboot, kwargs) == 1
    except Exception, E:
        return rhn.fail(E,'set variables for server %d' % (serverid))

# ---------------------------------------------------------------------------- #

def tagLatestSnapshot(rhn, serverid, tagname):
    """
    API:
    system.tagLatestSnapshot

    usage:
    tagLatestSnapshot(rhn, serverid, tagname)

    description:
    applies the given tag to the latest snapshot of a system

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server id
    tagname(str)            - the tag to apply
    """
    try:
        return rhn.session.system.tagLatestSnapshot(rhn.key, serverid, tagname) == 1
    except Exception, E:
        return rhn.fail(E, 'apply tag  %s to latest snapshot of system %d (%s)' % (tagname, serverid, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def upgradeEntitlement(rhn, serverid, entlabel):
    """
    API:
    system.upgradeEntitlement

    usage:
    upgradeEntitlement(rhn, serverid, entlabel

    description:
    Adds an entitlement to a given server. 

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    entlabel(str)           - entitlement name to add. one of [ 'enterprise_entitled',
                             'provisioning_entitled', 'monitoring_entitled',
                             'nonlinux_entitled', 'virtualization_host',
                             'virtualization_host_platform']
    """
    try:
        return rhn.session.system.upgradeEntitlement(rhn.key, serverid, entlabel) == 1
    except Exception, E:
        return rhn.fail(E,'add entitlement %s to server id %d' % (entlabel, serverid))
        
# ---------------------------------------------------------------------------- #

def whoRegistered(rhn, serverid):
    """
    API:
    system.whoRegistered

    usage:
    whoRegistered(rhn, serverid)

    description:
    Returns information about the user who registered the system

    returns:
    dict

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server ID number
    """
    try:
        return rhn.session.system.whoRegistered(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E,'discover user who registered server id %d' % (serverid))


# ------------------------- system.config namespace -------------------------- #

def addConfigChannels(rhn, serverids, chanlabels, prepend):        
    """
    API:
    system.config.addChannels

    usage:
    addConfigChannels(rhn, serverids, chanlabels, prepend)

    description:
    Given a list of servers and configuration channels, appends the configuration channels
    to either the top or the bottom (whichever you specify) of a system's subscribed configuration channels list.
    The ordering of the configuration channels provided in the add list is maintained while adding.
    If one of the configuration channels in the 'add' list has been previously subscribed
    by a server, the subscribed channel will be re-ranked to the appropriate place. 

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverids(list/int)     - list of server IDs
    chanlabels(list/str)    - list of channel labels
    prepend(bool)           - whether to add the channels in order to the top or bottom
                              of the subscribed channel list.
    """
    if not isinstance(serverids, list):
        serverids = [ serverids ]
    if not isinstance(chanlabels, list):
        chanlabels = [ chanlabels ]
    try:
        return rhn.session.system.config.addChannels(rhn.key, serverids, chanlabels, prepend) == 1
    except Exception, E:
        return rhn.fail(E, 'add config channel(s) [%s] to server(s) [%s]'%(','.join(chanlabels),
            ','.join([getName(rhn, x) for x in serverids ])))

# ---------------------------------------------------------------------------- #

def createOrUpdatePath(rhn, serverid, path, local, pathobj, isdir=False):
    """
    API:
    system.config.createOrUpdatePath

    usage:
    createOrUpdatePath(rhn, serverid, path, directory = False, local, pathobj)

    description:
    create or update a configuration file either in a system's local override channel or sandbox

    returns:
    bool, or throws exception (depends on RHN debug setting)

    parameters 
    rhn                         - an authenticated RHN session.
    path(str)                   - the absolute path on the target system, including filename.
    isdir(bool)                 - this is a directory, not a file
    local(int)                  - commit this file to the local override channel (1) or sandbox(0)
    pathobj(dict)               - a dict representing the path to update or create,
                                  with the following keys (* = optional):
    owner(str)                      - the owner of the file once deployed.
    group(str)                      - the group associated with the file once deployed.
    permissions(str)                - octal permissions for the deployed file (e.g. 0644)
    * contents(str)                 - the contents of the file (ignored for directories)
                                      while this will work without content, it's not the best idea.
    * contents_enc64(bool)          - contents are base64 encoded (for binary files)
    * selinux_ctx(str)              - SELinux context
    * macro_start_delimiter(str)    - string used to indicate beginning of macro expressions. Leave empty for default
    * macro_end_delimiter(str)      - string used to indicate the end of macro expressions. Leave empty for default.
    * revision(int)                 - revison of updated file (auto-incremented)
    """
    try:
        return isinstance(rhn.session.system.config.createOrUpdatePath(rhn.key, serverid, path, isdir, pathobj, local), dict)
    except Exception, E:
        if local == 1:
            return rhn.fail(E, 'update path %s in system %s local override channel' %(path, getName(rhn, serverid)))
        else:
            return rhn.fail(E, 'update path %s in system %s sandbox' %(path, getName(rhn, serverid)))
            
# ---------------------------------------------------------------------------- #

def createOrUpdatePathByArg(rhn, serverid, path, isdir=False, local=1, **kwargs):
    """
    API:
    none, special adaptation of system.config.createOrUpdatePath to use kwargs

    usage:
    createOrUpdatePath(rhn, serverid, path, directory = False, local = 0, **kwargs)
    where kwargs is a list of key=value pairs (see parameters below)

    description:
    create or update a configuration file either in a system's local override channel or sandbox

    returns:
    bool, or throws exception (depends on RHN debug setting)

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
        return isinstance(rhn.session.system.config.createOrUpdatePath(rhn.key, serverid, path, isdir, kwargs, local), dict)
    except Exception, E:
        if local == 1:
            return rhn.fail(E, 'update path %s in system %s local override channel' %(path, getName(rhn, serverid)))
        else:
            return rhn.fail(E, 'update path %s in system %s sandbox' %(path, getName(rhn, serverid)))
            
# ---------------------------------------------------------------------------- #

def createOrUpdateSymlink(rhn, serverid, path, local, pathobj):
    """
    API:
    system.config.createOrUpdateSymlink

    usage:
    createOrUpdateSymlink(rhn, channel_label, path, **kwargs)
    where **kwargs is a list of key=value pairs (see parameters, below)

    Creates or Updates a new Symlink (file or directory) in a config channel

    returns:
    dict showing path information

    parameters (*=optional)
    rhn                    - an authenticated RHN session.
    serverid(int)          - server ID
    path(str)              - path on filesystem
    local(int)             - commit this file to the local override channel (1) or sandbox(0)
                             (default is local override channel)
    pathobj(dict)          - dict representing the symlink and its target
                             keys as follows (* = optional):
    target_path(str)        - the absolute path to the symlink's target
    *selinux_ctx(str)       - SELinux context for the symlink
    *revision(int)          - revison of updated file 
    """
    try:
        return isinstance(rhn.session.system.config.createOrUpdateSymlink(rhn.key, serverid, path, pathobj, local), dict)
    except Exception, E:
        if local == 1:
            return rhn.fail(E, 'update symlink %s in system %s local override channel' %(path, getName(rhn, serverid)))
        else:
            return rhn.fail(E, 'update symlink %s in system %s sandbox' %(path, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def createOrUpdateSymlinkByArg(rhn, serverid, path, local=1, **kwargs):
    """
    API:
    none, special case of system.config.createOrUpdateSymlink adapted to use kwargs

    usage:
    createOrUpdateSymlink(rhn, channel_label, path, **kwargs)
    where **kwargs is a list of key=value pairs (see parameters, below)

    description:
    Creates or Updates a new Symlink (file or directory) in a config channel

    returns:
    dict showing path information

    parameters (*=optional)
    rhn                     - an authenticated RHN session.
    serverid(int)          - server ID
    path(str)               - path on filesystem
    *local(int)             - commit this file to the local override channel (1) or sandbox(0)
                              (default is local override channel)

    plus one or more key-value pairs as follows (* = optional)
    target_path(str)        - the absolute path to the symlink's target
    *selinux_ctx(str)       - SELinux context for the symlink
    *revision(int)          - revison of updated file 
    """
    try:
        if rhn.debug:
            print rhn.key, serverid, path, kwargs, local
        return isinstance(rhn.session.system.config.createOrUpdateSymlink(rhn.key, serverid, path, kwargs, local), dict)
    except Exception, E:
        if local == 1:
            return rhn.fail(E, 'update symlink %s in system %s local override channel' %(path, getName(rhn, serverid)))
        else:
            return rhn.fail(E, 'update symlink %s in system %s sandbox' %(path, getName(rhn, serverid)))

# ---------------------------------------------------------------------------- #

def deleteConfigFiles(rhn, serverid, pathlist, local):
    """
    API:
    system.config.deleteFiles

    usage:
    deleteFiles(rhn, serverid, fileList, localChannel=False)

    description:
    Deletes files from a local or sandbox channel of a server

    returns:
    bool, or throws exception.

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - server identifier
    pathlist(list/str)      - path (or list of paths) to delete
    local(bool)             - delete from local channel(true) or sandbox(false).
    """
    if not isinstance(pathlist, list):
        pathlist = [ pathlist ]
    try:
        return rhn.session.system.config.deleteFiles(rhn.key, serverid, pathlist, local) == 1
    except Exception, E:
        return rhn.fail(E, 'delete files from server')

# ---------------------------------------------------------------------------- #

def deployAllConfigChannels(rhn, serverids, runafter=None):
    """
    API:
    system.config.DeployAll

    usage:
    deployAllConfigChannels(rhn, serverids, runafter)

    description:
    Schedules a deploy action for all config channels on a given list of system IDs

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    systemIDList(list/int)  - list of system IDs to work on
    runafter(str)           - earliest runafter for deploy action. in iso8601 format.
                              e.g. 20110505T11:48:56 (%Y%m%dT%H:%M:%S)
                              if omitted, defaults to current time/runafter
    """
    # encode a DateTime instance (defaults to local time)
    applyafter = rhn.encodeDate(runafter)
    if not isinstance(serverids, list):
        serverids = [ serverids ]
    try:
        return rhn.session.system.config.deployAll(rhn.key, serverids, applyafter) == 1
    except Exception, E:
        return rhn.fail(E, 'schedule the requested deploy action' )

# ---------------------------------------------------------------------------- #

def listConfigChannels(rhn, serverid):
    """
    API:
    system.config.listChannels

    usage:
    listConfigChannels(rhn, serverid)

    Lists the config channels for a server order of rank

    returns:
    list of dicts, one per channel

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)            - server identifier
    """
    try:
        return rhn.session.system.config.listChannels(rhn.key, serverid)
    except Exception, E:
        return rhn.fail(E, 'list config channels for server %d' % serverid)

# ---------------------------------------------------------------------------- #

def listConfigFiles(rhn, serverid, local=1):
    """
    API:
    system.config.listFiles

    usage:
    listFiles(rhn, serverid, listLocal=1)

    descriptions
    Lists the configuration files for a server, either from config channels
    (including local overrides) or from the system's sandbox.

    returns:
    list of dicts, one per channel.

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - RHN Server ID
    local(int)              - list files in system's local override channel (1)
                              or sandbox (0)
    """
    try:
        return rhn.session.system.config.listFiles(rhn.key, serverid, local)
    except Exception, E:
        return rhn.fail(E, 'list files on server id %d' % serverid)

# ---------------------------------------------------------------------------- #

def lookupConfigFileInfo(rhn, serverid, pathlist, local=1):
    """
    API:
    system.config.lookUpFileInfo

    usage:
    lookupFileInfo(rhn, serverid, fileList, searchLocal=1)

    description:
    Lists the package filenames affected by a given erratum

    returns:
    list of dicts, one per path.

    parameters:
    rhn                     - an authenticated RHN session
    serverid(int)           - integer ID of the server to query
    pathlist(list/str)      - a list of paths to query
    local(int)              - search config channels + local override (1)
                              search sandbox (0)
    """
    if not isinstance(pathlist, list):
        pathlist = [ pathlist ]
    try:
        return rhn.session.system.config.lookupFileInfo(rhn.key, serverid, pathlist, local)
    except Exception, E:
        return rhn.fail(E, 'get file revision info for files [%s]' % ','.join(pathlist))
     
# ---------------------------------------------------------------------------- #

def removeConfigChannels(rhn, serverids, cfglabels):
    """
    API:
    system.config.removeChannels

    usage:
    removeConfigChannels(rhn, serverids, channelList)

    Removes the given config channels from a list of servers

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverids(list/int)     - list of server IDs
    cfglabels(list/str)     - list of configuration channel labels
    """
    if not isinstance(serverids, list):
        serverids = [ serverids ]
    if not isinstance(cfglabels, list):
        cfglabels = [ cfglabels ]
    try:
        return rhn.session.system.config.removeChannels(rhn.key, serverids, cfglabels) == 1
    except Exception, E:
        return rhn.fail(E, 'remove config channels [%s] from servers [%s]' %( ','.join(cfglabels),
            ','.join([ getName(rhn, sid) for sid in serverids ])))

# ---------------------------------------------------------------------------- #

def setConfigChannels(rhn, serverids, cfglabels):
    """
    API:
    system.config.setChannels

    usage:
    setConfigChannels(rhn, serverids, cfglabels))

    description:
    replaces the existing config channels for each of the servers in serverids
    cfglabels should be in descending ranked order

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    serverids(list/int)     - list of server IDs
    cfglabels(list/str)     - list of config channel labels
    """
    if not isinstance(serverids, list):
        serverids = [ serverids ]
    if not isinstance(cfglabels, list):
        cfglabels = [ cfglabels ]
    try:
        return rhn.session.system.config.setChannels(rhn.key, serverids, cfglabels) == 1
    except Exception, E:
        return rhn.fail(E, 'set config channels [%s] for servers [%s]' %( ','.join(cfglabels),
            ','.join([ getName(rhn, sid) for sid in serverids ])))

# ----------------------- system.custominfo namespace ------------------------ #

def createCustomInfoKey(rhn, label, description):
    """
    API:
    system.custominfo.createKey

    usage:
    createCustomInfoKey(rhn, label, description)

    description:
    create a new key for storing custom information

    returns:
    bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    label(str)               - label for the new key
    description(str)         - description of the key
    """
    try:
        return rhn.session.system.custominfo.createKey(rhn.key, label, description) == 1
    except Exception, E:
        return rhn.fail(E, 'create new custom info key %s' % label)

# ---------------------------------------------------------------------------- #

def deleteCustomInfoKey(rhn, label):
    """
    API:
    system.custominfo.deleteKey

    usage:
    deleteCustomInfoKey(rhn, label)

    description:
    deletes a custom system information key.
    This will remove the key and any information stored in it for all systems

    returns:
    bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    label(str)               - label for the new key
    """
    try:
        return rhn.session.system.custominfo.deleteKey(rhn.key, label) == 1
    except Exception, E:
        return rhn.fail(E, 'delete custom info key %s' % label)
    
def listAllCustomInfoKeys(rhn):
    """
    API:
    system.custominfo.listAllKeys

    usage:
    listAllCustomInfoKeys(rhn)

    description:
    List the custom information keys defined for the user's organization

    returns:
    list of dict (one per key)

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.system.custominfo.listAllKeys(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list all custom system information keys')

# ---------------------------------------------------------------------------- #

def updateCustomInfoKey(rhn, label, description):
    """
    API:
    system.custominfo.updateKey

    usage:
    updateCustomInfoKey(rhn, label, description)

    description:
    Update description of a custom key

    parameters:
    rhn                      - an authenticated RHN session
    label(str)               - Custom info key label
    description(str)         - Custom Info Key Description
    """
    try:
        return rhn.session.system.custominfo.updateKey(rhn.key, label, description) == 1
    except Exception, E:
        return rhn.fail(E, 'update description of custom info key "%s"' % label)

# ---------------------------------------------------------------------------- #
    
# ------------------ system.provisioning.snapshot namespace ------------------ #

def addTagToSnapshot(rhn, snapid, tagname):
    """
    API:
    system.provisioning.snapshot.addTagToSnapshot

    usage:
    addTagToSnapshot(rhn, snapid, tagname)

    description:
    Adds a tag to the chosen snapshot

    returns:
    bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    snapid(int)              - snapshot id
    tagname(str)             - the tag name to add to the snapshot
    """
    try:
        return rhn.session.system.provisioning.snapshot.addTagToSnapshot(rhn.key, snapid, tagname) == 1
    except Exception, E:
        return rhn.fail(E,'add tag %s to snapshot ID %d' %(tagname, snapid))

# ---------------------------------------------------------------------------- #

def deleteSnapshot(rhn, snapid):
    """
    API:
    system.provisioning.snapshot

    usage:
    deleteSnapshot(rhn, snapid)

    description:
    deletes the snapshot with the given ID

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session
    snapid(int)             - label for the new key
    """
    try:
        return rhn.session.system.provisioning.snapshot.deleteSnapshot(rhn.key. snapid) == 1
    except Exception, E:
        return rhn.fail(E, 'delete snapshot ID %d' % snapid)

# ---------------------------------------------------------------------------- #

def deleteSystemSnapshots(rhn, serverid, **kwargs):
    """
    API:
    none, special case of system.provisioning.snapshot.deleteSnapshots

    usage:
    deleteSnapshots(rhn, **kwargs)
    possible keyword arguments are:
    startDate, endDate

    description:
    deletes all snapshots for a given server, optionally between 2 dates.
    If no dates are provided, ALL snapshots for thse given server are deleted.
    if startDate is provided without endDate, evrything after startDate is deleted.
    
    returns:
    bool, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)           - RHN server id
    optional extra arguments:
    *startDate(str)          - iso8601 format date string
    *endDate(str)            - iso8601 format date string

    iso8601 format is %Y%m%dT%H:%M:%S e.g. 20110506T11:12:13
    """
    # let's encode our date strings appropriately for XMLRPC
    if kwargs.has_key('startDate'):
        kwargs['startDate'] = rhn.encodeDate(kwargs['startDate'])
    if kwargs.has_key('endDate'):
        kwargs['endDate'] = rhn.encodeDate(kwargs['endDate'])

    try:
        return rhn.session.system.provisioning.snapshot.deleteSnapshots(rhn.key, serverid, kwargs) == 1
    except Exception, E:
        return rhn.fail(E, 'delete snapshots for system %s' % getName(rhn, serverid))

# ---------------------------------------------------------------------------- #

def deleteSnapshots(rhn, **kwargs):
    """
    API:
    system.provisioning.deleteSnapshots

    usage:
    deleteSnapshots(rhn, **kwargs)

    description:
    delete all system snaphots, for all servers, optionally between 2 dates.
    

    returns:
    bool, or throws exception

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

# ---------------------------------------------------------------------------- #
    
def listSnapshotConfigFiles(rhn, snapid):    
    """
    API:
    system.provisioning.snapshot.listSnapshotConfigFiles

    usage:
    listSnapshotConfigFiles(rhn, snapid)

    description:
    list the config files associated with a snapshot

    returns:
    list of dict, one per configuration file

    parameters:
    rhn                      - an authenticated RHN session
    snapid(int)         - the snapshot ID
    """
    try:
        return rhn.session.system.provisioning.snapshot.listSnapshotConfigFiles(rhn.key, snapid)
    except Exception, E:
        return rhn.fail(E, 'list config files for snapshot ID %d' % snapid)

# ---------------------------------------------------------------------------- #

def listSnapshotPackages(rhn, snapid):
    """
    API:
    system.provisioning.snapshot.listSnapshotPackages

    usage:
    listSnapshotPackags(rhn, snapid)

    description:
    list the packages associated with a snapshot

    returns:
    list of dict, one per package

    parameters:
    rhn                      - an authenticated RHN session
    snapid(int)         - snapshot ID
    """
    try:
        return rhn.session.system.provisioning.snapshot.listSnapshotPackages(rhn.key, snapid)
    except Exception, E:
        return rhn.fail(E, 'list packages associated with snapshot ID %d' % snapid)

# ---------------------------------------------------------------------------- #

def listSnapshots(rhn, serverid, **kwargs):
    """
    API:
    system.provisioning.snapshot.listSnapshots

    usage:
    listSnapshots(rhn, serverid, **kwargs)
    where optional keyword args are startDate and/or endDate

    description:
    list the snapshots associated with the given server ID. Start and end dates are optional.

    returns:
    list of dict, one per snapshot

    parameters:
    rhn                      - an authenticated RHN session
    serverid(int)           - server ID
    optional extra arguments:
    *startDate(str)          - iso8601 format date string
    *endDate(str)            - iso8601 format date string

    iso8601 format is %Y%m%dT%H:%M:%S e.g. 20110506T11:12:13
    """
    # let's encode our date strings appropriately for XMLRPC
    dates = {}
    if kwargs.has_key('startDate'):
        dates['startDate'] = rhn.encodeDate(kwargs['startDate'])
    if kwargs.has_key('endDate'):
        dates['endDate'] = rhn.encodeDate(kwargs['endDate'])
    try:
        return rhn.session.system.provisioning.snapshot.listSnapshots(rhn.key, serverid, dates) == 1
    except Exception, E:
        return rhn.fail(E,  'list system snapshots for server %s' % getName(rhn, serverid))

# ------------------------- system.search namespace -------------------------- #

def searchDeviceDescription(rhn, query):
    """
    API:
    system.search.deviceDescription

    usage:
    searchDeviceDescriptions(rhn, query)

    description:
    list the systems matching the device description
    The search string is not case sensitive

    returns:
    list of dict, one per server.

    parameters:
    rhn                     - an authenticated RHN session
    query(str)              - string to search for
    """
    try:
        return rhn.session.system.search.deviceDescription(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching device description "%s"' % query)

# ---------------------------------------------------------------------------- #

def searchDeviceDriver(rhn, query):
    """
    API:
    system.search.deviceDriver

    usage:
    searchDeviceDriver(rhn, query)

    description:
    list the systems matching the device driver given
    The search string is not case sensitive

    returns:
    list of dict, one per server.

    parameters:
    rhn                     - an authenticated RHN session
    query(str)              - string to search for
    """
    try:
        return rhn.session.system.search.deviceDriver(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching device driver "%s"' % query)

# ---------------------------------------------------------------------------- #

def searchDeviceId(rhn, query):
    """
    API:
    system.search.deviceId

    usage:
    searchDeviceId(rhn, query)

    description:
    list the systems matching the device Id given
    The search string is not case sensitive

    returns:
    list of dict, one per server.

    parameters:
    rhn                     - an authenticated RHN session
    query(str)              - string to search for
    """
    try:
        return rhn.session.system.search.deviceId(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching device Id "%s"' % query)

# ---------------------------------------------------------------------------- #

def searchDeviceVendorId(rhn, query):
    """
    API:
    system.search.deviceVendorId

    usage:
    searchDeviceDescriptions(rhn, query)

    description:
    list the systems matching the device description
    The search string is not case sensitive

    returns:
    list of dict, one per server.

    parameters:
    rhn                     - an authenticated RHN session
    query(str)              - string to search for
    """
    try:
        return rhn.session.system.search.deviceVendorId(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching device VendorId "%s"' % query)

# ---------------------------------------------------------------------------- #

def searchHostname(rhn, query):
    """
    API:
    system.search.hostname

    usage:
    searchDeviceDescriptions(rhn, query)

    description:
    list the systems matching the hostname provided
    The search string is not case sensitive

    returns:
    list of dict, one per server.

    parameters:
    rhn                     - an authenticated RHN session
    query(str)              - string to search for
    """
    try:
        return rhn.session.system.search.hostname(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching device driver "%s"' % query)

# ---------------------------------------------------------------------------- #
        
def searchIp(rhn, query):
    """
    API:
    system.search.ip

    usage:
    searchip(rhn, query)

    description:
    list the systems matching the IP given
    The search string is not case sensitive

    returns:
    list of dict, one per server.

    parameters:
    rhn                     - an authenticated RHN session
    query(str)              - string to search for
    """
    try:
        return rhn.session.system.search.ip(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search for systems matching IP Address "%s"' % query)

# ---------------------------------------------------------------------------- #

def searchNameAndDescription(rhn, query):
    """
    API:
    system.search.NameAndDescription

    usage:
    searchNameAndDescription(rhn, query)

    description:
    list the systems matching the NameAndDescription given
    The search string is not case sensitive

    returns:
    list of dict, one per server.

    parameters:
    rhn                     - an authenticated RHN session
    query(str)              - string to search for
    """
    try:
        return rhn.session.system.search.nameAndDescription(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search for systems whose name or description match "%s"' % query)
        
# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
