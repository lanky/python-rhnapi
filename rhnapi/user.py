#!/usr/bin/env python
# -*- coding: utf-8 -*-
# the user namespace API calls for RHN
# import asrhn.user

# do I need to do this?
#import rhnapi
#### Actual API Calls #####

def listUsers(rhn):
    """
    Usage: listUsers(rhn)
    
    lists all existing RHN user accounts.

    returns: list of dicts

    params:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.user.listUsers(rhn.key)
    except Exception, E:
        rhn.fail(E, 'retrieve userlist from rhn server %s' % rhn.hostname)

def getDetails(rhn,rhnuser):
    """
    usage: getDetails(rhn,rhnuser)
    
    Looks up detailed info  about a specific rhn user

    returns: dict
        { 'created_date', 'email', 'first_names',
         'last_login_date', 'last_name' 'prefix'}

    params:
    rhn                     - an authenticated RHN session.
    rhnuser(str)            - username
    """
    try:
        return rhn.session.user.getDetails(rhn.key,rhnuser)
    except Exception, E:
        rhn.fail(E, 'retrieve info for user %s' %rhnuser)

def setDetails(rhn,rhnuser):
    """
    usage: setDetails(rhn,rhnuser)

    change details about a specific rhn user
    needs to be wrapped in a script.
    """
    try:
        rhn.session.user.setDetails(rhn.key,rhnuser)
    except Exception, E:
        rhn.fail(E, 'retrieve info for user %s' %rhnuser)

def createUser(rhn, rhnuser, password, firstname, lastname, email, usePAM=0):
    """
    add a new rhn user.
    params:
    rhnuser (str)    -    user name
    password (str)    -    desired password
    firstname (str)-    first name
    lastname (str)    -    last name
    email (str)    -    email address
    usePAM (int 0/1) -    use pam authentication for this user. False by default.
    """
    try:
        rhn.session.user.create(rhn.key,rhnuser, password, firstname, lastname, email, usePAM)
    except Exception, E:
        rhn.fail(E, 'add user %s' %rhnuser)

def createRHNUser(rhn, user_info):
    """
    Create a new user within your organisation on RHN Hosted (rhn.redhat.com)
    params:
    rhn                 authenticated RHN Session object
    user_info:       dict with the following information:
     string "address1"
    string "address2" (optional)
    string "city"
    string "country" (two-character country code)
    string "email"
    string "first_names"
    string "last_name"
    string "login"
    string "password"
    string "phone"
    string "prefix" (one of Dr. , Hr. , Miss , Mr. , Mrs. , Ms. , Sr. )
    string "state"
    string "zip"
    """
    try:
        rhn.session.user.create(rhn.key, user_info)
    except Exception, E:
        rhn.fail(E, 'add user %s' % user_info['login'])
    

def disableUser(rhn,rhnuser):
    """
    Disable (but not remove) an existingrhn account
    """
    try:
        rhn.session.user.disable(rhn.key,rhnuser)
    except Exception, E:
        rhn.fail(E, 'disable user %s' %rhnuser)

def enableUser(rhn,rhnuser, fail_silently=True):
    """
    Enable A currently disabled rhn account
    """
    try:
        rhn.session.user.enable(rhn.key,rhnuser)
    except Exception, E:
        if fail_silently:
            pass
        else:
            RHNFailure(E, 'disable user %s' %rhnuser)

def deleteUser(rhn,rhnuser):
    """
    Delete an existing RHN user
    """
    try:
        rhn.session.user.delete(rhn.key,rhnuser)
    except Exception, E:
        rhn.fail(E, 'delete user %s' %rhnuser)


##### Role manipulation... ####
def getRoles(rhn,rhnuser, prettynames=False):
    """
    show the roles associated with anrhn user
    params:
    rhn - an authenticated RHN session
    rhnuser (str) - list roles for this user
    prettynames (bool) - print full names rather than short names for the roles.
    """
    roledict = {
            'satellite_admin' : 'Satellite Administrator',
            'org_admin' : 'Organisation Administrator',
            'channel_admin' : 'Software Channel Administrator',
            'config_admin' : 'Configuration Channel Administrator',
            'system_group_admin' : 'System Group Administrator',
            'activation_key_admin' : 'Activation key Administrator',
            'monitoring_admin' : 'Monitoring Administrator',
            'normal_user' : 'Normal (Unprivileged) User'
            }
    try:
        roles = rhn.session.user.listRoles(rhn.key,rhnuser)
        print len(roles)
        if len(roles) == 0:
            roles = [ 'normal_user' ]
        if 'satellite_admin' in roles:
            roles = [ 'satellite_admin']
        elif 'org_admin' in roles:
            roles = [ 'org_admin' ]
        if prettynames:
            return [ roledict[x] for x in roles ]
        else:
            return roles
    except Exception, E:
        rhn.fail(E, 'list roles for user %s' %rhnuser)


def addRole(rhn,rhnuser, role, fail_silently=True):
    """
    add a new role to anrhn user.
    """
    try:
        rhn.session.user.addRole(rhn.key,rhnuser, role)
    except Exception, E:
        if fail_silently:
            pass
        else:
            rhn.fail(E, "grant role %s to user %s" %(role,rhnuser))


def removeRole(rhn,rhnuser, role, fail_silently=True):
    """
    remove a role from an rhn user.
    """
    try:
        rhn.session.user.removeRole(rhn.key,rhnuser, role )
    except Exception, E:
        if fail_silently:
            pass
        else:
            rhn.fail(E, "remove role %s from user %s" % (role,rhnuser))




def giveGroup(rhn,rhnuser, groupname, asdefault=False):
    """
    Add a specified system group to the given RHN user
    params:
    RHN - an authenticated RHN xmlRPC session and its associated key
    rhnuser (str)     an existing RHN user
    groupname (str)     an existing systemgroup to add to the user
    asdefault (bool)    make this a default group (false)
    """
    try:
        rhn.session.user.AddAssignedSystemGroup(rhn.key,rhnuser, systemgroup, asdefault)
    except Exception, E:
        rhn.fail(E, 'grant user %s admin access to group %s' % (rhnuser, groupname) )


def giveGroupList(rhn, username, grouplist, asdefault=False):
    """
    give an  RHN user admin rights over a list of system groups
    params:
    rhn - an authenticated RHN xmlRPC session and its associated key
    rhnuser (str)     an existing RHN user
    grouplist (str)     an existing systemgroup to add to the user
    asdefault (bool)    make this a default group (false)
    """
    try:
        rhn.session.user.AddAssignedSystemGroups(rhn.key,rhnuser, grouplist, asdefault)
    except Exception, E:
        rhn.fail(E, 'add one or more groups to %s' %rhnuser)

def addDefaultGroup(rhn,rhnuser, groupname):
    """
    Add a systemgroup to anrhnuser's list of default groups. Note that this does not imply group admin status,
    just that any systems registered using this username belong to this group by default.
    params:
    rhn - an authenticated RHN session
    rhnuser - RHN user account
    groupname - the group to add as a default
    """
    try:
        rhn.session.user.addDefaultSystemGroup(rhn.key,rhnuser, groupname)
    except Exception, E:
        rhn.fail(E, "add group %s to user %s's default system groups" % (groupname,rhnuser))

def addDefaultGroupList(rhn,rhnuser, grouplist):
    """
    Add a systemgroup to anrhnuser's list of default groups. Note that this does not imply group admin status,
    just that any systems registered using this username belong to this group by default.
    params:
    rhn - an authenticated RHN session
    rhnuser - RHN user account
    grouplist - the group to add as a default
    """
    try:
        rhn.session.user.addDefaultSystemGroups(rhn.key,rhnuser, grouplist)
    except Exception, E:
        rhn.fail(E, "add group %s to user %s's default system groups" % (groupname,rhnuser))

def listGroups(rhn, rhnuser):
    """
    List the system groups managed by the given rhnuser
    params:
    rhn - an authenticated RHN session
    rhnuser - RHN user account
    """
    try:
        usergroups = rhn.session.user.listAssignedSystemGroups(rhn.key,rhnuser)
        return [ ( x['name'], x['description'] ) for x in usergroups ]
    except Exception, E:
        rhn.fail(E, "list system groups for user %s" % (rhnuser))

def listDefaultGroups(rhn,rhnuser):
    """
    Add a systemgroup to anrhnuser's list of default groups. Note that this does not imply group admin status,
    just that any systems registered using this username belong to this group by default.
    params:
    rhn - an authenticated RHN session
    rhnuser - RHN user account
    grouplist - the group to add as a default
    """
    try:
        return rhn.session.user.listDefaultSystemGroups(rhn.key,rhnuser)
    except Exception, E:
        rhn.fail(E, "list default system groups for user %s" % (rhnuser))
    
 
