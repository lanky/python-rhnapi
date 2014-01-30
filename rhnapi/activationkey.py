#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the activationkey namespace
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


__doc__ = """
rhnapi.activationkey is an abstraction of the API calls available in RHN Satellite  >= 5.1.0
for managing activation keys.
Import this as rhnapi.activationkey

Most of the methods here require an authenticated RHN session as their first argument, 
which you can create with rhnapi.rhnSession().
"""
__author__ = "Stuart Sears"

# additional required imports
import sys

# ---------------------------------------------------------------------------- #

def addChildChannels(rhn, keyid, chanlabels):
    """
    API:
    activationkey.addChildChannels

    usage:
    addChildChannels(rhn, keyid, chanlabels)

    description:
    Add the specified child channels to an activation key.

    returns:
    Bool, or throws Exception
    
    parameters:
    rhn                     - an authenticated rhn session
    keyid (str)             - the key identifier (long hex or human-readable name)
    chanlabels (list/str)   - a list of child channel labels to add to the key
    """
    try:
        return rhn.session.activationkey.addChildChannels(rhn.key, keyid, chanlabels) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of child channels %r to %s' % (chanlabels, keyid))

# ---------------------------------------------------------------------------- #

def addConfigChannels(rhn, keyids, cfgchans, addToTop = False):
    """
    API:
    activationkey.addConfigChannels

    usage:
    addConfigChannels(rhn, keyids, cfgchans, addToTop=False)

    description:
    Add a list of configuration channels, in ranked order, to the given key
    (or list of keys)
    
    returns:
    Bool, or throws Exception
    
    parameters:
    rhn                        - an authenticated rhn session
    keyids (list/str)          - the key identifier (long hex or human-readable name)
    cfgchans(list/str)      - a list of configuration channel labels
    addToTop(bool)             - add this list to the top [false]
    """
    try:
        return rhn.session.activationkey.addConfigChannels(rhn.key, keyids, cfgchans, addToTop) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of %r to keys %r' % (cfgchans, keyids))

# ---------------------------------------------------------------------------- #

def addEntitlements(rhn, keyid, entslabels):
    """
    API:
    activationkey.addEntitlements

    usage:
    addEntitlements(rhn, keyid, entslabels)

    description:
    Add one or more of the following entitlements to a key:
    [monitoring_entitled, provisioning_entitled, virtualization_host, virtualization_host_platform]

    returns:
    Bool, or throws Exception
    
    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    entslabels (list)      - a list of add-on entitlements.

    entitlements are one or more of [ 'monitoring_entitled', 'provisioning_entitled',
                                      'vitualization_host', 'virtualization_host_platform' ]
    """
    try:
        return rhn.session.activationkey.addEntitlements(rhn.key, keyid, entslabels) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of  %r to key %s' % (entslabels, keyid))

# ---------------------------------------------------------------------------- #

def addGroups(rhn, keyid, groupids):
    """
    API:
    activationkey.addServerGroups

    usage:
    addGroups(rhn, keyid, group_ids)

    description:
    Adds the given list of server group IDs to the chosen activation key

    returns:
    Bool, or throws Exception

    shorter name for addServerGroups
    params:
    rhn                     - authenticated rhnSession object
    keyid(str)              - the activation key
    groupids(list/int)     - list of group IDs (integers)
    """
    return addServerGroups(rhn, keyid, groupids)

# ---------------------------------------------------------------------------- #

def addServerGroups(rhn, keyid, groupids):
    """
    API:
    activationkey.addServerGroups

    usage:
    addServerGroups(rhn, keyid, groupids)

    description:
    Add a list of system groups to an activation key
    The system groups are specified by id, not name.
    
    returns:
    Bool, or throws Exception

    parameters:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    groupids (list)        - a list of additional system group IDs.
    """
    try:
       return  rhn.session.activationkey.addServerGroups(rhn.key, keyid, groupids) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of groups %r to key %s' % (groupids, keyid))

# ---------------------------------------------------------------------------- #

def addGroupsByName(rhn, keyid, groupnames):
    """
    API:
    none, custom method

    usage:
    addGroupsByName(rhn, keyid, groupnames)

    description:
    Add a list of system groups by name. This involves calling out to rhnapi.systemgroup
    just passes this info to addServerGroups
    This skips groups that do not exist on the satellite.

    parameters:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    groupnames (list/str)  - a list of system group names to add.
    """
    # handle being given a single groupname, too
    # import our local systemgroup module
    import systemgroup
    allgroups = systemgroup.listAllGroups(rhn)
    ids = [ x['id'] for x in allgroups if x['name'] in groupnames ]
    return addServerGroups(rhn, keyid, ids)

# ---------------------------------------------------------------------------- #

def addPackages(rhn, keyid, pkglist):
    """
    API:
    activationkey.addPackages

    usage:
    addPackages(rhn, keyid, pkglist)

    description:
    Add a list of pkglist (with arch) to a key.

    returns:
    Bool, or throws Exception

    params
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    pkglist(list of dict)  - a list of package dicts { 'name', 'arch'(optional) }
    """
    try:
        return rhn.session.activationkey.addPackages(rhn.key, keyid, pkglist) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of %r to %s' % ([ x['name'] for x in pkglist ], keyid))

# ---------------------------------------------------------------------------- #

def addPackageNames(rhn, keyid, packagenames):
    """
    API:
    activationkey.addPackageNames

    usage:
    addPackageNames(rhn, keyid, packagenames)

    description:
    Add a list of package names to a key.
    Deprecated (but still functional) in favour of addPackages. Use that instead.

    returns:
    Bool, or throws Exception
    
    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    packagenames (list)    - a list of packagenames
    """
    try:
        return rhn.session.activationkey.addPackageNames(rhn.key, keyid, packagenames) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of %r to %s' % (packagenames, keyid))

# ---------------------------------------------------------------------------- #

def checkConfigDeployment(rhn, keyid):
    """
    API:
    activationkey.checkConfigDeployment

    usage:
    checkConfigDeployment(rhn, keyid)

    description:
    reports whether configuration deployment is enabled for a given key

    returns:
    Bool (config deployment status), or throws Exception

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    groups (list)          - a list of additional system group IDs.
    """
    try:
        return rhn.session.activationkey.checkConfigDeployment(rhn.key, keyid) == 1
    except Exception, E:
        return rhn.fail(E,'check config deployment status for key %s' % keyid)


# ---------------------------------------------------------------------------- #

def create(rhn, description, keyid='',  basechannel='', entitlements=[], usagelimit=None, universalDefault=False ):
    """
    API:
    activationkey.create

    usage:
    create(rhn, description, keyid='',  basechannel='', entitlements=[], usagelimit=None, universalDefault=False )

    description:
    Create a new activation key with the given properties.
    The keyid parameter passed in will be prefixed with the organization ID.
    Eg. If the caller passes in the key "foo" and belongs to an organization with the ID 100,
    the actual activation key will be "100-foo".

    returns:
    str (the new activation key)

    params: (* = optional)
    rhn                      -  an authenticated RHN session and its associated properties.
    description (str)        -  key description
    keyid (str)            -  Activation key name/id. leave blank for auto-generation
    *basechannel (str)       -  base channel label (blank for default)
    *entitlements (list)     -  a list of add-on entitlements. Default is none.
    *usagelimit (int)        -  usage limit. default=None (which means unlimited in this context)
    *universaldefault (bool) -  this key is the universal default key for all registrations (False)
    """
    try:
        if usagelimit is not None:
            # if we have specified a usage limit...
            return rhn.session.activationkey.create(rhn.key,keyid,description,basechannel,entitlements,usagelimit,universalDefault)
        else:
            # otherwise the key has unlimited usage
            return rhn.session.activationkey.create(rhn.key,keyid,description,basechannel,entitlements,universalDefault)
    except Exception, E:
        return rhn.fail(E,'create activation key %s' % keyid)
    
# ---------------------------------------------------------------------------- #

def delete(rhn, keyid):
    """
    API:
    activationkey.delete

    usage:
    delete(rhn, keyid)

    description:
    Delete an existing activation key.

    returns:
    Bool, or throws Exception

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.delete(rhn.key, keyid) == 1
    except Exception, E:
        return rhn.fail(E,'delete activation key %s' % keyid )

# ---------------------------------------------------------------------------- #

def disableConfigDeployment(rhn, keyid):
    """
    API:
    activationkey.disableConfigDeployment

    usage:
    disableConfigDeployment(rhn, keyid) 

    description:
    Lists the kickstart profiles on the satellite

    returns:
    Bool, or throws Exception

    parameters:
    rhn                    - an authenticated RHN session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.disableConfigDeployment(rhn.key, keyid) == 1
    except Exception, E:
        return rhn.fail(E, 'disable config deployment for key %s' % keyid)

# ---------------------------------------------------------------------------- #

def enableConfigDeployment(rhn, keyid):
    """
    API:
    activationkey.enableConfigDeployment

    usage:
    enableConfigDeployment(rhn, keyid) 

    description:
    enables config file deployment for the chosen key

    returns:
    Bool, or throws Exception

    parameters:
    rhn                      - an authenticated RHN session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.enableConfigDeployment(rhn.key, keyid) == 1
    except Exception, E:
        return rhn.fail(E, 'enable config deployment for key %s' % keyid)

# ---------------------------------------------------------------------------- #

def getDetails(rhn, keyid):
    """
    API:
    activationkey.getDetails

    usage:
    getDetails(rhn, keyid)

    description:
    show information about an activation key.
    
    returns:
    dict (activation key information)
        {
        'key' (str) :
        'description' (str) :
        'usage_limit' (int) :
        'base_channel_label' (str) :
        'child_channel_labels' (list of str) :
        'entitlements' (list of str) :
        'server_group_ids' (list of str) :
        'package_names' (list of str) :
            str packageName - (deprecated by packages)
        'packages' (list of dict) : { 'name' (str) : - packageName 'arch' (str) : - archLabel - optional }
        'universal_default' (bool) :
        'disabled' (bool) :
        }

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.getDetails(rhn.key, keyid)
    except Exception, E:
        return rhn.fail(E,'retrieve details for activation key %s' % keyid)

# ---------------------------------------------------------------------------- #

def listActivationKeys(rhn):
    """
    API:
    activationkey.listActivationKeys

    usage:
    listActivationKeys(rhn)

    description:
    List the Activation Keys available to the current logged-in user

    returns:
    list of dict, one per key

    params:
    rhn                    - an authenticated rhn session
    """
    try:
        return rhn.session.activationkey.listActivationKeys(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list activation keys for logged-in user %s' % rhn.login )

# ---------------------------------------------------------------------------- #

def listActivationKeyNames(rhn):
    """
    API:
    none, special case of listActivationKeys for simpler use cases

    usage:
    listActivationKeyNames(rhn)

    description:
    List the Activation Keys available to the current logged-in user


    returns:
    list of tuple: ( description(str), key(str) )

    params:
    rhn                    - an authenticated rhn session
    """
    try:
        return [ (x['description'], x['key']) for x in rhn.session.activationkey.listActivationKeys(rhn.key) ]
    except Exception, E:
        return rhn.fail(E,'list activation keys for logged-in user %s' % rhn.login )

# ---------------------------------------------------------------------------- #

def listActivatedSystems(rhn, keyid):
    """
    API:
    actiationkey.listActivatedSystems

    usage:
    listActivatedSystems(rhn, keyid)

    description:
    lists systems registered using a given activation key

    returns:
    list/dict { id, hostname, last checkin }

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.listActivatedSystems(rhn.key, keyid)
    except Exception, E:
        return rhn.fail(E, 'list activated systems for key %s' % keyid)

# ---------------------------------------------------------------------------- #

def list(rhn):
    """
    Calls the more-longwinded ListActivationKeys
    """
    return listActivationKeys(rhn)

# ---------------------------------------------------------------------------- #

def listConfigChannels(rhn, keyid):
    """
    API:
    activationkey.listConfigChannels
    
    usage:
    listConfigChannels(rhn, keyid)
    
    description:
    List the Configuration Channels associated with the given activation key

    returns:
    list of dict, one per config channel

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.listConfigChannels(rhn.key, keyid)
    except Exception, E:
        return rhn.fail(E, 'list config channels for key %s' % keyid)

        
# ---------------------------------------------------------------------------- #

def removeChildChannels(rhn, keyid, chanlabels):
    """
    API:
    activationkey.removeChildChannels

    usage:
    removeChildChannels(rhn, keyid, chanlabels)

    description:
    Removes the specified child chanlabels from an activation key.

    returns:
    bool (True if successful).

    params:
    rhn                   - an authenticated rhn session
    keyid (str)           - the key identifier (long hex or human-readable name)
    chanlabels (list(int))  - a list of child channel IDs to remove from the key.
    """
    try:
        return rhn.session.activationkey.removeChildChannels(rhn.key, keyid, chanlabels) == 1
    except Exception, E:
        return rhn.fail(E,'remove one or more of child channels %r from key %s' % (chanlabels, keyid))

# ---------------------------------------------------------------------------- #

def removeConfigChannels(rhn, keyids, cfgchans):
    """
    API:
    activationkey: removeConfigChannels

    usage:
    removeConfigChannels(rhn, keyid, cfgchans)
    
    description:
    Add the specified child cfgchans to an activation key.

    returns:
    True if successful, exception otherwise

    params:
    rhn                           - an authenticated rhn session
    keyids ( str OR list of str)) - the key identifier (long hex or human-readable name)
    cfgchans (list(str))          - a list of config channel labels to remove from the key.
    """
    if isinstance(keyids, str):
        keyids = [ keyids ]
    try:
        return rhn.session.activationkey.removeConfigChannels(rhn.key, keyids, cfgchans) == 1
    except Exception, E:
        return rhn.fail(E,'remove one or more of config channels %r from key %s' % (cfgchans, keyids))
    
# ---------------------------------------------------------------------------- #

def removeEntitlements(rhn, keyid, entlabels):
    """
    API:
    activationkey.removeEntitlements

    usage:
    removeEntitlements(rhn, keyid, entlabels)
   
    description:
    Remove one or more of the following entlabels from a key:
    [monitoring_entitled, provisioning_entitled, virtualization_host, virtualization_host_platform]

    returns:
    Bool, or throws Exception

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    entlabels (list)       - a list of entitlement labels to remove
    """
    try:
        return rhn.session.activationkey.removeEntitlements(rhn.key, keyid, entlabels) == 1
    except Exception, E:
        return rhn.fail(E,'remove one or more of  %r from key %s' % (entlabels, keyid))

# ---------------------------------------------------------------------------- #

def removePackageNames(rhn, keyid, packagenames):
    """
    API:
    activationkey.removePackageNames

    usage:
    removePackageNames(rhn, keyid, packagenames)

    description:
    Remove the given list of packages from an activation key
    deprecated in favour of removePackages

    params
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    packagenames (list)    - a list of packagenames
    """
    try:
        rhn.logInfo("removePackageNames is deprecated, please use removePackages instead")
        return rhn.session.activationkey.removePackageNames(rhn.key, keyid, packagenames) == 1
    except Exception, E:
        return rhn.fail(E,'remove one or more of %r from key %s' % (packagenames, keyid))

# ---------------------------------------------------------------------------- #

def removePackages(rhn, keyid, packageids):
    """
    API:
    activationkey.removePackages

    usage:
    removePackages(rhn, keyid, packagelist)

    description:
    Remove the given list of packages from an activation key

    params
    rhn                         - an authenticated rhn session
    keyid (str)                 - the key identifier (long hex or human-readable name)
    packagelist (list/dict)     - list of package dicts, in this format:
                                  { 'name' : packagename, 'arch' : arch_label }
                                  'arch' is optional
    """
    try:
        return rhn.session.activationkey.removePackages(rhn.key, keyid, packageids) == 1
    except Exception, E:
        return rhn.fail(E,'remove one or more of %r from key %s' % (packageids, keyid))

# ---------------------------------------------------------------------------- #

def removeGroups(rhn, keyid, groupids):
    """
    shortcut to removeServerGroups
    """
    return removeServerGroups(rhn, keyid, groupids)

# ---------------------------------------------------------------------------- #

def removeServerGroups(rhn, keyid, groupids):
    """
    Add a list of system groups to an activation key
    The system groups are specified by id, not name.
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    groupids (list)        - a list of system group IDs.
    """
    try:
        return rhn.session.activationkey.removeServerGroups(rhn.key, keyid, groupids) == 1
    except Exception, E:
        return rhn.fail(E,'remove one or more of %r from key %s' % (groupids, keyid))

# ---------------------------------------------------------------------------- #

def removeGroupsByName(rhn, keyid, groupnames):
    """
    API:
    none, custom method

    usage:
    removeGroupsByName(rhn, keyid, groupnames)

    description:
    Add a list of system groups by name. This involves calling out to rhnapi.groups

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    groupnames (list)          - a list of group names to remove.
    """
    import systemgroup
    groupinfo = systemgroup.listAllGroups(rhn)
    ids = [ x['id'] for x in groupinfo if x['name'] in groupnames ]
    return removeServerGroups(rhn, keyid, ids)

# ---------------------------------------------------------------------------- #

def setConfigChannels(rhn, keyids, cfgchans):
    """
    API:
    activationkey.setConfigChannels

    usage:
    setConfigChannels(rhn, keyids, cfgchans)

    description:
    Replaces the current set of config channels with the given list for all of the given activation keys.
    the channel list should be in descending order of rank.


    returns:
    Bool, or throws Exception

    params:
    rhn                    - an authenticated rhn session
    keyids (list/str)      - the key identifier (long hex or human-readable name)
    cfgchans (list/str)    - a list of config channel labels
    """
    try:
        return rhn.session.activationkey.setConfigChannels(rhn.key, keyids, cfgchans) == 1
    except Exception, E:
        return rhn.fail(E, 'set config channels %r for keys %r' %(cfgchans, keyids))

# ---------------------------------------------------------------------------- #

def setDetails(rhn, keyid, keyobj):
    """
    API:
    activationkey.setDetails

    usage:
    setDetails(rhn, keyid, keyobj)

    description:
    replaces the settings for an existing activation key

    returns:
    Bool, or throws Exception

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    keyobj (dict)          - information to store in the key. Could be retrieved using
                             getDetails
    """
    try:
        return rhn.session.activationkey.setDetails(rhn.key, keyid, keyobj ) == 1
    except Exception, E:
        
        return rhn.fail(E,'retrieve details for activation key %s' % keyid)

# ---------------------------------------------------------------------------- #

# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
