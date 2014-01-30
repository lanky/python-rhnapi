#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the 'user' namespace

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

# mapping of roles to "pretty names"
rolemaps = {
        'satellite_admin'       : 'Satellite Administrator',
        'org_admin'             : 'Organisation Administrator',
        'channel_admin'         : 'Software Channel Administrator',
        'config_admin'          : 'Configuration Channel Administrator',
        'system_group_admin'    : 'System Group Administrator',
        'activation_key_admin'  : 'Activation key Administrator',
        'monitoring_admin'      : 'Monitoring Administrator',
        'normal_user'           : 'Normal (Unprivileged) User'
        }

# ---------------------------------------------------------------------------- #

def addAssignedSystemGroup(rhn, rhnuser, groupname, isdefault):
    """
    API:
    user.addAssignedSystemGroup

    usage:
    addAssignedSystemGroup(rhn, rhnuser, groupname, isdefault)

    description:
    Add system group to user's list of assigned system groups

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - authenticated RHN Session object
    rhnuser(str)            - RHN user login name
    groupname(str)          - system group name
    isdefault(bool)         - add group as a default group
    """
    try:
        return rhn.session.user.addAssignedSystemGroup(rhn.key, rhnuser, groupname, isdefault) == 1
    except Exception, E:
        return rhn.fail(E, 'give user %s access to system group %s' %(rhnuser, groupname))

# ---------------------------------------------------------------------------- #

def addAssignedSystemGroups(rhn, rhnuser, grouplist, isdefault):
    """
    API:
    user.addAssignedSystemGroup

    usage:
    addAssignedSystemGroup(rhn, rhnuser, groupname, isdefault)

    description:
    Add a list of system groups to user's list of assigned system groups

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - authenticated RHN Session object
    rhnuser(str)            - RHN user login name
    grouplist(list of str)  - list of system group names
    isdefault(bool)         - add group as a default group
    """
    try:
        return rhn.session.user.addAssignedSystemGroup(rhn.key, rhnuser, grouplist, isdefault) == 1
    except Exception, E:
        return rhn.fail(E, 'assign system groups [%s] to user %s' %(','.join(grouplist), rhnuser))

# ---------------------------------------------------------------------------- #

def addDefaultSystemGroup(rhn, rhnuser, groupname):
    """
    API:
    user.addDefaultSystemGroup

    usage:
    addDefaultSystemGroup(rhn,rhnuser, groupname)

    description:
    Add a systemgroup to an rhnuser's list of default groups.
    Note that this does not imply group admin status, just that any systems
    registered by the rhnuser belong to this group by default.

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    groupname(str)          - the group to add as a default
    """
    try:
        return rhn.session.user.addDefaultSystemGroup(rhn.key, rhnuser, groupname) == 1
    except Exception, E:
        return rhn.fail(E, "add group %s to user %s's default system groups" % (groupname, rhnuser))

# ---------------------------------------------------------------------------- #

def addDefaultSystemGroups(rhn, rhnuser, grouplist):
    """
    API:
    user.addDefaultSystemGroup

    usage:
    addDefaultSystemGroup(rhn,rhnuser, grouplist)

    description:
    Add a list of system groups to an rhnuser's list of default groups.
    Note that this does not imply group admin status, just that any systems registered
    by this rhnuser belong to these groups by default.

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    grouplist(str)          - the group to add as a default
    """
    try:
        return rhn.session.user.addDefaultSystemGroup(rhn.key, rhnuser, grouplist) == 1
    except Exception, E:
        return rhn.fail(E, "add groups [%s] to user %s's default system groups" % (','.join(grouplist), rhnuser))

# ---------------------------------------------------------------------------- #

def addRole(rhn, rhnuser, role):
    """
    API:
    user.addRole

    usage:
    addRole(rhn, rhnuser, role)

    description:
    Add a role to an existing RHN User.
    Valid roles are:
    [ 
      'satellite_admin', 'org_admin', 'channel_admin',
      'config_admin', 'system_group_admin',
      'activation_key_admin', 'monitoring_admin'
    ]

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    role(str)               - Role to add. 
    """
    try:
        return rhn.session.user.addRole(rhn.key, rhnuser, role) == 1
    except Exception, E:
        return rhn.fail(E, "add role %s to user %s" %(role, rhnuser))

# ---------------------------------------------------------------------------- #

def create(rhn, rhnuser, password, firstname, lastname, email, enablepam = 0):
    """
    API:
    user.create

    usage:
    create(rhn, rhnuser, password, firstname, lastname, email, enablepam = 0)

    description:
    add a new rhn user.

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - authenticated RHN Session Object
    rhnuser(str)            - user name
    password(str)           - desired password
    firstname(str)          - first name
    lastname(str)           - last name
    email(str)              - email address
    enablepam(int)          - use pam authentication for this user 1 => yes, 0 => no
    """
    try:
        return rhn.session.user.create(rhn.key, rhnuser, password, firstname, lastname, email, enablepam) == 1
    except Exception, E:
        return rhn.fail(E, 'create user %s' % rhnuser)

# ---------------------------------------------------------------------------- #

def delete(rhn, rhnuser):
    """
    API:
    user.delete

    usage:
    deleteUser(rhn, rhnuser)

    description:
    Delete an existing RHN user

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    """
    try:
        return rhn.session.user.delete(rhn.key, rhnuser) == 1
    except Exception, E:
        return rhn.fail(E, 'delete user %s' % rhnuser)

# ---------------------------------------------------------------------------- #

def disable(rhn, rhnuser):
    """
    API:
    user.disable
    
    usage:
    disable(rhn, rhnuser)

    description:
    Disable (but not remove) an existing rhn account

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    """
    try:
        return rhn.session.user.disable(rhn.key, rhnuser) == 1
    except Exception, E:
        return rhn.fail(E, 'disable user %s' % rhnuser)

# ---------------------------------------------------------------------------- #

def enable(rhn, rhnuser):
    """
    API:
    user.enable

    usage:
    enable(rhn, rhnuser)
    
    description:
    Enable a currently disabled rhn account

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    """
    try:
        return rhn.session.user.enable(rhn.key, rhnuser) == 1
    except Exception, E:
        return rhn.fail(E, 'disable user %s' % rhnuser)

# ---------------------------------------------------------------------------- #

def getDetails(rhn, rhnuser):
    """
    API:
    user.getDetails

    usage:
    getDetails(rhn, rhnuser)
    
    description:
    Looks up detailed info about a specific rhn user

    returns:
    dict (user information)
        {
          'first_names' (str)     : (deprecated),
          'first_name' (str)      : user first name,
          'last_name' (str)       : user last name,
          'email' (str),          : user email,
          'created_date' (str)    : date user created,
          'last_login_date' (str) : date last login,
          'prefix' (str)          : prefix (Mr., Sr. etc)
          'enabled' (bool)        : is the user account enabled?
          'use_pam' (bool)        : does the account use pam authentication?
        }

    parameters:
    rhn                     - an authenticated RHN session.
    rhnuser(str)            - RHN user account name
    """
    try:
        return rhn.session.user.getDetails(rhn.key, rhnuser)
    except Exception, E:
        return rhn.fail(E, 'retrieve info for user %s' % rhnuser)

# ---------------------------------------------------------------------------- #

def getLoggedInTime(rhn, rhnuser):
    """
    API:
    user.getLoggedInTime

    usage:
    getLoggedInTime(rhn, rhnuser)

    description:
    last login time for the specified user account

    returns:
    dateTime.iso8601

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    """
    try:
        return rhn.session.getLoggedInTime(rhn.key, rhnuser) 
    except Exception, E:
        return rhn.fail(E,'retrieve last login for user %s' % rhnuser)

# ---------------------------------------------------------------------------- #

def listAssignableRoles(rhn):
    """
    API:
    user.listAssignableRoles

    usage:
    listAssignableRoles(rhn)

    description:
    List all roles that the logged-in user can assign to others

    returns:
    list of str (role labels)

    parameters:
    rhn                     - an authenticated RHN session
    """
    try:
        return rhn.session.user.listAssignableRoles(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list roles assignable by user %s' % rhn.login)

# ---------------------------------------------------------------------------- #

def listAssignedSystemGroups(rhn, rhnuser):
    """
    API:
    user.listAssignedSystemGroups

    usage:
    listAssignedSystemGroups(rhn, rhnuser)

    description:
    Returns the system groups that a user can administer.

    returns:
    list of dict, one per assigned group
        {
          'id' (int)           : group ID
          'name' (str)         : group Name
          'sysdesciption' (str)  : group sysdesciption
          'org_id' (int)       : RHN org the group is in
          'system_count' (int) : number of systems in the group
        }

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    """
    try:
        return rhn.session.user.listAssignedSystemGroups(rhn.key, rhnuser) 
    except Exception, E:
        return rhn.fail(E,'list system groups administered by user %s' % rhnuser)

# ---------------------------------------------------------------------------- #

def listDefaultSystemGroups(rhn, rhnuser):
    """
    API:
    user.listDefaultSystemGroups

    usage:
    listDefaultSystemGroups(rhn, rhnuser)

    description:
    list a user's default system groups

    returns:
    list of dict, one per group
        {
          'id' (int)           : group ID
          'name' (str)         : group Name
          'sysdesciption' (str)  : group sysdesciption
          'org_id' (int)       : RHN org the group is in
          'system_count' (int) : number of systems in the group
        }
            
    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    """
    try:
        return rhn.session.user.listDefaultSystemGroups(rhn.key, rhnuser) 
    except Exception, E:
        return rhn.fail(E,'list default system groups for user %s' % rhnuser)

# ---------------------------------------------------------------------------- #

def listRoles(rhn,rhnuser, pretty = False):
    """
    API:
    user.listRoles (with additional arg)

    usage:
    listRoles(rhn,rhnuser, pretty = False)

    description:
    Show the roles assigned to an rhn user
    org and satellite admins inherit all subroles, so
    only the toplevel role is returned
    the 'pretty' arg shows role names rather than labels

    returns:
    list of str (role labels)

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - list roles for this user
    pretty(bool)            - print full names rather than labels (org_admin => Organisation Administrator)
    """
    try:
        roles = rhn.session.user.listRoles(rhn.key, rhnuser)
        if len(roles) == 0:
            roles = [ 'normal_user' ]
        elif 'satellite_admin' in roles:
            roles = [ 'satellite_admin']
        elif 'org_admin' in roles:
            roles = [ 'org_admin' ]
        if pretty:
            return [ rolemaps[x] for x in roles ]
        else:
            return roles
    except Exception, E:
        return rhn.fail(E, 'list roles for user %s' % rhnuser)

# ---------------------------------------------------------------------------- #

def listUsers(rhn):
    """
    API:
    user.listUsers

    usage:
    listUsers(rhn)
    
    description:
    lists all existing RHN user accounts.

    returns:
    list of dict, one per user:
        {
          'id' (int)       : user ID
          'login' (str)    : user login
          'login_uc' (str) : user login in uppercase
          'enabled' (bool) : if the user is enabled
        }

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.user.listUsers(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list users on rhn server %s' % rhn.hostname)

# ---------------------------------------------------------------------------- #

def removeAssignedSystemGroup(rhn, rhnuser, groupname, isdefault):
    """
    API:
    user.removeAssignedSystemGroup

    usage:
    removeAssignedSystemGroup(rhn, rhnuser, groupname, isdefault)

    description:
    Remove the specified group from a users list of assigned groups

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - authenticated RHN Session object
    rhnuser(str)            - RHN user login name
    groupname(str)          - system group name
    isdefault(bool)         - also remove group from user's default groups
    """
    try:
        return rhn.session.user.removeAssignedSystemGroup(rhn.key, rhnuser, groupname, isdefault) == 1
    except Exception, E:
        return rhn.fail(E, 'remove user %s access to system group %s' %(rhnuser, groupname))

# ---------------------------------------------------------------------------- #

def removeAssignedSystemGroups(rhn, rhnuser, grouplist, isdefault):
    """
    API:
    user.removeAssignedSystemGroups

    usage:
    removeAssignedSystemGroups(rhn, rhnuser, groupname, isdefault)

    description:
    remove a list of system groups from a user's list of assigned system groups

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - authenticated RHN Session object
    rhnuser(str)            - RHN user login name
    grouplist(list of str)  - list of system group names
    isdefault(bool)         - also remove groups from user's detfault group list.
    """
    try:
        return rhn.session.user.removeAssignedSystemGroup(rhn.key, rhnuser, grouplist, isdefault) == 1
    except Exception, E:
        return rhn.fail(E, 'remove system groups [%s] from user %s' %(','.join(grouplist), rhnuser))

# ---------------------------------------------------------------------------- #

def removeDefaultSystemGroup(rhn, rhnuser, groupname):
    """
    API:
    user.removeDefaultSystemGroup

    usage:
    removeDefaultSystemGroup(rhn,rhnuser, groupname)

    description:
    Remove a systemgroup from an rhnuser's list of default groups.

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    groupname(str)          - the group to remove as a default
    """
    try:
        return rhn.session.user.removeDefaultSystemGroup(rhn.key, rhnuser, groupname) == 1
    except Exception, E:
        return rhn.fail(E, "remove group %s to user %s's default system groups" % (groupname, rhnuser))

# ---------------------------------------------------------------------------- #

def removeDefaultSystemGroups(rhn, rhnuser, grouplist):
    """
    API:
    user.removeDefaultSystemGroup

    usage:
    removeDefaultSystemGroup(rhn,rhnuser, grouplist)

    description:
    Remove a list of system groups from an rhnuser's list of default groups.

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    grouplist(str)          - the group to remove as a default
    """
    try:
        return rhn.session.user.removeDefaultSystemGroup(rhn.key, rhnuser, grouplist) == 1
    except Exception, E:
        return rhn.fail(E, "remove groups [%s] from user %s's default system group list" % (','.join(grouplist), rhnuser))

# ---------------------------------------------------------------------------- #

def removeRole(rhn, rhnuser, role):
    """
    API:
    user.removeRole

    usage:
    removeRole(rhn, rhnuser, role)

    description:
    remove a role from a user 

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    """
    try:
        return rhn.session.user.removeRole(rhn.key,rhnuser, role )
    except Exception, E:
        return rhn.fail(E, "remove role %s from user %s" % (role, rhnuser))

# ---------------------------------------------------------------------------- #

def setDetails(rhn, rhnuser, userinfo):
    """
    API:
    user.setDetails

    usage:
    setDetails(rhn, rhnuser, userinfo)

    description:
    change details about a specific rhn user

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    userinfo(dict)          - RHN user info as a dict (see above)

    """
    try:
        return rhn.session.user.setDetails(rhn.key,rhnuser, userinfo) == 1
    except Exception, E:
        return rhn.fail(E, 'retrieve info for user %s' % rhnuser)

# ---------------------------------------------------------------------------- #

def setDetailsByArg(rhn, rhnuser, **kwargs):
    """
    API:
    none, special case of user.setDetails with variable args

    usage:
    setDetailsByArg(rhn, rhnuser, key1=val1, key2=val2,...)

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    
    plus one or more of the following as key=value parameters
    'first_name' (str)      - user's first name(s) 
    'last_name' (str)       - user's last name(s)
    'email' (str)           - user's email address
    'prefix' (str)          - prefix (one of ['Dr.', 'Hr.'', 'Miss', 'Mr.', 'Mrs', 'Ms.', 'Sr.'])
    'password' (str)        - user password
    """
    try:
        return rhn.session.user.setDetails(rhn.key,rhnuser, kwargs) == 1
    except Exception, E:
        return rhn.fail(E, 'retrieve info for user %s' % rhnuser)

# ---------------------------------------------------------------------------- #

def usePamAuthentication(rhn, rhnuser, enablepam):
    """
    API:
    user.usePamAuthentication

    usage:
    usePamAuthentication(rhn, rhnuser, enablepam)

    description:
    enable or disable PAM Authentication for an RHN user

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session
    rhnuser(str)            - RHN user account
    enablepam(int)            - whether to enable or disable PAM authentication
                              1 => enable, 0 => disable
    """
    if enablepam == 1:
        task = 'enable'
    else:
        task = 'disable'
    try:
        return rhn.session.user.usePamAuthentication(rhn.key, rhnuser, enablepam) == 1
    except Exception, E:
        return rhn.fail(E,'%s PAM Authentication for user %s' %( task, rhnuser))

# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
