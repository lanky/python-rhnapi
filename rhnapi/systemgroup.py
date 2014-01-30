#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the 'systemgroup' namespace
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
systemgroup.py
An abstraction of the systemgroup namespace from the RHN Satellite  / Spacewalk XMLRPC API
created for and tested on RHN Satellite 5.4.1

All of the methods in here most probably require an authenticated rhnSession object from the
parent rhnapi class.
There are a few convenience functions in here for special cases of functions in the original API
such as
addAdmins/removeAdmins -> special case of addOrRemoveAdmins
"""

__author__ = "Stuart Sears"

# ---------------------------------------------------------------------------- #

def addOrRemoveAdmins(rhn, sysgroup, adminlist, action):
    """
    API:
    systemgroup.addOrRemoveAdmins

    usage:
    addOrRemoveAdmins(rhn, sysgroup, adminlist, action)

    description:
    Adds a list of Administrators to a configuration channel

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup(str)           - a system group name
    adminlist(list/str)     - a list of RHN logins
    action(int)             - 1 to add, 0 to remove
                              (or use the special case functions below)
    """
    if action == 1:
        task = "add"
    elif action == 0:
        task = "remove"
    else:
        task = "ERROR: no action defined"
    try:
        return rhn.session.systemgroup.addOrRemoveAdmins(rhn.key, sysgroup, adminlist, action) == 1
    except Exception, E:
        return rhn.fail(E, '%s one or more of %s as admin(s) of group %s' %( task, ','.join(adminlist), sysgroup))

# ---------------------------------------------------------------------------- #

def addAdmins(rhn, sysgroup, adminlist):
    """
    API:
    none, special case of addOrRemoveAdmins

    usage:
    addAdmins(rhn, sysgroup, adminlist)

    description:
    Adds a list of Administrators to a configuration channel

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup(str)           - a system group name
    adminlist(list/str)     - a list of RHN logins
    """
    return addOrRemoveAdmins(rhn, sysgroup, adminlist, 1)
    
# ---------------------------------------------------------------------------- #

def addAdmin(rhn, sysgroup, adminlogin):
    """
    API:
    none, special case of addOrRemoveAdmins

    usage:
    addAdmin(rhn, sysgroup, adminlogin)

    description:
    Adds a single administrator to a configuration channel

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup(str)           - a system group name
    adminlogin(str)         - a single RHN login
    """
    return addOrRemoveAdmins(rhn, sysgroup, [adminlogin], 1)

# ---------------------------------------------------------------------------- #

def removeAdmins(rhn, sysgroup, adminlist):
    """
    API:
    none, special case of addOrRemoveAdmins

    usage:
    removeAdmins(rhn, sysgroup, adminlist)

    Removes a list of administrators from a system group

    returns: 1 on success

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup(str)           - a system group name
    adminlist(list/str)     - a list of RHN logins
    """
    return addOrRemoveAdmins(rhn, sysgroup, adminlist, 0)

# ---------------------------------------------------------------------------- #

def removeAdmin(rhn, sysgroup, adminlogin):
    """
    API:
    none, special case of addOrRemoveAdmins

    usage:
    removeAdmin(rhn, sysgroup, adminlogin)

    Removes an individual administrator from a system group.

    returns: 1 for success

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup(str)           - a system group name
    adminlogin(str)         - a single RHN login
    """
    return addOrRemoveAdmins(rhn, sysgroup, [adminlogin], 0)

# ---------------------------------------------------------------------------- #

def addOrRemoveSystems(rhn, sysgroup, serverids, add=True):
    """
    API:
    systemgroup.addOrRemoveSystems

    usage:
    addOrRemoveSystems(rhn, sysgroup, serverids, action)

    description:
    Adds a list of systems to a system group

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup(str)           - a system group name
    serverids(list/int)     - list of system IDs
    """
    if add:
        task = "add"
    else:
        task = "remove"
    try:
        return rhn.session.systemgroup.addOrRemoveSystems(rhn.key, sysgroup, serverids, add) == 1
    except Exception, E:
        return rhn.fail(E, '%s one or more of %s as members of group %s' %(task, ','.join(serverids), sysgroup))

# ---------------------------------------------------------------------------- #

def addSystems(rhn, sysgroup, serverids):
    """
    API:
    none, special case of addOrRemoveSystems

    usage:
    addSystems(rhn, sysgroup, serverids)

    description:
    Adds a list of systems to a system group

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup(str)           - a system group name
    serverids(list/int)     - list of system IDs
    """
    return addOrRemoveSystems(rhn, sysgroup, serverids, 1)

# ---------------------------------------------------------------------------- #

def addSystem(rhn, sysgroup, serverid):
    """
    API:
    none, special case of addOrRemoveSystems

    usage:
    addSystem(rhn, sysgroup, serverids)

    description:
    Adds a list of systems to a system group

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup(str)           - a system group name
    serverid(int)           - an individual system ID
    """
    return addOrRemoveSystems(rhn, sysgroup, [serverid], 1)

# ---------------------------------------------------------------------------- #

def removeSystems(rhn, sysgroup, serverids):
    """
    API:
    none, special case of addOrRemoveSystems

    usage:
    removeSystems(rhn, sysgroup, serverids)

    description:
    Removes a list of systems from a system group

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup(str)           - a system group name
    serverids(list/int)     - a list of system IDs
    """
    return addOrRemoveSystems(rhn, sysgroup, serverids, 0)

# ---------------------------------------------------------------------------- #

def removeSystem(rhn, sysgroup, serverid):
    """
    API:
    none, special case of addOrRemoveSystems

    usage:
    removeSystem(rhn, sysgroup, serverid)

    Removes an individual system from a system group.

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup(str)           - a system group name
    serverid(int)           - and individual system ID
    """
    return addOrRemoveSystems(rhn, sysgroup, [serverid], 0)

# ---------------------------------------------------------------------------- #

def create(rhn, sysgroup, sysdesc):
    """
    API:
    systemgroup.create

    usage:
    create(rhn, sysgroup, sysdesc)

    description:
    Creates a new system group

    returns:
    dict of group information
        {
          'id' (int)           : group ID
          'name' (str)         : group Name
          'sysdesciption' (str)  : group sysdesciption
          'org_id' (int)       : RHN org the group is in
          'system_count' (int) : number of systems in the group
        }

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.systemgroup.create(rhn.key, sysgroup, sysdesc)
    except Exception, E:
        return rhn.fail(E, 'create system group %s' %( sysgroup ))

def delete(rhn, sysgroup):
    """
    API:
    systemgroup.delete

    usage:
    delete(rhn, sysgroup)

    Deletes a system group

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    """
    try:
        return rhn.session.systemgroup.delete(rhn.key, sysgroup) == 1
    except Exception, E:
        return rhn.fail(E, 'delete system group %s' %( sysgroup))

# ---------------------------------------------------------------------------- #

def getDetails(rhn, groupspec):
    """
    API:
    systemgroup.getDetails

    usage:
    getDetails(rhn, groupspec)

    description:
    Retrieves group details by ID or Name

    returns:
    dict of group information
        {
          'id' (int)           : group ID
          'name' (str)         : group Name
          'sysdesciption' (str)  : group sysdesciption
          'org_id' (int)       : RHN org the group is in
          'system_count' (int) : number of systems in the group
        }


    parameters:
    rhn                     - an authenticated RHN session
    groupspec(int or str)   - group ID or name
    """
    try:
        return rhn.session.systemgroup.getDetails(rhn.key, groupspec)
    except Exception, E:
        ID = str(groupspec)
        return rhn.fail(E, 'retrieve information about group %s' % ID )
    
# ---------------------------------------------------------------------------- #

def listActiveSystemsInGroup(rhn, sysgroup):
    """
    API:
    systemgroup.listActiveSystemsInGroup

    usage:
    listActiveSystemsInGroup(rhn, sysgroup)

    description:
    lists the Active systems in a chosen system group

    returns:
    list of int (server IDs), one per system.

    parameters:
    rhn                      - an authenticated RHN session
    sysgroup              - the name of a system group
    """
    try:
        return rhn.session.systemgroup.listActiveSystemsInGroup(rhn.key, sysgroup)
    except Exception, E:
        return rhn.fail(E, 'list active systems in group %s' % sysgroup)
        
# ---------------------------------------------------------------------------- #

def listAdministrators(rhn, sysgroup):
    """
    API:
    systemgroup.listAdministrators

    usage: 
    listAdministrators(rhn, sysgroup)

    description:
    lists the package filenames affected by a given erratum

    returns:
    list of dict, one per admin user:
        {
          'id' (int)       : user ID
          'login' (str)    : user login
          'login_uc' (str) : user login in uppercase
          'enabled' (bool) : if the user is enabled
        }

    parameters:
    rhn                      - an authenticated RHN session
    sysgroup(str)            - system group name
    """
    try:
        return rhn.session.systemgroup.listAdministrators(rhn.key, sysgroup)
    except Exception, E:
        return rhn.fail(E, 'list administrators of group %s' %( sysgroup))

# ---------------------------------------------------------------------------- #

def listAllGroups(rhn):
    """
    API:
    systemgroup.listAllGroups

    usage:
    listAllGroups(rhn)

    description:
    Retrieve a list of system groups that are accessible by the logged in user.

    returns:
    list of dict (group info)
        {
          'id' (int)           : group ID
          'name' (str)         : group Name
          'sysdesciption' (str)  : group sysdesciption
          'org_id' (int)       : RHN org the group is in
          'system_count' (int) : number of systems in the group
        }

    params:
    rhn                 - authenticated rhnSession object
    """
    try:
        return rhn.session.systemgroup.listAllGroups(rhn.key)
    except Exception, E:
        rhn.fail(E, 'Failed to list system groups')

# ---------------------------------------------------------------------------- #

def listGroupsWithNoAssociatedAdmins(rhn):
    """
    API:
    systemgroup.listGroupsWithNoAssociatedAdmins

    usage:
    listGroupsWithNoAssociatedAdmins(rhn, sysgroup)

    description:
    list groups with no admins assigned.

    returns:
    list of dict (group info)
        {
          'id' (int)           : group ID
          'name' (str)         : group Name
          'sysdesciption' (str)  : group sysdesciption
          'org_id' (int)       : RHN org the group is in
          'system_count' (int) : number of systems in the group
        }

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup                - the name of a system group
    """
    try:
        return rhn.session.systemgroup.listGroupsWithNoAssociatedAdmins(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list systems groups with no admin users')

# ---------------------------------------------------------------------------- #

def listGroupsWithoutAdmins(rhn):
    """
    backwards compatibility. Alias for listGroupsWithNoAssociatedAdmins
    """
    return listGroupsWithNoAssociatedAdmins(rhn)

# ---------------------------------------------------------------------------- #
    
def listInactiveSystemsInGroup(rhn, sysgroup, days = 1):
    """
    API:
    systemgroup.listInactiveSystemsInGroup

    usage:
    listInactiveSystemsInGroup(rhn, sysgroup)

    description:
    lists the Inactive systems in a chosen system group

    returns:
    list of int (server IDs), one per system.

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup                - the name of a system group
    days(int)               - number of days before a system is considered inactive.
                              default: 1
    """
    try:
        return rhn.session.systemgroup.listInactiveSystemsInGroup(rhn.key, sysgroup, days)
    except Exception, E:
        return rhn.fail(E, 'list inactive systems in group %s' % sysgroup)

# ---------------------------------------------------------------------------- #

def listSystems(rhn, sysgroup):
    """
    API:
    systemgroup.listSystems

    usage:
    listSystems(rhn, sysgroup)

    description:
    lists the systems in a chosen system group

    returns:
    list of dicts, one per system.
        {
          'id' (int) : - System id
          'profile_name' (str) :
          'base_entitlement' (str) : - System's base entitlement label. (enterprise_entitled or sw_mgr_entitled)
          'addon_entitlements' (list/str)   : System's addon entitlements labels, including monitoring_entitled, provisioning_entitled, virtualization_host, virtualization_host_platform
          'auto_update' (boolean)           : True if system has auto errata updates enabled.
          'release' (str)                   : The Operating System release (i.e. 4AS, 5Server
          'address1' (str)                  :
          'address2' (str)                  :
          'city' (str)                      :        
          'state' (str)                     :
          'country' (str)                   :
          'building' (str)                  :
          'room' (str)                      :
          'rack' (str)                      :
          'description' (str)               :
          'hostname' (str)                  :
          'last_boot' (dateTime.iso8601)    : 
          'osa_status' (str)                : 'unknown', 'offline', or 'online'.
          'lock_status' (boolean)           : is the system locked?
        }

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.systemgroup.listSystems(rhn.key, sysgroup)
    except Exception, E:
        return rhn.fail(E, 'list systems in group %s' % sysgroup)

# ---------------------------------------------------------------------------- #

def scheduleApplyErrataToActive(rhn, sysgroup, errlist, runafter = None ):
    """
    API:
    systemgroup.scheduleApplyErrataToActive

    usage:
    listAdministrators(rhn, sysgroup)

    description:
    lists the Administrators of a chosen system group

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup                - the name of a system group
    errlist                 - a list of errata IDs to apply
    runafter                - an iso 8601 format date
                               (use datetime.datetime.isoformat())
    """
    try:
        if runafter is not None:
            return rhn.session.systemgroup.scheduleApplyErrataToActive(rhn.key, sysgroup, errlist, runafter) == 1
        else:
            return rhn.session.systemgroup.scheduleApplyErrataToActive(rhn.key, sysgroup, errlist, runafter) == 1
    except Exception, E:
        return rhn.fail(E, 'schedule errata [%s] on active systems in group %s' % (','.join(errlist), sysgroup))

# ---------------------------------------------------------------------------- #
    
def update(rhn, sysgroup, grpdesc):
    """
    API:
    systemgroup.update

    usage:
    update(rhn, sysgroup, grpdesc)

    description:
    updates information about a systemgroup (desciption, really)

    returns:
    dict of group information
        {
          'id' (int)           : group ID
          'name' (str)         : group Name
          'grpdesciption' (str)  : group grpdesciption
          'org_id' (int)       : RHN org the group is in
          'system_count' (int) : number of systems in the group
        }

    parameters:
    rhn                     - an authenticated RHN session
    sysgroup(str)           - a system group name
    grpdesc(str)            - group description
    """
    try:
        return rhn.session.systemgroup.update(rhn.key, sysgroup, grpdesc)
    except Exception, E:
        return rhn.fail(E, 'update system group %s' % sysgroup )

# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
