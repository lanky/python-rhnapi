#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstrating the 'org' namespace
# and its sub-namespaces
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
rhnapi.org
An abstraction of the org and org.trusts namespaces from the RHN Satellite API for
RHN Satellite versions >= 5.4 (may work on earlier versions, but not tested)
As these are organization administration functions, they will require the use of an
RHN Satellite user account with at least Org Admin privileges and probably (at least
for creation and deletion of organizations) Satellite Admin privileges.
"""

__author__ = "Stuart Sears"

# org
#    * create
#    * delete
#    * getDetails
#    * getDetails
#    * listOrgs
#    * listSoftwareEntitlements
#    * listSoftwareEntitlements
#    * listSoftwareEntitlements
#    * listSoftwareEntitlementsForOrg
#    * listSystemEntitlements
#    * listSystemEntitlements
#    * listSystemEntitlements
#    * listSystemEntitlementsForOrg
#    * listUsers
#    * migrateSystems
#    * setSoftwareEntitlements
#    * setSoftwareFlexEntitlements
#    * setSystemEntitlements
#    * updateName

# ----------------------------------- org  ----------------------------------- #
def create(rhn, orgname, admlogin, admpass, admprefix, admfirst,
     admlast, admemail, pamauth = False):
    """
    API:
    org.create

    usage:
    create(rhn, orgname, admlogin, admpass, admprefix, admfirst,
            admlast, admemail, pamauth)

    description:
    Creates a new organization and its associated administrative account.
    This account must be unique on the satellite.

    returns:
    dict (org info)

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
    orgname(str)            - name for the new organization
    admlogin(str)           - Org admin username
    admpass(str)            - Org Admin user's admpassword
    admprefix(str)          - admprefix ('title') - one of
                              [ 'Dr.' , 'Hr.' , 'Miss' , 'Mr.' , 'Mrs.' , 'Ms.' , 'Sr.']
    admfirst(str)           - Admin user's first (christian) name
    admlast(str)            - admin user's last (family) name
    admemail(str)           - admin user's admemail address
    pamauth(bool)           - if the admin user account uses PAM authentication [False]
    """
    try:
        return rhn.session.org.create(rhn.key, orgname, admlogin, admpass, admprefix,
                    admfirst, admlast, admemail, pamauth)
    except Exception, E:
        return rhn.fail(E, 'create organization %s with admin login %s' %(orgname, admlogin))

# ---------------------------------------------------------------------------- #

def delete(rhn, orgid):
    """
    API:
    org.delete

    usage:
    delete(rhn, orgid)

    description:
    deletes the organization with the specified org ID. It is not possible to delete org ID 1.
    This requires Satellite Administrator privileges.

    returns:
    Bool

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)              - The RHN Org Identifier
    """
    try:
        return rhn.session.org.delete(rhn.key, orgid) == 1
    except Exception, E:
        return rhn.fail(E, 'delete Org ID %d' % orgid)

# ---------------------------------------------------------------------------- #

def getDetails(rhn, orgspec):
    """
    API:
    org.getDetails

    usage:
    getDetails(rhn, orgspec)

    description:
    looks up information about the chosen organization.
    You may specify organisation by name or numerical ID

    returns:
    dict (org info)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgspec(int OR str)       - name(str) or id(int) of an organization
    """
    try:
        return rhn.session.org.getDetails(rhn.key, orgspec)
    except Exception, E:
        return rhn.fail(E, 'get information about org %s' % str(orgspec))

# ---------------------------------------------------------------------------- #

def listOrgs(rhn):
    """
    API:
    org.listOrgs

    usage:
    listOrgs(rhn)

    description:
    Lists the existing organizations on the satellite.
    Returns the same information as getDetails, but for ALL organisations.

    returns:
    list of dict (org info)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.org.listOrgs(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list organizations on the satellite %s' % rhn.hostname)


# show usage of software entitlements across all your orgs

def listSoftwareEntitlements(rhn, entlabel = None, unentitled = False):
    """
    usage: listSoftwareEntitlements(rhn)

    List software entitlement allocation information across all organizations.
    Requires satellite administrator privileges.

    returns: list/dict

    parameters: [* = optional]
    rhn                     - authenticated rhnapi.rhnSession() object
    *entlabel(str)          - software channel/entitlement label
    *unentitled(bool)       - also show orgs without this specific entitlement
                              This can only be specified with 'entlabel' and will
                              be ignored otherwise
    """
    try:
        if entlabel is not None:
            res = rhn.session.org.listEntitlements(rhn.key, entlabel, unentitled)
            if res == -1:
                res = "unlimited"
        else:
            res = rhn.session.org.listEntitlements(rhn.key)
        return res
    except Exception, E:
        if entlabel is not None:
            return rhn.fail(E, 'List usage of entitlement %s across all orgs' % entlabel)
        return rhn.fail(E, 'List software entitlement usage across all orgs')

# show usage of a specific softw
def ListSoftwareEntitlementsForOrg(rhn, orgid):
    """
    usage: ListSoftwareEntitlementsForOrg(rhn, orgid)

    shows an organization's allocation of each available software entitlement
    a value of -1 means 'unlimited'

    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - numerical organzation ID
    """
    try:
        return rhn.session.org.ListSoftwareEntitlementsForOrg(rhn.key, orgid)
    except Exception, E:
        return rhn.fail(E, 'List software entitlements for org %(id)d (%(name)s)' % getDetails(rhn, orgid) )

def ListSystemEntitlements(rhn, label = None, unentitled = False):
    """
    usage: ListSystemEntitlements(rhn, label, includeUnentitled)

    list allocation of either all system entitlements across orgs, or a
    specified system entitlement

    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    *label(str)              - software channel/entitlement label
    *includeUnentitled(bool) - also show orgs without this specific entitlement
                               This can only be specified with 'entlabel' and will
                               be ignored otherwise
    """
    try:
        if label is not None:
            return rhn.session.org.ListSystemEntitlements(rhn.key, label, unentitled)
        else:
            return rhn.session.org.ListSystemEntitlements(rhn.key)
    except Exception, E:
        if label is not None:
            return rhn.fail(E, 'list usage of systemn entitlement %s across orgs' % label)
        return rhn.fail(E, 'list usage of all system entitlements across orgs')

def ListSystemEntitlementsForOrg(rhn, orgid):
    """
    usage: SystemEntitlementsForOrg(rhn, orgid)

    List an organization's allocation of each system entitlement.

    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - numerical organzation ID
    """
    try:
        return rhn.session.org.ListSystemEntitlementsForOrg(rhn.key, orgid)
    except Exception, E:
        return rhn.fail(E, 'list system entitlement usage for org %(id)d (%(name)s)' % getDetails(rhn, orgid) )

def listUsers(rhn, orgid):
    """
    usage: listUsers(rhn, orgid)

    lists the user accounts in a given organization.

    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - organization ID
    """
    try:
        return rhn.session.org.listUsers(rhn.key, orgid)
    except Exception, E:
        return rhn.fail(E, 'list users in org %(id)d (%(name)s)' % getDetails(rhn, orgid) )

def migrateSystems(rhn, dest_orgid, systemlist):
    """
    usage: migrateSystems(rhn, destorgid, systemlist)

    Migrate systems from one org to another. Behaviour can depend on the privileges of the
    user performing the migration:
    This requires that there is a trust configured between the current org of the chosen
    systems and the destination org.

    Satellite admins can migrate systems between any 2 orgs with a trust relationship.
    Org admins can only migrate sysems from their own org to another trusted one.

    returns: list/int

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    dest_orgid(int)          - org ID for destination org
    systemlist(list/int)     - list of system IDs
    """
    try:
        return rhn.session.org.migrateSystems(rhn.key, dest_orgid, systemlist)
    except Exception, E:
        return rhn.fail(E, 'Migrate systems to org %d' % dest_orgid)


def setSoftwareEntitlements(rhn, orgid, label, allocation):
    """
    usage: setSoftwareEntitlements(rhn, orgid, label, allocation)

    Set an organization's entitlement allocation for the given software
    entitlement. If increasing the entitlement allocation, the default
    organization (i.e. orgId=1) must have a sufficient number of free
    entitlements


    returns: True, or throws exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - organization to set entitlements for
    label(str)               - label for the chosen entitlement
    allocation(int)          - how many entitlements to allocate
    """
    try:
        return rhn.session.org.setSoftwareEntitlements(rhn.key, orgid, label, allocation) == 1
    except Exception, E:
        orginfo = "%(id)d (%(name)s)" % getDetails(rhn, orgid)
        return rhn.fail(E, 'allocate %d entitlements for %s to org %s' %(allocation, label, orginfo) )


def setSoftwareFlexEntitlements(rhn, orgid, label, allocation):
    """
    usage: setSoftwareFlexEntitlements(rhn, orgid, label, allocation)

    Set an organization's entitlement allocation for the given software
    entitlement. If increasing the entitlement allocation, the default
    organization (i.e. orgId=1) must have a sufficient number of free
    flex entitlements


    returns: True, or throws exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - organization to set entitlements for
    label(str)               - label for the chosen entitlement
    allocation(int)          - how many entitlements to allocate
    """
    try:
        return rhn.session.org.setSoftwareFlexEntitlements(rhn.key, orgid, label, allocation) == 1
    except Exception, E:
        orginfo = "%(id)d (%(name)s)" % getDetails(rhn, orgid)
        return rhn.fail(E, 'allocate %d flex entitlements for %s to org %s' %(allocation, label, orginfo))

def setSystemEntitlements(rhn, orgid, label, allocation):
    """
    usage: setSystemEntitlements(rhn, orgid, label, allocation)

    Set an organization's entitlement allocation for the given software
    entitlement. If increasing the entitlement allocation, the default
    organization (i.e. orgId=1) must have a sufficient number of free
    entitlements


    returns: True, or throws exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - organization to set entitlements for
    label(str)               - label for the chosen entitlement:
                               one of ['enterprise_entitled',
                                       'monitoring_entitled',
                                       'provisioning_entitled',
                                       'virtualization_host',
                                       'virtualization_platform' ]
    allocation(int)          - how many entitlements to allocate
    """
    try:
        return rhn.session.org.setSystemEntitlements(rhn.key, orgid, label, allocation) == 1
    except Exception, E:
        orginfo = "%(id)d (%(name)s)" % getDetails(rhn, orgid)
        return rhn.fail(E, 'allocate %d %s entitlements to org %s' %(allocation, label, orginfo) )

def updateName(rhn, orgid, newname):
    """
    usage: updateName(rhn, orgid, newname)


    returns:

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - organization ID to rename
    newname(str)             - new organizaiton name
    """
    try:
        return rhn.session.org.updateName(rhn.key, orgid, newname)
    except Exception, E:
        return rhn.fail(E, 'change name for organization %(id)d (%(name)s)' % getDetails(rhn, orgid) )

# -------------------------------- org.trusts -------------------------------- #

def addTrust(rhn, orgid, trustorgid):
    """
    API:
    org.trusts.addTrust

    usage:
    addTrust(rhn, orgid, trustorgid)

    description:
    Adds a new organizational trust to the specified org.

    returns:
    Bool

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - Organization ID
    trustorgid(int)        - Org ID you wish to trust
    """
    try:
        return rhn.session.org.trusts.addTrust(rhn.key, orgid, trustorgid) == 1
    except Exception, E:
        return rhn.fail(E, 'add a new trust for org %d to org %d' %(trustorgid, orgid))

# ---------------------------------------------------------------------------- #

def getTrustDetails(rhn, trustorgid):
    """
    API:
    org.trusts.getDetails

    usage: getTrustDetails(rhn, orgid)
    abstraction of org.trusts.getDetails (to avoid name clashes)

    display the details for a given trusted org
    from the perspective of the user's org.

    returns:
    dict (trusted org info)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - organization ID
    """
    try:
        return rhn.session.org.trusts.getDetails(rhn.key, trustorgid)
    except Exception, E:
        return rhn.fail(E, 'get details about trusted org %d' % trustorgid)

# ---------------------------------------------------------------------------- #

def listChannelsConsumed(rhn, trustorgid):
    """
    API:
    org.trusts.listChannelsConsumed

    usage:
    listChannelsConsumed(rhn, trustorgid)

    description:
    Lists all software channels that the organization given may consume from
    the user's organization.

    returns:
    list of dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    trustorgid(int)               - organization ID
    """
    try:
        return rhn.session.org.trusts.listChannelsConsumed(rhn.key, trustorgid)
    except Exception, E:
        return rhn.fail(E, 'list channels consumed by org %d' % trustorgid )

# ---------------------------------------------------------------------------- #

def listChannelsProvided(rhn, trustorgid):
    """
    API:
    org.trusts.listChannelsProvided

    usage:
    listChannelsProvided(rhn, trustorgid)

    description:
    Lists all software channels that the organization given is providing
    to the user's organization.

    returns:
    list of dict (channel info)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    trustorgid(int)               - organization ID
    """
    try:
        return rhn.session.org.trusts.listChannelsProvided(rhn.key, trustorgid)
    except Exception, E:
        return rhn.fail(E, 'list channels provided to your org by org %d' % trustorgid)

# ---------------------------------------------------------------------------- #

def listTrustedOrgs(rhn):
    """
    API:
    org.trusts.listOrgs

    usage:
    listTrustedOrgs(rhn)

    description:
    List all organanizations trusted by the user's organization.

    returns:
    list of dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.org.trusts.listOrgs(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list orgs trusted by your organization')

# ---------------------------------------------------------------------------- #

def listSystemsAffected(rhn, orgid, trustedorgid):
    """
    API:
    org.trusts.listSystemsAffected

    usage:
    listSystemsAffected(rhn, orgid, trustedorgid)

    description:
    Get a list of systems within the trusted organization that would be affected
    if the trust relationship was removed.
    This basically lists systems that are using at least one shared package

    returns:
    list of dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - your organization ID
    trustedorgid(int)        - trusted organization ID
    """
    try:
        return rhn.session.org.trusts.listSystemsAffected(rhn.key, orgid, trustedorgid)
    except Exception, E:
        return rhn.fail(E, 'list systems affected by removing the trust between orgs %d and %d' %(orgid, trustedorgid))

# ---------------------------------------------------------------------------- #

def listTrusts(rhn, orgid):
    """
    API:
    org.trusts.listTrusts

    usage:
    listTrusts(rhn, orgid)

    description:
    Returns the list of organizations trusted by the given org id

    Requires Satellite Administrator privileges

    returns:
    list of dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - organization ID
    """
    try:
        return rhn.session.org.trusts.listTrusts(rhn.key, orgid)
    except Exception, E:
        return rhn.fail(E, 'list orgs trusted by org id %d' % orgid)

# ---------------------------------------------------------------------------- #

def removeTrust(rhn, orgid, trustedorgid):
    """
    API:
    org.trusts.removeTrust

    usage:
    removeTrust(rhn, orgid, trustedorgid)

    description:
    removes an organization trust from the given org.

    Requires Satellite Administrator privileges

    returns:
    Bool

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - your organization ID
    trustedorgid(int)        - trusted organization ID
    """
    try:
        return rhn.session.org.trusts.removeTrust(rhn.key, orgid, trustedorgid) == 1
    except Exception, E:
        return rhn.fail(E, 'remove the trust between org %d and %d' %(orgid, trustedorgid))

# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
