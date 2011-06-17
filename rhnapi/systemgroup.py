#!/usr/bin/env python
# -*- coding: utf-8 -*-
# an abstraction of the 'systemgroup' namespace
# from the RHN API for satellite 5.1.0

# import this as rhnapi.systemgroup.
# from rhnapi import systemgroup doesn't really work
# as yet, because these things need the rhnSession class
# defined either in rhnapi.base or rhnapi itself to 
# actually do anything.

def addAdmins(rhn, systemGroup, adminList):
    """
    usage: addAdmins(rhn, systemGroup, adminList)

    Adds a list of Administrators to a configuration channel

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup(str)         - a system group name
    adminList(list/str)      - a list of RHN logins
    """
    try:
        return rhn.session.systemgroup.addOrRemoveAdmins(rhn.key, systemGroup, adminList, 1) == 1
    except Exception, E:
        return rhn.fail(E, 'add one of %s to group %s' %( ','.join(adminList), systemGroup))

def addAdmin(rhn, systemGroup, adminLogin):
    """
    usage: addAdmin(rhn, systemGroup, adminLogin)

    Adds a single administrator to a configuration channel

    returns: 1 for success(!)

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup(str)         - a system group name
    adminLogin(str)          - a single RHN login
    """
    return addAdmins(rhn, systemGroup, [adminLogin])

def removeAdmins(rhn, systemGroup, adminList):
    """
    usage: removeAdmins(rhn, systemGroup, adminList)

    Removes a list of administrators from a system group

    returns: 1 on success

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup(str)         - a system group name
    adminList(list/str)      - a list of RHN logins
    """
    try:
        return rhn.session.systemgroup.addOrRemoveAdmins(rhn.key, systemGroup, adminList, 0) == 1
    except Exception, E:
        return rhn.fail(E, 'add one of %s to group %s' %( ','.join(adminList), systemGroup))

def removeAdmin(rhn, systemGroup, adminLogin):
    """
    usage: removeAdmin(rhn, systemGroup, adminLogin)

    Removes an individual administrator from a system group.

    returns: 1 for success

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup(str)         - a system group name
    adminLogin(str)          - a single RHN login
    """
    return removeAdmins(rhn, systemGroup, [adminLogin])

def addSystems(rhn, systemGroup, systemList):
    """
    usage: addSystems(rhn, systemGroup, systemList)

    Adds a list of systems to a system group

    returns: 1 on success

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup(str)         - a system group name
    systemList(list/int)     - list of system IDs
    """
    try:
        return rhn.session.systemgroup.addOrRemoveSystems(rhn.key, systemGroup, adminList, 1) == 1
    except Exception, E:
        return rhn.fail(E, 'add one of %s to group %s' %( ','.join(systemList), systemGroup))

def addSystem(rhn, systemGroup, systemID):
    """
    usage: addSystems(rhn, systemGroup, systemList)

    Adds a list of systems to a system group

    returns: 1 on success

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup(str)         - a system group name
    systemID(int)            - an individual system ID
    """
    return addSystems(rhn, systemGroup, [systemID])

def removeSystems(rhn, systemGroup, systemList):
    """
    usage: removeSystems(rhn, systemGroup, systemList)

    Removes a list of systems from a system group

    returns: 1 on success

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup(str)         - a system group name
    systemList(list/int)     - a list of system IDs
    """
    try:
        return rhn.session.systemgroup.addOrRemoveSystems(rhn.key, systemGroup, systemList) == 1
    except Exception, E:
        return rhn.fail(E, 'remove one or more of %s from group %s' %( ','.join(systemList), systemGroup))

def removeSystem(rhn, systemGroup, systemID):
    """
    usage: removeSystem(rhn, systemGroup, systemID)

    Removes an individual system from a system group.

    returns: 1 on success

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup(str)         - a system group name
    systemID(int)            - and individual system ID
    """
    removeSystems(rhn, systemGroup, [systemID]) == 1

def create(rhn, systemGroup, descr):
    """
    usage: create(rhn, systemGroup, descr)

    Creates a new system group

    returns: dict, containing group info

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.systemgroup.create(rhn.key, systemGroup, descr)
    except Exception, E:
        return rhn.fail(E, 'create system group %s' %( systemGroup ))

def delete(rhn, systemGroup):
    """
    usage: delete(rhn, systemGroup)

    Deletes a system group

    returns: 1 on success

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.systemgroup.delete(rhn.key, systemGroup)
    except Exception, E:
        return rhn.fail(E, 'add one of %s to group %s' %( ','.join(adminList), systemGroup))

def getDetails(rhn, groupNameOrID):
    """
    usage: getDetails(rhn, groupNameOrID)

    Retrieves group details by ID or Name

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.systemgroup.getDetails(rhn.key, groupNameOrID)
    except Exception, E:
        ID = str(groupNameOrID)
        return rhn.fail(E, 'retrieve information about group %s' % ID )
    
def listAdmins(rhn, systemGroup):
    """
    usage: 

    Lists the package filenames affected by a given erratum

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.systemgroup.listAdmins(rhn.key, systemGroup)
    except Exception, E:
        return rhn.fail(E, 'list administrators of group %s' %( systemGroup))

def listAdministrators(rhn, systemGroup):
    """
    usage:  listAdministrators(rhn, systemGroup)

    Lists the Administrators of a chosen system group

    returns: list of dict (basic user info)

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup              - the name of a system group
    """
    try:
        return rhn.session.systemgroup.listAdministrators(rhn.key, systemGroup)
    except Exception, E:
        return rhn.fail(E, 'list admins of group %s' % systemGroup)

def listGroupsWithoutAdmins(rhn):
    """
    usage: listGroupsWithoutAdmins(rhn)

    Lists the system groups that have no associated administrators,
    aside from org admins

    returns: list of dicts, one per group.

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.systemgroup.listGroupsWithNoAssociatedAdmins(rhn.key)
    except Exception, E:
        rhn.fail(E, 'list groups with no administrators')

def listGroupsWithNoAssociatedAdmins(rhn, systemGroup):
    """
    usage: listGroupsWithNoAssociatedAdmins(rhn, systemGroup)

    List groups with no admins assigned.

    returns: list of dict (basic user info)

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup              - the name of a system group
    """
    try:
        return rhn.session.systemgroup.listGroupsWithNoAssociatedAdmins(rhn.key, systemGroup)
    except Exception, E:
        return rhn.fail(E, 'list active systems in group %s' % systemGroup)
    
def listSystems(rhn, systemGroup):
    """
    usage:  listSystems(rhn, systemGroup)

    Lists the systems in a chosen system group

    returns: list of dicts, one per system.

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.systemgroup.listSystems(rhn.key, systemGroup)
    except Exception, E:
        return rhn.fail(E, 'list systems in group %s' % systemGroup)

def listActiveSystemsInGroup(rhn, systemGroup):
    """
    usage:  listActiveSystemsInGroup(rhn, systemGroup)

    Lists the Active systems in a chosen system group

    returns: list of int (server IDs), one per system.

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup              - the name of a system group
    """
    try:
        return rhn.session.systemgroup.listActiveSystemsInGroup(rhn.key, systemGroup)
    except Exception, E:
        return rhn.fail(E, 'list active systems in group %s' % systemGroup)

def listInactiveSystemsInGroup(rhn, systemGroup, days = 2):
    """
    usage:  listInactiveSystemsInGroup(rhn, systemGroup)

    Lists the Inactive systems in a chosen system group

    returns: list of int (server IDs), one per system.

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup              - the name of a system group
    days(int)                - number of days before a system is considered inactive.
                               default: 1
    """
    try:
        return rhn.session.systemgroup.listInactiveSystemsInGroup(rhn.key, systemGroup, days)
    except Exception, E:
        return rhn.fail(E, 'list inactive systems in group %s' % systemGroup)

def update(rhn, systemGroup, descr):
    """
    usage: update(rhn, systemGroup, descr)

    updates information about a systemgroup (description, really)

    returns: dict

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup(str)         - a system group name
    descr(str)               - group description
    """
    try:
        return rhn.session.systemgroup.update(rhn.key, systemGroup, descr)
    except Exception, E:
        return rhn.fail(E, 'update system group %s' % systemGroup )

def listAllGroups(rhn):
    """
    usage: listAllGroups(rhn)

    Retrieve a list of system groups that are accessible by the logged in user.

    returns: list(dict)

    params:
    rhn                 - authenticated rhnSession object
    """
    try:
        return rhn.session.systemgroup.listAllGroups(rhn.key)
    except Exception, E:
        rhn.fail(E, 'Failed to list system groups')

def scheduleApplyErrataToActive(rhn, systemGroup, erratalist, earliestOccurrence = None ):
    """
    usage:  listAdministrators(rhn, systemGroup)

    Lists the Administrators of a chosen system group

    returns: list of dict (basic user info)

    parameters:
    rhn                      - an authenticated RHN session
    systemGroup              - the name of a system group
    erratalist               - a list of errata IDs to apply
    earliestOccurrence       - an iso 8601 format date
                               (use datetime.datetime.isoformat())
    """
    try:
        if earliestOccurrence is not None:
            return rhn.session.systemgroup.scheduleApplyErrataToActive(rhn.key, systemGroup, erratalist, earliestOccurrence) == 1
        else:
            return rhn.session.systemgroup.scheduleApplyErrataToActive(rhn.key, systemGroup, erratalist, earliestOccurrence) == 1
    except Exception, E:
        return rhn.fail(E, 'schedule errata [%s] on active systems in group %s' % (','.join(erratalist),systemGroup))

    
