#!/usr/bin/env python
# -*- coding: utf-8 -*-
# An abstraction of the RHN API for activation keys.
# Author: Stuart Sears <sjs@redhat.com>
# Caution. This is an unsupported API package.
# it may cause untold and hideous damage to your
# RHN satellite and anything else you hold dear
# for which I will not be held responsible.
# if you use it you acknowledge this risk :)

__doc__ = """
rhnapi.activationkey is an abstraction of the API calls available in RHN Satellite  >= 5.1.0
for managing activation keys.
Import this as rhnapi.activationkey

Most of the methods here require an authenticated RHN session as their first argument, 
which you can create with rhnapi.rhnSession().
"""
import sys

def addChildChannels(rhn, keyid, chan_labels):
    """
    API: activationkey.addChildChannels

    usage: addChildChannels(rhn, keyid, chan_labels)

    returns: bool, or exception

    description:
    Add the specified child channels to an activation key.
    
    parameters:
    rhn                     - an authenticated rhn session
    keyid (str)             - the key identifier (long hex or human-readable name)
    chan_labels (list/str)  - a list of child channel labels to add to the key
    """
    try:
        return rhn.session.activationkey.addChildChannels(rhn.key, keyid, chan_labels) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of child channels %r to %s' % (chan_labels, keyid))

def addConfigChannels(rhn, keyids, config_labels, addToTop = False):
    """
    API: activationkey.addConfigChannels

    usage: addConfigChannels(rhn, keyids, configchannels, addToTop=False)

    description:
    Add a list of configuration channels, in ranked order, to the given key
    (or list of keys)
    
    returns: True, or throws its toys about
    
    parameters:
    rhn                        - an authenticated rhn session
    keyids (list/str)          - the key identifier (long hex or human-readable name)
    config_labels(list/str)    - a list of configuration channel labels
    addToTop(bool)             - add this list to the top [false]
    """
    try:
        return rhn.session.activationkey.addConfigChannels(rhn.key, keyids, config_labels, addToTop) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of %r to keys %r' % (config_labels, keyids))

def addEntitlements(rhn, keyid, entitlements):
    """
    API: activationkey.addEntitlements

    usage: addEntitlements(rhn, keyid, entitlements)

    Add one or more of the following entitlements to a key:
    [monitoring_entitled, provisioning_entitled, virtualization_host, virtualization_host_platform]
    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    entitlements (list)    - a list of add-on entitlements.

    entitlements are one or more of [ 'monitoring_entitled', 'provisioning_entitled',
                                      'vitualization_host', 'virtualization_host_platform' ]
    """
    try:
        return rhn.session.activationkey.addEntitlements(rhn.key, keyid, entitlements) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of  %r to key %s' % (entitlements, keyid))

def addGroups(rhn, keyid, group_ids):
    """
    API: activationkey.addServerGroups

    usage: addGroups(rhn, keyid, groups)
    shorter name for addServerGroups
    """
    return addServerGroups(rhn, keyid, group_ids)

def addServerGroups(rhn, keyid, group_ids):
    """
    API: activationkey.addServerGroups

    usage:  addServerGroups(rhn, keyid, groups)

    description:
    Add a list of system groups to an activation key
    The system groups are specified by id, not name.
    
    returns: True, or throws exception

    parameters:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    group_ids (list)       - a list of additional system group IDs.
    """
    try:
       return  rhn.session.activationkey.addServerGroups(rhn.key, keyid, group_ids) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of groups %r to key %s' % (group_ids, keyid))

def addGroupsByName(rhn, keyid, groupnames):
    """
    API: none, custom method

    usage: addGroupsByName(rhn, keyid, groupnames)

    description:
    Add a list of system groups by name. This involves calling out to rhnapi.systemgroup
    just passes this info to addServerGroups

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

def addPackages(rhn, keyid, packages):
    """
    usage: addPackages(rhn, keyid, packages)

    Add a list of packages (with arch) to a key.

    returns: int(1) or Exception

    params
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    package(list of dict)  - a list of package dicts { 'name', 'arch'(optional) }
    """
    try:
        return rhn.session.activationkey.addPackages(rhn.key, keyid, packages) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of %r to %s' % ([ x['name'] for x in packages ], keyid))

def addPackageNames(rhn, keyid, packagenames):
    """
    Add a list of package names to a key.
    params
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    packagenames (list)    - a list of packagenames
    """
    try:
        return rhn.session.activationkey.addPackageNames(rhn.key, keyid, channels) == 1
    except Exception, E:
        return rhn.fail(E,'add one or more of %r to %s' % (packagenames, keyid))

def checkConfigDeployment(rhn, keyid):
    """
    usage: checkConfigDeployment(rhn, keyid)

    returns: True (1) or exception

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    groups (list)          - a list of additional system group IDs.
    """
    try:
        return rhn.session.activationkey.checkConfigDeployment(rhn.key, keyid)
    except Exception, E:
        return rhn.fail(E,'check config deployment status for key %s' % keyid)


def create(rhn, description, keyid="",  basechannel='', entitlements=[], usagelimit=None, universalDefault=False ):
    """
    Create a new activation key with the given properties.
    The keyid parameter passed in will be prefixed with the organization ID.
    Eg. If the caller passes in the key "foo" and belongs to an organization with the ID 100,
    the actual activation key will be "100-foo".

    returns: str (the new activation key)

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
        if usagelimit != None:
            # if we have specified a usage limit...
            return rhn.session.activationkey.create(rhn.key,keyid,description,basechannel,entitlements,usagelimit,universalDefault)
        else:
            # otherwise the key has unlimited usage
            return rhn.session.activationkey.create(rhn.key,keyid,description,basechannel,entitlements,universalDefault)
    except Exception, E:
        return rhn.fail(E,'create activation key %s' % keyid)
    
def delete(rhn, keyid):
    """
    Delete an existing activation key.
    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.delete(rhn.key, keyid) == 1
    except Exception, E:
        return rhn.fail(E,'delete activation key %s' % keyid )

def getDetails(rhn, keyid):
    """
    show information about an activation key.
    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.getDetails(rhn.key, keyid)
    except Exception, E:
        return rhn.fail(E,'retrieve details for activation key %s' % keyid)

def list(rhn):
    """
    Calls the more-longwinded ListActivationKeys
    """
    return listActivationKeys(rhn)

def listActivatedSystems(rhn, keyid):
    """
    usage: listActivatedSystems(rhn, keyid)

    returns: list/dict { id, hostname, last checkin }

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.listActivatedSystems(rhn.key, keyid)
    except Exception, E:
        return rhn.fail(E, 'list activated systems for key %s' % keyid)

def listActivationKeys(rhn):
    """
    List the Activation Keys available to the current logged-in user

    usage: listActivationKeys(rhn)

    returns: list(dict)

    params:
    rhn                    - an authenticated rhn session
    """
    try:
        return rhn.session.activationkey.listActivationKeys(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list activation keys for logged-in user %s' % rhn.login )

def listActivationKeyNames(rhn):
    """
    List the Activation Keys available to the current logged-in user

    usage: listActivationKeyNames(rhn)

    returns: list(str)

    params:
    rhn                    - an authenticated rhn session
    """
    try:
        return [ (x['description'], x['key']) for x in rhn.session.activationkey.listActivationKeys(rhn.key) ]
    except Exception, E:
        return rhn.fail(E,'list activation keys for logged-in user %s' % rhn.login )

def listConfigChannels(rhn, keyid):
    """
    List the Activation Keys available to the current logged-in user

    usage: listActivationKeys(rhn)

    returns: list(dict)

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.listConfigChannels(rhn.key, keyid)
    except Exception, E:
        return rhn.fail(E, 'list config channels for key %s' % keyid)

        
def removeChildChannels(rhn, keyid, channels):
    """
    Add the specified child channels to an activation key.

    usage: removeChildChannels(rhn, keyid, channels)

    returns: True if successful, exception otherwise

    params:
    rhn                   - an authenticated rhn session
    keyid (str)           - the key identifier (long hex or human-readable name)
    channels (list(int))  - a list of child channel IDs to remove from the key.
    """
    try:
        return rhn.session.activationkey.removeChildChannels(rhn.key, keyid, channels) == 1
    except Exception, E:
        return rhn.fail(E,'remove one or more of child channels %r from key %s' % (channels, keyid))

def removeConfigChannels(rhn, keyids, channels):
    """
    Add the specified child channels to an activation key.

    usage: removeConfigChannels(rhn, keyid, channels)

    returns: True if successful, exception otherwise

    params:
    rhn                   - an authenticated rhn session
    keyid (list(str))     - the key identifier (long hex or human-readable name)
    channels (list(str))  - a list of config channel labels to remove from the key.
    """
    try:
        return rhn.session.activationkey.removeChildChannels(rhn.key, keyid, channels) == 1
    except Exception, E:
        return rhn.fail(E,'remove one or more of config channels %r from key %s' % (channels, keyid))
    
def removeEntitlements(rhn, keyid, entitlements):
    """
    Remove one or more of the following entitlements from a key:
    [monitoring_entitled, provisioning_entitled, virtualization_host, virtualization_host_platform]

    usage: removeEntitlements(rhn, keyid, entitlements)

    returns: True or throws exception

    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    entitlements (list)    - a list of entitlements to remove
    """
    try:
        return rhn.session.activationkey.removeEntitlements(rhn.key, keyid, channels) == 1
    except Exception, E:
        return rhn.fail(E,'remove one or more of  %r from key %s' % (entitlements, keyid))

def removePackages(rhn, keyid, packagenames):
    """
    Add a list of package names to a key.
    params
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    packagenames (list)    - a list of packagenames
    """
    try:
        return rhn.session.activationkey.addPackageNames(rhn.key, keyid, channels) == 1
    except Exception, E:
        return rhn.fail(E,'remove one or more of %r from key %s' % (packagenames, keyid))

def removeGroups(rhn, keyid, groups):
    """
    shortcut to removeServerGroups
    """
    removeServerGroups(rhn, keyid, groups)

def removeServerGroups(rhn, keyid, groups):
    """
    Add a list of system groups to an activation key
    The system groups are specified by id, not name.
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    groups (list)          - a list of removeitional system group IDs.
    """
    try:
        return rhn.session.activationkey.removeServerGroups(rhn.key, keyid, channels) == 1
    except Exception, E:
        return rhn.fail(E,'remove one or more of %r from key %s' % (packagenames, keyid))

def removeGroupsByName(rhn, keyid, groupnames):
    """
    Add a list of system groups by name. This involves calling out to rhnapi.groups
    params
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    groups (list)          - a list of group names to remove.
    """
    import systemgroup
    groupinfo = systemgroup.listAllGroups(rhn)
    ids = [ x['id'] for x in allgroups if x['name'] in groupnames ]
    return removeServerGroups(rhn, keyid, ids)

def setConfigChannels(rhn, keyids, channels):
    """
    Replaces the current set of config channels with the given list for all of the given activation keys.
    channels list is in ranking order

    usage: setConfigChannels(rhn, keyids, channels)

    returns: True or exception

    params:
    rhn                    - an authenticated rhn session
    keyids (list/str)      - the key identifier (long hex or human-readable name)
    channels (list/str)    - a list of group names to remove.
    """
    try:
        return rhn.session.activationkey.setConfigChannels(rhn.key, keyids, channels) == 1
    except Exception, E:
        return rhn.fail(E, 'set config channels %r for keys %r' %(channels, keyids))

def setDetails(rhn, keyid, keydata):
    """
    show information about an activation key.
    params:
    rhn                    - an authenticated rhn session
    keyid (str)            - the key identifier (long hex or human-readable name)
    keydata (dict)         - information to store in the key. Could be retrieved using
                             getDetails
    """
    try:
        return rhn.session.activationkey.setDetails(rhn.key, keyid, keydata ) == 1
    except Exception, E:
        return rhn.fail(E,'retrieve details for activation key %s' % keyid)

def enableConfigDeployment(rhn, keyid):
    """
    usage: enableConfigDeployment(rhn, keyid) 

    Lists the kickstart profiles on the satellite

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.enableConfigDeployment(rhn.key, keyid) == 1
    except Exception, E:
        return rhn.fail(E, 'enable config deployment for key %s' % keyid)

def disableConfigDeployment(rhn, keyid):
    """
    usage: disableConfigDeployment(rhn, keyid) 

    Lists the kickstart profiles on the satellite

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    keyid (str)            - the key identifier (long hex or human-readable name)
    """
    try:
        return rhn.session.activationkey.disableConfigDeployment(rhn.key, keyid) == 1
    except Exception, E:
        return rhn.fail(E, 'disable config deployment for key %s' % keyid)
