#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
rhnapi.org
An abstraction of the org and org.trusts namespaces from the RHN Satellite API for 
RHN Satellite versions >= 5.4 (may work on earlier versions, but not tested)
As these are organization administration functions, they will require the use of an
RHN Satellite user account with at least Org Admin privileges and probably (at least
for creation and deletion of organizations) Satellite Admin privileges.
"""

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

## ---- org namespace functionality ---------------------------------------------- ##
def createOrganization(rhn, org_name, admin_login, admin_pass, admin_prefix, admin_firstname,
     admin_lastname, admin_email, usePAM = False):
    """
    usage: createOrganization(rhn, org_name, admin_login, admin_pass, admin_prefix, admin_firstname,
            admin_lastname, admin_email, usePAM)

    Creates a new organization and its associated administrative account.
    This account must be unique on the satellite.

    returns: dict (org info) or exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    org_name(str)            - name for the new organization

    Plus parameters for creating the new user.
    admin_login(str)         - Org admin username
    admin_pass(str)          - Org Admin user's password
    admin_prefix(str)        - prefix ('title') - one of
                          [ 'Dr.' , 'Hr.' , 'Miss' , 'Mr.' , 'Mrs.' , 'Ms.' , 'Sr.']
    admin_firstname(str)     - Admin user's first (christian) name
    admin_lastname(str)      - admin user's last (family) name
    admin_email(str)         - admin user's email address
    usePAM(bool)              - if the admin user account uses PAM authentication [False]
    """
    try:
        return rhn.session.org.create(rhn.key, org_name, admin_login, admin_pass, admin_prefix,
                    admin_firstname, admin_lastname, admin_email, usePAM)
    except Exception, E:
        return rhn.fail(E, 'create organization %s with admin login %s' %(org_name, admin_login))

def deleteOrganization(rhn, org_id):
    """
    usage: deleteOrganization(rhn, org_id)

    deletes the organization with the specified org ID. It is not possible to delete org ID 1.
    This requires Satellite Administrator privileges.

    returns: True, or throws exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    org_id(int)              - The RHN Org Identifier
    """
    try:
        return rhn.session.org.delete(rhn.key, org_id) == 1
    except Exception, E:
        return rhn.fail(E, 'delete Org ID %d' % org_id)

def getDetails(rhn, org_id):
    """
    usage: getDetails(rhn, org_id)

    looks up information about the chosen organization

    returns: dict, or Exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    org_id(int OR str)       - name(str) or id(int) of an organization
    """
    try:
        return rhn.session.org.getDetails(rhn.key, org_id)
    except Exception, E:
        return rhn.fail(E, 'get information about org %s' % str(org_id))

def listOrgs(rhn):
    """
    usage: listOrgs(rhn)

    Lists the existing organizations on the satellite.
    
    returns: list/dict, or throws exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.org.listOrgs(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list organizations on the satellite %s' % rhn.hostname)


# show usage of software entitlements across all your orgs

def listSoftwareEntitlements(rhn, ent_label = None, includeUnentitled = False):
    """
    usage: listSoftwareEntitlements(rhn)

    List software entitlement allocation information across all organizations.
    Requires satellite administrator privileges.
    
    returns: list/dict

    parameters: [* = optional]
    rhn                      - authenticated rhnapi.rhnSession() object
    *ent_label(str)          - software channel/entitlement label 
    *includeUnentitled(bool) - also show orgs without this specific entitlement
                              This can only be specified with 'ent_label' and will
                              be ignored otherwise
    """
    try:
        if ent_label is not None:
            return rhn.session.org.listEntitlements(rhn.key, ent_label, includeUnentitled)
        else:
            return rhn.session.org.listEntitlements(rhn.key)
    except Exception, E:
        if ent_label is not None:
            return rhn.fail(E, 'List usage of entitlement %s across all orgs' % ent_label)
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
        return rhn.fail(E, 'List software entitlements for org %d (%s)' % (orgid, getDetails(orgid)['name']))

def ListSystemEntitlements(rhn, label = None, includeUnentitled = False):        
    """
    usage: ListSystemEntitlements(rhn, label, includeUnentitled)

    list allocation of either all system entitlements across orgs, or a
    specified system entitlement

    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    *label(str)              - software channel/entitlement label 
    *includeUnentitled(bool) - also show orgs without this specific entitlement
                               This can only be specified with 'ent_label' and will
                               be ignored otherwise
    """
    try:
        if label is not None:
            return rhn.session.org.ListSystemEntitlements(rhn.key, label, includeUnentitled)
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
        return rhn.fail(E, 'list system entitlement usage for org %d (%s)' %(orgid, getDetails(orgid)['name']) )

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
        return rhn.fail(E, 'list users in org %d (%s)' %(orgid, getDetails(orgid)['name']))

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
        return rhn.fail(E, 'allocate %d entitlements for %s to org %d (%s)' %(allocation, label,
                                                                orgid, getDetails(orgid)['name']))

    
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
        return rhn.fail(E, 'allocate %d entitlements for %s to org %d (%s)' %(allocation, label,
                                                                orgid, getDetails(orgid)['name']))

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
        return rhn.fail(E, 'allocate %d entitlements for %s to org %d (%s)' %(allocation, label,
                                                                orgid, getDetails(orgid)['name']))

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
        return rhn.fail(E, 'change name for organization %d (%s)' %(orgid, getDetails(orgid)['name']))
    
## ---- org.trusts ----------------------------------------------------- ##    

def addTrust(rhn, orgid, trustedorgid):
    """
    usage: addTrust(rhn, orgid, trustedorgid)
    
    adds a new organizational trust to the specified org.

    returns: True, or throws Exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - Organization ID
    trustedorgid(int)        - Org ID you wish to trust
    """
    try:
        return rhn.session.org.trusts.addTrust(rhn.key, orgid, trustedorgid) == 1
    except Exception, E:
        return rhn.fail(E, 'add a new trust for org %d to org %d' %(trustedorgid, orgid))

        
def getTrustDetails(rhn, orgid):
    """
    usage: getTrustDetails(rhn, orgid)
    abstraction of org.trusts.getDetails (to avoid name clashes)

    display the details for a given trusted org 
    from the perspective of the user's org.

    returns: dict:

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - organization ID                     
    """
    try:
        return rhn.session.org.trusts.getDetails(rhn.key, orgid)
    except Exception, E:
        return rhn.fail(E, 'get details about trusted org %d' % orgid)
        
def listChannelsConsumed(rhn, orgid):
    """
    usage: listChannelsConsumed(rhn, orgid)

    Lists all software channels that the organization given may consume from
    the user's organization.

    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - organization ID                     
    """
    try:
        return rhn.session.org.trusts.listChannelsConsumed(rhn.key, orgid)
    except Exception, E:
        return rhn.fail(E, 'list channels consumed by org %d' % orgid )

def listChannelsProvided(rhn, orgid):
    """
    usage: listChannelsProvided(rhn, orgid)

    Lists all software channels that the organization given is providing
    to the user's organization.

    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - organization ID                     
    """
    try:
        return rhn.session.org.trusts.listChannelsProvided(rhn.key, orgid)
    except Exception, E:
        return rhn.fail(E, 'list channels provided to your org by org %d' % orgid)

def listTrustedOrgs(rhn):
    """
    usage: listTrustedOrgs(rhn)

    List all organanizations trusted by the user's organization. 


    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.org.trusts.listOrgs(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list orgs trusted by your organization')

def listSystemsAffected(rhn, orgid, trustedorgid):        
    """
    usage: listSystemsAffected(rhn, orgid, trustedorgid)

    Get a list of systems within the trusted organization that would be affected
    if the trust relationship was removed.
    This basically lists systems that are sharing at least (1) package. 

    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - your organization ID                     
    trustedorgid(int)        - trusted organization ID                     
    """
    try:
        return rhn.session.org.trusts.listSystemsAffected(rhn.key, orgid, trustedorgid)
    except Exception, E:
        return rhn.fail(E, 'list systems affected by removing the trust between orgs %d and %d' %(orgid, trustedorgid))


def listTrusts(rhn, orgid):
    """
    usage: listTrusts(rhn, orgid)

    Returns the list of organizations trusted by the given org id

    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - organization ID                     
    """
    try:
        return rhn.session.org.trusts.listTrusts(rhn.key, orgid)
    except Exception, E:
        return rhn.fail(E, 'list orgs trusted by org id %d' % orgid)

def removeTrust(rhn, orgid, trustedorgid):
    """
    usage: removeTrust(rhn, orgid, trustedorgid)

    removes an organization trust from the given org.


    returns: True, or throws exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    orgid(int)               - your organization ID                     
    trustedorgid(int)        - trusted organization ID                     
    """
    try:
        return rhn.session.org.trusts.removeTrust(rhn.key, orgid, trustedorgid) == 1
    except Exception, E:
        return rhn.fail(E, 'remove the trust between org %d and %d' %(orgid, trustedorgid))
