#!/usr/bin/env python
# -*- coding: utf-8 -*-
__doc__ = """
RHN API channel module, updated for satellite 5.4
This contains methods from the following API namespaces:

channel
channel.access
channel.software
channel.org

These were merged because it made sense to me and because the channel API namespace
has but a few methods.

Methods in this file almost invariably require an current rhnSession object
from the top-level rhnapi module
"""
import time
import re
from operator import itemgetter

# possible architectures according to the RHN satellite channel creation page:
# the mapping allows me to use the shorter names
# --------------------------------------------------------------------------------- #
arch_labels = { 'ia32' : 'channel-ia32',
                'ia64': 'channel-ia64',
                'ppc' : 'channel-ppc',
                'sparc' : 'channel-sparc',
                'sparc-solaris': 'channel-sparc-sun-solaris',
                'i386-solaris' : 'channel-i386-sun-solaris',
                'iSeries' : 'channel-iseries',
                'pSeries' : 'channel-pSeries',
                'x86_64' : 'channel-x86_64',
                's390' : 'channel-s390',
                's390x' : 'channel-s390x',
                }
# The channel namespace
#    * listAllChannels
#    * listMyChannels
#    * listPopularChannels
#    * listRedHatChannels
#    * listRetiredChannels
#    * listSharedChannels
#    * listSoftwareChannels

# --------------------------------------------------------------------------------- #
def listSoftwareChannels(rhn):
    """
    usage: listSoftwareChannels(rhn)

    Lists all visible software channels

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.channel.listSoftwareChannels(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list visible software channels')

# --------------------------------------------------------------------------------- #
def listAllChannels(rhn):
    """
    usage: listAllChannels(rhn)

    Lists all visible software channels

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.channel.listAllChannels(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list software channels')

# --------------------------------------------------------------------------------- #
def listMyChannels(rhn):
    """
    usage: listMyChannels(rhn)

    Lists all visible software channels

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.channel.listMyChannels(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list software channels')

# --------------------------------------------------------------------------------- #
def listPopularChannels(rhn, popcount):
    """
    usage: listPopularChannels(rhn)

    Lists all visible software channels that have at least popcount systems using them

    parameters:
    rhn                     - an authenticated RHN session.
    popcount(int)             - minimum number of systems subscribed
    """
    try:
        return rhn.session.channel.listPopularChannels(rhn.key, popcount)
    except Exception, E:
        return rhn.fail(E,'list visible software channels with at least %d systems subscribed' % popcount)

# --------------------------------------------------------------------------------- #
def listRedHatChannels(rhn):
    """
    usage: listRedHatChannels(rhn)

    Lists all visible Red Hatsoftware channels

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.channel.listRedHatChannels(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list visible Red Hat software channels')

# --------------------------------------------------------------------------------- #
def listRetiredChannels(rhn):
    """
    usage: listRetiredChannels(rhn)

    Lists all retired software channels

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.channel.listRetiredChannels(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list retired software channels')

# --------------------------------------------------------------------------------- #
def listSharedChannels(rhn):
    """
    usage: listSharedChannels(rhn)

    Lists all software channels which may be shared by the logged-in user's organization.

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.channel.listSharedChannels(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list shared software channels')

# from channel.access        
#    * disableUserRestrictions
#    * enableUserRestrictions
#    * getOrgSharing
#    * setOrgSharing

# --------------------------------------------------------------------------------- #
def disableUserRestrictions(rhn, chanlabel):
    """
    usage: disableUserRestrictions(rhn, chanlabel)

    Disable user restrictions for the given channel.
    If disabled, all users within the organization may subscribe to the channel.

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    """
    try:
        return rhn.session.channel.access.disableUserRestrictions(rhn.key, chanlabel) == 1
    except Exception, E:
        return rhn.fail(E,'disable user access restrictions for channel %s' % chanlabel)

# --------------------------------------------------------------------------------- #
def enableUserRestrictions(rhn, chanlabel):
    """
    usage: enableUserRestrictions(rhn, chanlabel)

    Enable user restrictions for the given channel.
    If enabled, only selected users within the organization may subscribe to the channel. 

    returns:
    True, False or exception

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    """
    try:
        return rhn.session.channel.access.enableUserRestrictions(rhn.key, chanlabel) ==1
    except Exception, E:
        return rhn.fail(E,'enable user access restrictions for channel %s' % chanlabel)
        
# --------------------------------------------------------------------------------- #
def getOrgSharing(rhn, chanlabel):
    """
    usage: getOrgSharing(rhn, chanlabel)

    Get organization sharing access control.

    returns: str ('public', 'private', or 'protected')

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    """
    try:
        return rhn.session.channel.access.getOrgSharing(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E,'get Org sharing info for channel %s' % chanlabel)

# --------------------------------------------------------------------------------- #
def setOrgSharing(rhn, chanlabel, access):
    """
    usage: setOrgSharing(rhn, chanlabel)

    Set organization sharing access control. 

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    access(str)             - access setting ('public', 'private', or 'protected')
    """
    try:
        return rhn.session.channel.access.setOrgSharing(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E,'set Org sharing info for channel %s' % chanlabel)

# from channel.org
#    * disableAccess
#    * enableAccess
#    * list

# --------------------------------------------------------------------------------- #
def disableAccess(rhn, chanlabel, orgId):
    """
    usage: disableAccess(rhn, chanlabel, orgId)

    disable access to the channel for the given organization.

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    orgId(int)              - org id being removed access
    """
    try:
        return rhn.session.channel.org.disableAccess(rhn.key, chanlabel, orgId) == 1
    except Exception, E:
        return rhn.fail(E,'disable access to channel %s for org %d' % (chanlabel, orgId))

# --------------------------------------------------------------------------------- #
def enableAccess(rhn, chanlabel, orgId):
    """
    usage: enableAccess(rhn, chanlabel, orgId)

    enable access to the channel for the given organization.

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    orgId(int)              - org id being granted access
    """
    try:
        return rhn.session.channel.org.enableAccess(rhn.key, chanlabel, orgId) == 1
    except Exception, E:
        return rhn.fail(E,'grant access to channel %s for org %d' % (chanlabel, orgId))

# --------------------------------------------------------------------------------- #
def listOrgs(rhn, chanlabel):
    """
    usage: listOrgs(rhn, chanlabel)

    List the organizations associated with the given channel that may be trusted

    returns: list(dict)

    params:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    """
    try:
        return rhn.session.channel.org.list(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E,'list orgs for channel %s' % chanlabel)

# from channel.software:
#    * addPackages
#    * availableEntitlements
#    * clone
#    * create
#    * delete
#    * getChannelLastBuildById
#    * getDetails
#    * getDetails
#    * isGloballySubscribable
#    * isUserSubscribable
#    * listAllPackages
#    * listAllPackagesByDate
#    * listArches
#    * listChildren
#    * listErrata
#    * listErrataByType
#    * listLatestPackages
#    * listPackagesWithoutChannel
#    * listSubscribedSystems
#    * listSystemChannels
#    * mergeErrata
#    * mergePackages
#    * regenerateNeededCache
#    * regenerateYumCache
#    * removePackages
#    * setContactDetails
#    * setGloballySubscribable
#    * setSystemChannels
#    * setUserSubscribable
#    * subscribeSystem

# --------------------------------------------------------------------------------- #
def create(rhn, label, name, summary, arch, parent='', checksum=None, gpgkey=None):
    """
    API: channel.software.create

    usage: create(rhn, label, name, summary, arch, parent='', checksum)
    
    description:
    Creates a new software channel with the supplied information.

    returns: bool, or throws exception.

    parameters:
    rhn                     - an authenticated RHN session.
    label (str)             - the new channel label. lowercase, no spaces.
    name (str)              - Human-readable channel name.
    summary (str)           - summary of channel
    arch (str)              - channel architecture [ IA-32, IA-64, PPC, Sparc, Sparc Solaris,
                              i386 Solaris, iSeries, pSeries, s390, s390x, x86_64]
    *parent (str)           - the parent channel label. leave blank to create a new base channel.
    *checksum(str)          - 'sha1' or 'sha256'
    *gpgkey(dict)           - gpg key information { 'url' : str, 'id' : str, 'fingerprint' : str }

    If gpgkey is provided, checksum is also required. Sorry, but that's just how it is.
    """
    try:
        if gpgkey is not None and checksum is not None:
            return rhn.session.channel.software.create(rhn.key, label, name, summary,
                                                  arch, parent, checksum, gpgkey) == 1
        elif checksum is not None:
            return rhn.session.channel.software.create(rhn.key, label, name, summary,
                                                          arch, parent, checksum) == 1
        else:
            return rhn.session.channel.software.create(rhn.key, label, name, summary,
                                                                        arch, parent) == 1
    except Exception, E:
        return rhn.fail(E, 'create software channel %s' % name)


def createChannel(rhn, label, name, summary, arch, **kwargs):
    """
    API: channel.software.create

    usage: create(rhn, label, name, summary, arch, **kwargs)
    where kwargs is a sequence of key=value entries. See the 'parameters' section below
    
    description:
    Creates a new software channel with the supplied information.

    returns: bool, or throws exception.

    parameters:
    rhn                     - an authenticated RHN session.
    label (str)             - the new channel label. lowercase, no spaces.
    name (str)              - Human-readable channel name.
    summary (str)           - summary of channel
    arch (str)              - channel architecture [ IA-32, IA-64, PPC, Sparc, Sparc Solaris,
                              i386 Solaris, iSeries, pSeries, s390, s390x, x86_64]
    *parent (str)           - the parent channel label. leave blank to create a new base channel.
    *checksum(str)          - 'sha1' or 'sha256'
    *gpgkey(dict)           - gpg key information { 'url' : str, 'id' : str, 'fingerprint' : str }

    If gpgkey is provided, checksum is also required. Sorry, but that's just how it is.
    """
    try:
        return rhn.session.channel.software.create(rhn.key, label, name, summary, arch, **kwargs) == 1
    except Exception, E:
        return rhn.fail(E, 'create software channel %s' % name)
# --------------------------------------------------------------------------------- #
def clone(rhn, source_channel, name, label, summary, parent_label=None, arch_label=None,
          gpg_url=None, gpg_id=None, gpg_fingerprint=None, description=None, no_errata=False):
    """
    usage: clone(rhn,source_channel,name,label,summary, **optional args)

    Clones an existing channel

    returns: bool, or throws exception
    
    For optional args, give the variable name as well to avoid specifying all of them.
    cloneChannel(rhn,source_channel,name,label,summary, parent_label='rhel-i386-server-5')

    parameters (those marked * are optional):
    rhn                     - an authenticated RHN session.
    source_channel(str)     - the channel to clone
    name (str)              - the new channel name
    label(str)              - the new channel label.
    summary(str)            - the new channel summary
    no_errata(bool)         - do (not) clone errata!. Default False - channels are cloned with all applicable errata
    *parent_label(str)      - the new channel parent. If omitted, the clone is a base channel.
    *arch_label(str)        - the new channel arch. Keeps the original if omitted
    *gpg_url(str)           - URL for the clone gpg (public) key
    *gpg_id(str)            - GPG-id
    *gpg_fingerprint(str)   - GPG fingerprint
    *description(str)       - cloned channel description
    """
    clone_details =     {
                    'name' : name, 'label' : label, 'summary' : summary, 'parent_label' : parent_label ,
                    'arch_label' : arch_label, 'gpg_url' : gpg_url, 'gpg_id' : gpg_id,
                     'gpg_fingerprint' : gpg_fingerprint, 'description' : description,
                     }
    for k in clone_details.keys():
        if clone_details[k] is None:
            del clone_details[k]
    try:
        # well, it returns an integer if the channel cloned successfully, so let's test that
        return isinstance(rhn.session.channel.software.clone(rhn.key, source_channel, clone_details, no_errata), int)
    except Exception, E:
        return rhn.fail(E, 'clone channel label %s as %s ' % (source_channel, clone_details['label'] ) )

# --------------------------------------------------------------------------------- #
def cloneChannel(rhn, chanlabel, noerrata = False, **kwargs):
    """
    API: channel.software.clone

    usage: cloneChannel(rhn, chanlabel, noerrata, **kwargs)
        where **kwargs is a list of name=value pairs.
        see parametes below for valid args

    minimal example: cloneChannel(rhn, chanlable, noerrata, name=NAME, label=LABEL, summary=SUMMARY)

    description:
    Attempted simplification of the clonechannel, using kwargs (which are parsed into a dict anyway)
    providing broken args will cause exceptions to be thrown!

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel to clone

    plus the following keyword parameters (* indicates an optional parameter)
    name (str)              - the new channel name
    label(str)              - the new channel label.
    summary(str)            - the new channel summary
    no_errata(bool)         - do (not) clone errata!. Default False - channels are cloned with all applicable errata
    *parent_label(str)      - the new channel parent. If omitted, the clone is a base channel.
    *arch_label(str)        - the new channel arch. Keeps the original if omitted
    *gpg_url(str)           - URL for the clone gpg (public) key
    *gpg_id(str)            - GPG-id
    *gpg_fingerprint(str)   - GPG fingerprint
    *description(str)       - cloned channel description
    """
    try:
        res = rhn.session.channel.software.clone(rhn.key, chanlabel, kwargs, noerrata)
        return isinstance(res, int)
    except Exception, E:
        return rhn.fail(E, "clone channel %s as %s" %(chanlabel, kwargs['label']))

# --------------------------------------------------------------------------------- #
def deleteChannel(rhn, channel_label):
    """
    wrapper for backwards compat
    """
    return delete(rhn, channel_label)

# --------------------------------------------------------------------------------- #
def delete(rhn, channel_label):
    """
    usage: deleteChannel(rhn, channel_label)

    Deletes a channel using its label as a key
    
    returns: Boolean or Exception

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label (str)     - the channel to delete.
    """
    try:
        return rhn.session.channel.software.delete(rhn.key, channel_label) == 1
    except Exception, E:
        return rhn.fail(E, 'delete channel %s ' % channel_label )
    
# --------------------------------------------------------------------------------- #
def detailsByLabel(rhn, channel_label):
    """
    usage: detailsByLabel(rhn, channel_label)

    Retrieves channel information for a given channel label

    returns: dict

    Parameters:
    rhn                     - an authenticated RHN session.
    channel_label (str)     - the channel label
    """
    
    try:
        return rhn.session.channel.software.getDetails(rhn.key, channel_label)
    except Exception, E:
        return rhn.fail(E, 'retrieve details for channel %s ' % channel_label)

# --------------------------------------------------------------------------------- #
def detailsByID(rhn, channel_id):
    """
    usage: detailsByID(rhn, channel_id)

    Retrieves channel information for a given channel ID number

    returns: dict
    
    parameters:
    rhn                     - an authenticated RHN session.
    channel_id (int)        - the channel id
    """
    try:
        return rhn.session.channel.software.getDetails(rhn.key, channel_id)
    except Exception, E:
        return rhn.fail(E, 'retrieve details for channel %s ' % channel_id)

# --------------------------------------------------------------------------------- #
def addPackages(rhn, channel_label, packagelist):
    """
    usage: addPackages(rhn, channel_label, packagelist)
    
    Add packages to a channel using their package IDs
    
    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    packagelist(list/int)   - list of package IDs (ints)
    """
    try:
        rhn.session.channel.software.addPackages(rhn.key, channel_label, packagelist)
    except Exception, E:
        return rhn.fail(E, 'add packages to %s' % (channel_label))

# --------------------------------------------------------------------------------- #
def availableEntitlements(rhn, channel_label):
    """
    usage: getEntitlements(rhn, channel_label)
    
    Reports the number of available entitlements for the given channel
    
    returns:
    available entitlement count (init)
    
    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label

    """
    try:
        return rhn.session.channel.software.availableEntitlements(rhn.key, channel_label)
    except Exception, E:
        return rhn.fail(E, 'get number of available entitlements for channel %s' % channel_label)

# --------------------------------------------------------------------------------- #
def isGloballySubscribable(rhn, channel_label):
    """
    usage: isGloballySubscribable(rhn, channel_label)

    Checks if a channel is globally subscribable (by all users).

    returns: True for yes, False for no, or an Exception.

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    """
    try:
        return rhn.session.channel.software.isGloballySubscribable(rhn.key, channel_label) == 1
    except Exception, E:
        return rhn.fail(E, 'get subscribability details for %s' % channel_label)

# --------------------------------------------------------------------------------- #
def setGloballySubscribable(rhn, channel_label):
    """
    usage: setGloballySubscribable(rhn, channel_label)

    Set a channel to be globally subscribable (by all users)

    returns:  True if successful. Exception otherwise
    
    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    """
    try:
        return  rhn.session.channel.software.setGloballySubscribable(rhn.key, channel_label) == 1
    except Exception, E:
        return rhn.fail(E, 'set channel %s globally subscribable ' % channel_label)

# --------------------------------------------------------------------------------- #
def isUserSubscribable(rhn, channel_label, user_login):
    """
    usage: isUserSubscribable(rhn, channel_label, user_login)
    
    Checks if a channel is subscribable by a specific user.
    
    returns: True for yes, False for no, Exception.
    
    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    user_login(str)         - the user to check.
    """
    try:
        return  rhn.session.channel.software.isUserSubscribable(rhn.key, channel_label, user_login) == 1
    except Exception, E:
        return rhn.fail(E, 'check if user %s can subscribe machines to channel %s' % ( user_login, channel_label) )

# --------------------------------------------------------------------------------- #
def setUserSubscribable(rhn, channel_label, user_login):
    """
    usage: setUserSubscribable(rhn, channel_label, user_login)

    Set a channel to be subscribable by a specific user.
    
    returns: True for yes, False for no, Exception.

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    user_login(str)         - the user to check.
    """
    try:
        return rhn.session.channel.software.setUserSubscribable(rhn.key, channel_label, user_login) == 1
    except Exception, E:
        return rhn.fail(E, 'set channel %s subscribable by user %s' % ( channel_label, user_login) )

# --------------------------------------------------------------------------------- #
def listAllPackages(rhn, channel_label, start_date=None, end_date=None):
    """
    usage: listPackages(rhn, channel_label, start_date='', end_date='')
    
    Lists all packages in a channel, regardless of modification date/time.
    packages may be listed multiple times - each erratum/version has a different ID

    returns: a list of dicts (hashes), one per package  [ {..}, {..} ]
    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    *start_date(str)        - start date. Optional.
    *end_date(str)          - end date. Optional. If no start_date, end_date is ignored.

    Date formats are string representations of iso8601:
    format is '%Y-%m-%d %H:%M:%S' e.g. '2009-01-23 14:05:43'
    """
    try:
        if start_date is None:
            return rhn.session.channel.software.listAllPackages(rhn.key, channel_label)
        elif end_date is None:
            return rhn.session.channel.software.listAllPackages(rhn.key, channel_label, start_date)
        else:
            return rhn.session.channel.software.listAllPackages(rhn.key, channel_label, start_date, end_date)
    except Exception, E:
        return rhn.fail(E, 'list packages in channel %s' % ( channel_label ) )

# --------------------------------------------------------------------------------- #
def listArches(rhn):
    """
    usage: listArches(rhn)

    Lists the possible channel architectures
    
    returns: list of dicts, one per architecture. [ {...},...]

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.channel.software.listAllPackages(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list possible channel architectures' )

# --------------------------------------------------------------------------------- #
def listChildren(rhn, channel_label):
    """
    List the children of a given channel

    returns: list of dict

    params:
    rhn                - an authenticated RHN session
    channel_label(str) - label of base channel
    """
    try:
        return rhn.session.channel.software.listChildren(rhn.key, channel_label)
    except Exception, E:
        return rhn.fail(E, 'list children of base channel %s' % channel_label)

# --------------------------------------------------------------------------------- #
def listErrata(rhn, channel_label, start_date=None, end_date=None):
    """
    usage: listErrata(rhn, channel_label, start_date='', end_date='')

    Lists the errata in a given channel. Can take date arguments as detail below
    
    parameters (* means optional):
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    *start_date(str)        - start date. Optional.
    *end_date(str)          - end date. Optional. If no start_date, end_date is ignored.

    Date formats are string representations of iso8601:
    format is '%Y-%m-%d %H:%M:%S' e.g. '2009-01-23 14:05:43'
    """
    try:
        if start_date is None:
            return rhn.session.channel.software.listErrata(rhn.key, channel_label)
        elif end_date is None:
            return rhn.session.channel.software.listErrata(rhn.key, channel_label, start_date)
        else:
            return rhn.session.channel.software.listErrata(rhn.key, channel_label, start_date, end_date)
    except Exception, E:
        return rhn.fail(E, 'list errata in channel %s' % ( channel_label ) )

# --------------------------------------------------------------------------------- #
def listErrataByType(rhn, channel_label, advisoryType):
    """
    List the errata of a specific type that are applicable to a channel 

    returns: list of dict

    Parameters:

    rhn                -  authenticated RHN session
    channel_label(str) - channel to query 
    advisoryType(str)  - type of advisory ['Security Advisory',
                                           'Product Enhancement Advisory',
                                           'Bug Fix Advisory'] 
    """
    try:
        return rhn.session.channel.software.listErrataByType(rhn.key, channel_label, advisoryType)
    except Exception, E:
        return rhn.fail(E, 'fetch %s errata for channel %s' %( advisoryType, channel_label ) )
# --------------------------------------------------------------------------------- #
def listLatestPackages(rhn,channel_label):
    """
    usage: listLatestPackages(rhn,channel_label)

    Lists the latest packages (highest version/release/epoch) in a given channel
    
    returns: list of dicts, one per package.
    
    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    """
    try:
        return rhn.session.channel.software.listLatestPackages(rhn.key, channel_label)
    except Exception, E:
        return rhn.fail(E, 'list latest packages in channel %s' % ( channel_label ) )
# --------------------------------------------------------------------------------- #
def listPackagesWithoutChannel(rhn):
    """
    usage: listPackagesWithoutChannel(rhn)

    Lists all packages that are not in a channel. Typically custom packages.

    returns: list of dicts

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.channel.software.listPackagesWithoutChannel(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list packages that are not in a  channel' )

# --------------------------------------------------------------------------------- #
def listSubscribedSystems(rhn, channel_label):
    """
    usage: listSubscribedSystems(rhn, channel_label)

    Lists the systems that are subscribed to a given channel
    
    returns: list of dicts - one per system

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    """
    try:
        return rhn.session.channel.software.listSubscribedSystems(rhn.key, channel_label)
    except Exception, E:
        return rhn.fail(E, 'list systems subscribed to channel %s' % ( channel_label ) )

# --------------------------------------------------------------------------------- #
def listSystemChannels(rhn, system_id):
    """
    usage: listSystemChannels(rhn, system_id)

    Lists the channels a given system is subscribed to.
    
    returns: list of dicts, one per channel.
    
    parameters:
    rhn                     - an authenticated RHN session.
    system_id(int)          - system ID
    """
    try:
        return rhn.session.channel.software.listSystemChannels(rhn.key, system_id)
    except Exception, E:
        return rhn.fail(E, 'list channels for system ID %d' % ( system_id ) )

# --------------------------------------------------------------------------------- #
def setSystemChannels(rhn, system_id, channel_list):
    """
    usage: setSystemChannels(rhn, system_id, channel_list)

    Sets the channels a given system is subscribed to.
    
    parameters:
    rhn                     - an authenticated RHN session.
    system_id(int)          - system ID
    """
    try:
        rhn.session.channel.software.setSystemChannels(rhn.key, system_id)
    except Exception, E:
        return rhn.fail(E, 'subscribing system ID %d to channels %s' % ( system_id, ','.join(channel_list) ) )

# --------------------------------------------------------------------------------- #
def mergeErrata(rhn, src_label, tgt_label, start_date=None, end_date=None):
    """
    Merges all errata from one channel to another, optionally between 2 dates

    returns: list of dict (representing errata structures)

    parameters (* means optional):
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    *start_date(str)        - start date. Optional (if omitted, defaults to 1980-01-01 00:00:00
    *end_date(str)          - end date. Optional. (if omitted, the current date and time are used)

    Date formats are string representations of iso8601:
    format is '%Y-%m-%d %H:%M:%S' e.g. '2009-01-23 14:05:43'
    """
    # cope with no dates being given
    if end_date is None:
        # well, set the end date to *now*
        end_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if start_data is None:
        # the beginning of 1980 is more than old enough. That's pre-Linux
        start_date = time.strftime('%Y-%m-%d %H:%M:%S', (1980, 1, 1, 0, 0, 0, 0, 0, 0))
    try:
        return rhn.session.channel.software.mergeErrata(rhn.key, src_label, tgt_label, start_date, end_date)
    except Exception, E:
        return rhn.fail(E, 'merge errata from channel %s to channel %s' % (src_label, tgt_label) )

# --------------------------------------------------------------------------------- #
def mergePackages(rhn, source_channel, target_channel):
    """
    usage: mergePackages(rhn, source_channel, target_channel)

    Merges packages from one channel into another

    returns: list of dict (package structures)
    
    parameters:
    rhn                     - an authenticated RHN session.
    source_channel(str)     - channel label to merge from
    target_channel(str)     - channel label to merge into
    """
    try:
        return rhn.session.channel.software.mergePackages(rhn.key, source_channel, target_channel)
    except Exception, E:
        return rhn.fail(E, 'merge packages from channel %s to channel %s ' % ( source_channel, target_channel ) )

# --------------------------------------------------------------------------------- #
def regenerateNeededCache(rhn, channel_label=None):
    """
    usage: regenerateNeededCache(rhn, channel_label)

    returns: Boolean or exception.

    Completely clear and regenerate the needed Errata and Package cache for all
    systems subscribed to the specified channel.
    This should be used only if you believe your cache is incorrect for all the systems in a given channel.

    parameters:
    rhn(rhnapi.rhnSession) - authenticated session
    *channel_label(str)     - label of target channel.

    If run without channel_label, will regenerate all cache for all channels.
    This requires Satellite Administrator privileges.
    """
    try:
        if channel_label is not None:
            return rhn.session.channel.software.regenerateNeededCache(rhn.key, channel_label) == 1
        else:
            return rhn.session.channel.software.regenerateNeededCache(rhn.key) == 1
            
    except Exception, E:
        return rhn.fail(E, 'Regenerate Errata and Package Cache for channel %s' % channel_label)

# --------------------------------------------------------------------------------- #
def regenerateYumCache(rhn, channel_label):
    """
    usage: regenerateYumCache(rhn, channel_label)

    Regenerates the yum cache for the specified channel

    parameters:
    rhn(rhnapi.rhnSession) - authenticated session
    *channel_label(str)     - label of target channel.
    """
    try:
        return rhn.session.channel.software.regenerateYumCache(rhn.key, channel_label) == 1
    except Exception, E:
        return rhn.fail(E, 'regenerate Yum cache for channel %s' % channel_label)

# --------------------------------------------------------------------------------- #
def removePackages(rhn, channel_label, package_ids):
    """
    usage: removePackages(rhn, channel_label, package_ids)

    Removes a list of packages from a channel
    
    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    package_ids(list)       - list of package IDs (ints) to remove
    """
    try:
        return rhn.session.channel.software.removePackages(rhn.key, channel_label, packagelist) == 1
    except Exception, E:
        return rhn.fail(E, 'remove  package IDs %s from channel %s' % ( channel_label, ','.join(packagelist)) )

# --------------------------------------------------------------------------------- #
def setContactDetails(rhn, channel_label, name, email, phone, policy):
    """
    Sets the administrative contact/support information for a channel

    parameters:
    rhn(rhnapi.rhnSession)  - authenticated RHN session object
    channel_label(str)      - channel label
    name(str)               - channel maintainer's name
    email(str)              - channel maintainer's email
    phone(str)              - channel maintainer's phone number
    policy(str)             - channel support policy
    """
    try:
        return rhn.session.channel.software.setContactDetails(rhn.key, channel_label,
                                                          name, email, phone, policy) == 1
    except Exception, E:
        return rhn.fail(E, 'set contact details for channel %s' % channel_label)
# --------------------------------------------------------------------------------- #
def listChildChannels(rhn, channel_label):
    """
    usage: listChildChannels(rhn, channel_label)

    Lists the available child channels for a given parent
    
    returns: list of channel labels

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    """
    try:
        return sorted([ x['label'] for x in rhn.session.channel.software.listChildren(rhn.key, channel_label)])
    except Exception, E:
        rhn.fail(E, 'list children of channel %s' % ( channel_label ) )
    
def listBaseChannels(rhn, regex=None):
    """
    API: None, custom method

    usage: listBaseChannels(rhn)

    List the base channels on your satellite
    
    returns: list of channel labels

    parameters:
    rhn                     - an authenticated RHN session.
    regex(str)              - optional regular expression to match against labels
    """
    try:
        allchannels = sorted(rhn.session.channel.listSoftwareChannels(rhn.key), key=itemgetter('label'))
        basechannels = [ x['label'] for x in allchannels if x['parent_label'] == '' ]
        if regex is not None:
            pattern = re.compile(r'%s' % str(regex))
            return [ x for x in basechannels if pattern.search(x) ]
        else:
            return basechannels
    except Exception, E:
        rhn.fail(E, 'list base channels on your satellite')
    
def channelsByArch(rhn, arch):
    """
    rhn - an authenticated RHN session
    arch(str) - the channel architecture to list.
    """
    try:
        chanlist = rhn.session.channel.listSoftwareChannels(rhn.key)
        return [ x['label'] for x in chanlist if x['arch'] == arch ]
    except Exception, E:
        rhn.fail(E, "find channels with arch %s" % (arch))

# --------------------------------------------------------------------------------- #
# Methods under here are not technically part of the API, just utility functions I added
# to simplify scripting of channel deletion...

def hasChildren(rhn, channel_label):
    """
    CUSTOM METHOD

    usage: hasChildren(rhn, channel_label)

    returns: True if the given base channel label has child channels,
             False otherwise
    params:
    rhn                - authentication rhnapi.rhnSession
    channel_label(str) - the channel label to check
    """
    try:
        return len(rhn.session.channel.software.listChildren(rhn.key, channel_label)) != 0
    except Exception, E:
        rhn.fail(E, 'check for children of channel %s' % channel_label)

def deleteRecursive(rhn, channel_label):
    """
    CUSTOM METHOD
    deletes all children of a given custom channel, then the channel itself.
    This could cause utter mayhem, be careful.

    usage: deleteRecursive(rhn, channel_label)

    returns: True if successful,
             False otherwise
             or throws exception
    params:
    rhn                 - authenticated rhnapi.rhnSession 
    channel_label(str)  - label of parent channel
    """
    # I could call my other utility methods in here, but for portability, 
    # I'm using the API directly
    try:
        if hasChildren(rhn, channel_label):
            for child in rhn.session.channel.software.listChildren(rhn.key, channel_label):
                rhn.session.channel.software.delete(rhn.key, child['label'])
        # handily, this will fail if any of the child channels could not be deleted:
        return rhn.session.channel.software.delete(rhn.key, channel_label) == 1
    except Exception, E:
        rhn.fail(E, 'recursively delete channel %s and all its child channels' % channel_label)

def cloneRecursive(rhn, channel_label, prefix=None, suffix=None):
    """
    CUSTOM METHOD
    A placeholder for a custom method to recursively clone channels,
    adding either a prefix or suffix (or both) to their existing labels
    Mostly I envision this being a date (for example) or something like 'prod' or 'test'

    usage: cloneRecursive(rhn, parent_label, target_label, prefix=None, suffix=None)

    params: ( * = optional )
    rhn               - 
    parent_label(str) - 
    *prefix(str)      - 
    *suffix(str)      - 

    You really MUST provide one of prefix or suffix, as otherwise the cloning will fail,
    because source and target labels will be identical.
    """
    return 'Not Implemented Yet'


        
