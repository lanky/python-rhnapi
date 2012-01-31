#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the 'channel' namespaces (see __doc__ below)
#
# Copyright 2009-2012 Stuart Sears
#
# This file is part of python-rhnapi
#
# python-rhnapi is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
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

__author__ = "Stuart Sears"

# Additional stdlib modules
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
    API:
    channel.listSoftwareChannels

    usage:
    listSoftwareChannels(rhn)
    
    description:
    Lists all visible software channels

    returs:

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
    API:
    channel.listAllChannels

    usage:
    listAllChannels(rhn)
    
    description:
    Lists all visible software channels

    returns:
    list/dict

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
    API:
    channel.listMyChannels

    usage:
    listMyChannels(rhn)
    
    description:
    Lists all visible software channels

    returns:
    list/dict

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
    API:
    channel.listPopularChannels

    usage:
    listPopularChannels(rhn)
    
    description:
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
    API:
    channel.listRedHatChannels

    usage:
    listRedHatChannels(rhn)

    description:
    Lists all visible Red Hat software channels

    returns:
    list of dict

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
    API:
    channel.listRetiredChannels

    usage:
    listRetiredChannels(rhn)

    description:
    Lists all retired software channels

    returns:
    list/dict

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
    API:
    channel.listSharedChannels

    usage:
    listSharedChannels(rhn)

    description:
    Lists all software channels which may be shared by the logged-in user's organization.

    returns:
    list of dict

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
    API:
    channel.access.disableUserRestrictions

    usage:
    disableUserRestrictions(rhn, chanlabel)

    description:
    Disable user restrictions for the given channel.
    If disabled, all users within the organization may subscribe to the channel.

    returns:
    Bool, or throws Exception

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
    API:
    channel.access.enableUserRestrictions

    usage:
    enableUserRestrictions(rhn, chanlabel)
    
    description:
    Enable user restrictions for the given channel.
    If enabled, only selected users within the organization may subscribe to the channel. 

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    """
    try:
        return rhn.session.channel.access.enableUserRestrictions(rhn.key, chanlabel) ==1
    except Exception, E:
        return rhn.fail(E,'enable user access restrictions for channel %s' % chanlabel)
        
# ---------------------------------------------------------------------------- #

def getDetails(rhn, chanspec):
    """
    API:
    channel.software.getDetails

    calls detailsByLabel or detailsByID depending on information passed
    """
    if isinstance(chanspec, int):
        return detailsByID(rhn, chanspec)
    elif isinstance(chanspec, str):
        return detailsByLabel(rhn, chanspec)
    else:
        return rhn.fail(E, 'get details for channel %s' % str(chanspec))

# --------------------------------------------------------------------------------- #

def getOrgSharing(rhn, chanlabel):
    """
    API:
    channel.access.getOrgSharing

    usage:
    getOrgSharing(rhn, chanlabel)

    description:
    Get organization sharing access control.

    returns:
    str ('public', 'private', or 'protected')

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    """
    try:
        return rhn.session.channel.access.getOrgSharing(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E,'get Org sharing info for channel %s' % chanlabel)

# --------------------------------------------------------------------------------- #

def setOrgSharing(rhn, chanlabel, accesslevel):
    """
    API:
    channel.access.setOrgSharing

    usage:
    setOrgSharing(rhn, chanlabel, accesslevel)

    description:
    Set organization sharing access control. 

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    accesslevel(str)        - access setting ('public', 'private', or 'protected')
    """
    try:
        return rhn.session.channel.access.setOrgSharing(rhn.key, chanlabel, accesslevel) == 1
    except Exception, E:
        return rhn.fail(E,'set Org sharing info for channel %s to %s' % (chanlabel, accesslevel))

# from channel.org
#    * disableAccess
#    * enableAccess
#    * list

# --------------------------------------------------------------------------------- #

def disableAccess(rhn, chanlabel, orgid):
    """
    API:
    channel.org.disableAccess

    usage:
    disableAccess(rhn, chanlabel, orgid)

    description:
    disables access to the channel for the given organization.

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    orgid(int)              - org id being removed access
    """
    try:
        return rhn.session.channel.org.disableAccess(rhn.key, chanlabel, orgid) == 1
    except Exception, E:
        return rhn.fail(E,'disable access to channel %s for org %d' % (chanlabel, orgid))

# --------------------------------------------------------------------------------- #

def enableAccess(rhn, chanlabel, orgid):
    """
    API:
    channel.org.enableAccess

    usage:
    enableAccess(rhn, chanlabel, orgid)

    description:
    enable access to the channel for the given organization.

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - the channel label
    orgid(int)              - org id being granted access
    """
    try:
        return rhn.session.channel.org.enableAccess(rhn.key, chanlabel, orgid) == 1
    except Exception, E:
        return rhn.fail(E,'grant access to channel %s for org %d' % (chanlabel, orgid))

# --------------------------------------------------------------------------------- #

def listOrgs(rhn, chanlabel):
    """
    API:
    channel.org.list

    usage:
    listOrgs(rhn, chanlabel)

    description:
    List the organizations associated with the given channel that may be trusted

    returns:
    list of dict

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

def create(rhn, chanlabel, channame, summary, arch, parent='', checksum=None, gpgkey=None):
    """
    API:
    channel.software.create

    usage:
    create(rhn, chanlabel, channame, summary, arch, parent='', checksum)
    
    description:
    Creates a new software channel with the supplied information.

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel (str)         - the new channel label. lowercase, no spaces.
    channame (str)          - Human-readable channel name.
    summary (str)           - summary of channel
    arch (str)              - channel architecture [ IA-32, IA-64, PPC, Sparc, Sparc Solaris,
                              i386 Solaris, iSeries, pSeries, s390, s390x, x86_64]
    *parent (str)           - the parent channel chanlabel. leave blank to create a new base channel.
    *checksum(str)          - 'sha1' or 'sha256'
    *gpgkey(dict)           - gpg key information { 'url' : str, 'id' : str, 'fingerprint' : str }

    If gpgkey is provided, checksum is also required. Sorry, but that's just how it is.
    """
    try:
        if gpgkey is not None and checksum is not None:
            return rhn.session.channel.software.create(rhn.key, chanlabel, channame, summary,
                                                  arch, parent, checksum, gpgkey) == 1
        elif checksum is not None:
            return rhn.session.channel.software.create(rhn.key, chanlabel, channame, summary,
                                                          arch, parent, checksum) == 1
        else:
            return rhn.session.channel.software.create(rhn.key, chanlabel, channame, summary,
                                                                        arch, parent) == 1
    except Exception, E:
        return rhn.fail(E, 'create software channel %s' % channame)


def createChannel(rhn, chanlabel, channame, summary, arch, **kwargs):
    """
    API:
    channel.software.create

    usage:
    create(rhn, chanlabel, channame, summary, arch, **kwargs)
    where kwargs is a sequence of key=value entries. See the 'parameters' section below
    
    description:
    Creates a new software channel with the supplied information.
    This is a reworking of channel.create using optional parameters passed as key=value pairs

    returns:
    Bool, or throws Exception.

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel (str)             - the new channel label. lowercase, no spaces.
    channame (str)              - Human-readable channel name.
    summary (str)           - summary of channel
    arch (str)              - channel architecture [ IA-32, IA-64, PPC, Sparc, Sparc Solaris,
                              i386 Solaris, iSeries, pSeries, s390, s390x, x86_64]
    *parent (str)           - the parent channel chanlabel. leave blank to create a new base channel.
    *checksum(str)          - 'sha1' or 'sha256'
    *gpgkey(dict)           - gpg key information { 'url' : str, 'id' : str, 'fingerprint' : str }

    If gpgkey is provided, checksum is also required. Sorry, but that's just how it is.
    """
    try:
        return rhn.session.channel.software.create(rhn.key, chanlabel, channame, summary, archLabel='channel-%s' % arch, **kwargs) == 1
    except Exception, E:
        return rhn.fail(E, 'create software channel %s' % channame)
# --------------------------------------------------------------------------------- #

def clone(rhn, source_channel, name, label, summary, parent_label=None, arch_label=None,
          gpg_url=None, gpg_id=None, gpg_fingerprint=None, description=None, no_errata=False):
    """
    API:
    channel.software.clone

    usage:
    clone(rhn,source_channel,name,label,summary, **optional args)

    description:
    Clones an existing channel

    returns:
    Bool, or throws Exception
    
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
    API:
    channel.software.clone

    usage:
    cloneChannel(rhn, chanlabel, noerrata, **kwargs)
        where **kwargs is a list of name=value pairs.
        see parametes below for valid args

    minimal example:
    cloneChannel(rhn, chanlable, noerrata, name=NAME, label=LABEL, summary=SUMMARY)

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
    except Exception, E:
        return rhn.fail(E, "clone channel %s as %s" %(chanlabel, kwargs['label']))

    # SH : For 5.4 just cloning via channel.software.clone is not enough apparently, see :
    # https://access.redhat.com/kb/docs/DOC-55475
    # Without this logic, kicstart profiles fail to find some packages in child channels,
    # meaning things basically don't work
    if isinstance(res,int):
        if ( noerrata == False):
            rhn.session.channel.software.mergeErrata(rhn.key, chanlabel, kwargs['label'])
        rhn.session.channel.software.mergePackages(rhn.key, chanlabel, kwargs['label'])
        rhn.session.channel.software.regenerateNeededCache(rhn.key, kwargs['label'])

    return isinstance(res, int)


# --------------------------------------------------------------------------------- #

def deleteChannel(rhn, chanlabel):
    """
    wrapper for backwards compat
    """
    return delete(rhn, chanlabel)

# --------------------------------------------------------------------------------- #

def delete(rhn, chanlabel):
    """
    API:
    channel.software.delete

    usage:
    deleteChannel(rhn, chanlabel)

    description:
    Deletes a channel using its label as a key
    
    returns:
    Bool

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel (str)     - the channel to delete.
    """
    try:
        return rhn.session.channel.software.delete(rhn.key, chanlabel) == 1
    except Exception, E:
        return rhn.fail(E, 'delete channel %s ' % chanlabel )
    
# --------------------------------------------------------------------------------- #

def detailsByLabel(rhn, chanlabel):
    """
    API:
    channel.software.getDetails
    
    usage:
    detailsByLabel(rhn, chanlabel)

    description:
    Retrieves channel information for a given channel label

    returns:
    dict

    Parameters:
    rhn                     - an authenticated RHN session.
    chanlabel (str)     - the channel label
    """
    try:
        return rhn.session.channel.software.getDetails(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E, 'retrieve details for channel %s ' % chanlabel)

# --------------------------------------------------------------------------------- #

def detailsByID(rhn, chanid):
    """
    API:
    channel.software.getDetails

    usage:
    detailsByID(rhn, chanid)

    description:
    Retrieves channel information for a given channel ID number

    returns:
    dict
    
    parameters:
    rhn                     - an authenticated RHN session.
    chanid (int)        - the channel id
    """
    try:
        return rhn.session.channel.software.getDetails(rhn.key, chanid)
    except Exception, E:
        return rhn.fail(E, 'retrieve details for channel %s ' % chanid)

# --------------------------------------------------------------------------------- #

def addPackages(rhn, chanlabel, packagelist):
    """
    API:
    channel.software.addPackages

    usage:
    addPackages(rhn, chanlabel, packagelist)
    
    description:
    Add packages to a channel using their package IDs
    
    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - channel label
    packagelist(list/int)   - list of package IDs (ints)
    """
    try:
        return rhn.session.channel.software.addPackages(rhn.key, chanlabel, packagelist) == 1
    except Exception, E:
        return rhn.fail(E, 'add packages to %s' % (chanlabel))

# --------------------------------------------------------------------------------- #

def availableEntitlements(rhn, chanlabel):
    """
    API:
    channel.software.availableEntitlements

    usage:
    availableEntitlements(rhn, chanlabel)
    
    description:
    Reports the number of available entitlements for the given channel
    
    returns:
    available entitlement count (int)
    
    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)      - channel label
    """
    try:
        return rhn.session.channel.software.availableEntitlements(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E, 'get number of available entitlements for channel %s' % chanlabel)

# --------------------------------------------------------------------------------- #

def isGloballySubscribable(rhn, chanlabel):
    """
    API:
    channel.software.isGloballySubscribable

    usage:
    isGloballySubscribable(rhn, chanlabel)

    description:
    Checks if a channel is globally subscribable (by all users).

    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)      - channel label
    """
    try:
        return rhn.session.channel.software.isGloballySubscribable(rhn.key, chanlabel) == 1
    except Exception, E:
        return rhn.fail(E, 'get subscribability details for %s' % chanlabel)

# --------------------------------------------------------------------------------- #

def setGloballySubscribable(rhn, chanlabel):
    """
    API:


    usage:
    setGloballySubscribable(rhn, chanlabel)

    description:
    Set a channel to be globally subscribable (by all users)

    returns:
    True if successful. Exception otherwise
    
    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)      - channel label
    """
    try:
        return  rhn.session.channel.software.setGloballySubscribable(rhn.key, chanlabel) == 1
    except Exception, E:
        return rhn.fail(E, 'set channel %s globally subscribable ' % chanlabel)

# --------------------------------------------------------------------------------- #

def isUserSubscribable(rhn, chanlabel, username):
    """
    API:
    channel.software.isUserSubscribable

    usage:
    isUserSubscribable(rhn, chanlabel, username)
    
    description:
    Checks if a channel is subscribable by a specific user.
    
    returns:
    True for yes, False for no, Exception.
    
    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)      - channel label
    username(str)         - the user to check.
    """
    try:
        return  rhn.session.channel.software.isUserSubscribable(rhn.key, chanlabel, username) == 1
    except Exception, E:
        return rhn.fail(E, 'check if user %s can subscribe machines to channel %s' % ( username, chanlabel) )

# --------------------------------------------------------------------------------- #

def setUserSubscribable(rhn, chanlabel, username):
    """
    API:
    channel.software.setUserSubscribable

    usage:
    setUserSubscribable(rhn, chanlabel, username)

    description:
    Set a channel to be subscribable by a specific user.
    
    retu
    rns: True for yes, False for no, Exception.

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)      - channel label
    username(str)         - the user to check.
    """
    try:
        return rhn.session.channel.software.setUserSubscribable(rhn.key, chanlabel, username) == 1
    except Exception, E:
        return rhn.fail(E, 'set channel %s subscribable by user %s' % ( chanlabel, username) )

# --------------------------------------------------------------------------------- #

def listAllPackages(rhn, chanlabel, start_date=None, end_date=None):
    """
    API:
    channel.software.listAllPackages

    usage:
    listPackages(rhn, chanlabel, start_date='', end_date='')
    
    description:
    Lists all packages in a channel, regardless of modification date/time.
    packages may be listed multiple times - each erratum/version has a different ID

    returns:
    list of dict, one per package  [ {..}, {..} ]

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - channel label
    *start_date(str)        - start date. Optional.
    *end_date(str)          - end date. Optional. If no start_date, end_date is ignored.

    Date formats are string representations of iso8601:
    format is '%Y-%m-%d %H:%M:%S' e.g. '2009-01-23 14:05:43'
    """
    try:
        if start_date is None:
            return rhn.session.channel.software.listAllPackages(rhn.key, chanlabel)
        elif end_date is None:
            return rhn.session.channel.software.listAllPackages(rhn.key, chanlabel, start_date)
        else:
            return rhn.session.channel.software.listAllPackages(rhn.key, chanlabel, start_date, end_date)
    except Exception, E:
        return rhn.fail(E, 'list packages in channel %s' % ( chanlabel ) )

# --------------------------------------------------------------------------------- #

def listArches(rhn):
    """
    API:
    channel.software.listArches

    usage:
    listArches(rhn)

    description:
    Lists the possible channel architectures
    
    returns:
    list of dicts, one per architecture. [ {...},...]

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.channel.software.listArches(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list possible channel architectures' )

# --------------------------------------------------------------------------------- #

def listChildren(rhn, chanlabel):
    """
    API:
    channel.software.listChildren

    usage:
    listChildren(rhn, chanlabel)
    
    description:
    List the children of a given channel

    returns:
    list of dict, one per child channel

    params:
    rhn                 - an authenticated RHN session
    chanlabel(str)      - label of base channel
    """
    try:
        return rhn.session.channel.software.listChildren(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E, 'list children of base channel %s' % chanlabel)

# --------------------------------------------------------------------------------- #

def listErrata(rhn, chanlabel, start_date=None, end_date=None):
    """
    API:
    channel.software.listErrata

    usage:
    listErrata(rhn, chanlabel, start_date='', end_date='')

    description:
    Lists the errata in a given channel. Optionally between 2 dates.

    returns:
    list of dict
    
    parameters (* means optional):
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - channel label
    *start_date(str)        - start date. Optional.
    *end_date(str)          - end date. Optional. If no start_date, end_date is ignored.

    Date formats are string representations of iso8601:
    format is '%Y-%m-%d %H:%M:%S' e.g. '2009-01-23 14:05:43'
    """
    try:
        if start_date is None:
            return rhn.session.channel.software.listErrata(rhn.key, chanlabel)
        elif end_date is None:
            return rhn.session.channel.software.listErrata(rhn.key, chanlabel, start_date)
        else:
            return rhn.session.channel.software.listErrata(rhn.key, chanlabel, start_date, end_date)
    except Exception, E:
        return rhn.fail(E, 'list errata in channel %s' % ( chanlabel ) )

# --------------------------------------------------------------------------------- #

def listErrataByType(rhn, chanlabel, errtype):
    """
    API:
    channel.software.listErrataByType

    usage:
    listErrataByType(rhn, chanlabel, errtype)

    description:
    List the errata of a specific type that are applicable to a channel 

    returns:
    list of dict

    Parameters:
    rhn                 -  authenticated RHN session
    chanlabel(str)      - channel to query 
    errtype(str)        - type of advisory ['Security Advisory',
                                           'Product Enhancement Advisory',
                                           'Bug Fix Advisory'] 
    """
    try:
        return rhn.session.channel.software.listErrataByType(rhn.key, chanlabel, errtype)
    except Exception, E:
        return rhn.fail(E, 'fetch %s errata for channel %s' %( errtype, chanlabel ) )

# --------------------------------------------------------------------------------- #

def listLatestPackages(rhn,chanlabel):
    """
    API:
    channel.software.listLatestPackages

    usage:
    listLatestPackages(rhn,chanlabel)

    description:
    Lists the latest packages (highest version/release/epoch) in a given channel
    
    returns:
    list of dicts, one per package.
    
    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - channel label
    """
    try:
        return rhn.session.channel.software.listLatestPackages(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E, 'list latest packages in channel %s' % ( chanlabel ) )

# --------------------------------------------------------------------------------- #

def listPackagesWithoutChannel(rhn):
    """
    API:
    channel.software.listPackagesWithoutChannel

    usage:
    listPackagesWithoutChannel(rhn)

    description:
    Lists all packages that are not in a channel. Typically custom packages.

    returns:
    list of dict

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.channel.software.listPackagesWithoutChannel(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list packages that are not in a  channel' )

# --------------------------------------------------------------------------------- #

def listSubscribedSystems(rhn, chanlabel):
    """
    API:
    channel.software.listSubscribedSystems

    usage:
    listSubscribedSystems(rhn, chanlabel)

    description:
    Lists the systems that are subscribed to a given channel
    
    returns:
    list of dicts - one per system

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - channel label
    """
    try:
        return rhn.session.channel.software.listSubscribedSystems(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E, 'list systems subscribed to channel %s' % ( chanlabel ) )

# --------------------------------------------------------------------------------- #

def listSystemChannels(rhn, systemid):
    """
    API:
    channel.software.listSystemChannels

    usage:
    listSystemChannels(rhn, systemid)

    description:
    Lists the channels a given system is subscribed to.
    
    returns:
    list of dicts, one per channel.
    
    parameters:
    rhn                     - an authenticated RHN session.
    systemid(int)           - system ID
    """
    try:
        return rhn.session.channel.software.listSystemChannels(rhn.key, systemid)
    except Exception, E:
        return rhn.fail(E, 'list channels for system ID %d' % ( systemid ) )

# --------------------------------------------------------------------------------- #

def setSystemChannels(rhn, systemid, chanlist):
    """
    API:
    channel.software.setSystemChannels

    usage:
    setSystemChannels(rhn, systemid, chanlist)

    description:
    Sets the channels a given system is subscribed to, replacing existing subscriptions.
    
    parameters:
    rhn                     - an authenticated RHN session.
    systemid(int)           - system ID
    """
    try:
        rhn.session.channel.software.setSystemChannels(rhn.key, systemid)
    except Exception, E:
        return rhn.fail(E, 'subscribing system ID %d to channels %s' % ( systemid, ','.join(chanlist) ) )

# --------------------------------------------------------------------------------- #

def mergeErrata(rhn, sourcechan, destchan, start_date=None, end_date=None):
    """
    API:
    channel.software.mergeErrata

    usage:
    mergeErrata(rhn, sourcechan, destchan, start_date=None, end_date=None)

    description:
    Merges all errata from one channel to another, optionally between 2 dates

    returns:
    list of dict (representing errata structures)

    parameters (* means optional):
    rhn                     - an authenticated RHN session.
    sourcechan(str)         - source channel label
    destchan(str)           - destination channel label
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
        return rhn.session.channel.software.mergeErrata(rhn.key, sourcechan, destchan, start_date, end_date)
    except Exception, E:
        return rhn.fail(E, 'merge errata from channel %s to channel %s' % (sourcechan, destchan) )

# --------------------------------------------------------------------------------- #

def mergePackages(rhn, sourcechan, destchan):
    """
    API:
    channel.software.mergePackages

    usage:
    mergePackages(rhn, sourcechan, destchan)

    description:
    Merges packages from one channel into another

    returns:
    list of dict (package structures)
    
    parameters:
    rhn                     - an authenticated RHN session.
    sourcechan(str)     - channel label to merge from
    destchan(str)     - channel label to merge into
    """
    try:
        return rhn.session.channel.software.mergePackages(rhn.key, sourcechan, destchan)
    except Exception, E:
        return rhn.fail(E, 'merge packages from channel %s to channel %s ' % ( sourcechan, destchan ) )

# --------------------------------------------------------------------------------- #

def regenerateNeededCache(rhn, chanlabel=None):
    """
    API:
    channel.software.regenerateNeededCache

    usage:
    regenerateNeededCache(rhn, chanlabel)

    description:
    Completely clear and regenerate the needed Errata and Package cache for all
    systems subscribed to the specified channel.
    This should be used only if you believe your cache is incorrect for all the systems in a given channel.

    If run without chanlabel, will regenerate all cache for all channels.
    This requires Satellite Administrator privileges.

    returns:
    Boolean

    parameters:
    rhn(rhnapi.rhnSession)      - authenticated session
    *chanlabel(str)             - label of target channel.
    """
    try:
        if chanlabel is not None:
            return rhn.session.channel.software.regenerateNeededCache(rhn.key, chanlabel) == 1
        else:
            return rhn.session.channel.software.regenerateNeededCache(rhn.key) == 1
            
    except Exception, E:
        return rhn.fail(E, 'Regenerate Errata and Package Cache for channel %s' % chanlabel)

# --------------------------------------------------------------------------------- #

def regenerateYumCache(rhn, chanlabel):
    """
    API:
    channel.software.regenerateYumCache

    usage:
    regenerateYumCache(rhn, chanlabel)

    description:
    Regenerates the yum cache for the specified channel

    returns:
    Bool, or throws Exception

    parameters:
    rhn(rhnapi.rhnSession) - authenticated session
    *chanlabel(str)     - label of target channel.
    """
    try:
        return rhn.session.channel.software.regenerateYumCache(rhn.key, chanlabel) == 1
    except Exception, E:
        return rhn.fail(E, 'regenerate Yum cache for channel %s' % chanlabel)

# --------------------------------------------------------------------------------- #

def removePackages(rhn, chanlabel, package_ids):
    """
    API:
    channel.software.removePackages

    usage:
    removePackages(rhn, chanlabel, package_ids)

    description:
    Removes a list of packages from a channel
    
    returns:
    Bool, or throws Exception

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)      - channel label
    package_ids(list)       - list of package IDs (ints) to remove
    """
    try:
        return rhn.session.channel.software.removePackages(rhn.key, chanlabel, packagelist) == 1
    except Exception, E:
        return rhn.fail(E, 'remove  package IDs %s from channel %s' % ( chanlabel, ','.join(packagelist)) )

# --------------------------------------------------------------------------------- #

def setContactDetails(rhn, chanlabel, name, email, phone, policy):
    """
    API:
    channel.software.setContactDetails    

    usage:
    setContactDetails(rhn, chanlabel, name, email, phone, policy)

    description:
    Sets the administrative contact/support information for a channel

    returns:
    Bool, or throws Exception

    parameters:
    rhn(rhnapi.rhnSession)  - authenticated RHN session object
    chanlabel(str)          - channel label
    name(str)               - channel maintainer's name
    email(str)              - channel maintainer's email
    phone(str)              - channel maintainer's phone number
    policy(str)             - channel support policy
    """
    try:
        return rhn.session.channel.software.setContactDetails(rhn.key, chanlabel,
                                                          name, email, phone, policy) == 1
    except Exception, E:
        return rhn.fail(E, 'set contact details for channel %s' % chanlabel)

# --------------------------------------------------------------------------------- #

def listChildChannels(rhn, chanlabel):
    """
    API:
    none, special case of listChildren

    usage:
    listChildChannels(rhn, chanlabel)

    description:
    Lists the available child channels for a given parent
    
    returns:
    list of channel labels

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)      - channel label
    """
    try:
        return sorted([ x['label'] for x in rhn.session.channel.software.listChildren(rhn.key, chanlabel)])
    except Exception, E:
        return rhn.fail(E, 'list children of channel %s' % ( channel_label ) )
    
# --------------------------------------------------------------------------------- #

def listBaseChannels(rhn, regex=None):
    """
    API:
    None, custom method

    usage:
    listBaseChannels(rhn)

    description:
    List the base channels on your satellite

    returns:
    list of channel labels

    parameters:
    rhn                     - an authenticated RHN session.
    regex(str)              - optional regular expression to match against labels
    """
    try:
        # Note we cannot use listSoftwareChannels here or it wont see channels shared by 
        # multi-org-trusts, ref unresolved BZ655056, therefore it's neccesary to get all 
        # Channels, then see if they have a parent_label via channel.software.getDetails()
        # because, stupidly listAllChannels doesn't return parent_label, ref BZ500690
        allchannels = sorted(rhn.session.channel.listAllChannels(rhn.key), key=itemgetter('label'))
        basechannels = list()
        for channel in allchannels:
            chdetails = rhn.session.channel.software.getDetails(rhn.key, channel['id'])
            if len(chdetails['parent_channel_label']) == 0:
                basechannels.append(channel['label'])
        if regex is not None:
            pattern = re.compile(r'%s' % str(regex))
            return [ x for x in basechannels if pattern.search(x) ]
        else:
            return basechannels
    except Exception, E:
        return rhn.fail(E, 'list base channels on your satellite')
    
def channelsByArch(rhn, archlabel):
    """
    API:
    none, custom method

    usage:
    channelsByArch(rhn, archlabel)

    description:
    lists all channels of a given architecture. 


    returns:
    list of string (channel labels)

    parameters:
    rhn                     - an authenticated RHN session
    archlabel(str)          - the channel architecture to list.
    """
    try:
        chanlist = rhn.session.channel.listSoftwareChannels(rhn.key)
        return [ x['label'] for x in chanlist if x['arch'] == archlabel ]
    except Exception, E:
        return rhn.fail(E, "find channels with arch %s" % (arch))

# --------------------------------------------------------------------------------- #
# Methods under here are not technically part of the API, just utility functions I added
# to simplify scripting of channel deletion...

def hasChildren(rhn, chanlabel):
    """
    API:
    none, custom method

    usage:
    hasChildren(rhn, chanlabel)

    description:
    check if the given channel label has child channels.

    returns:
    Bool, or throws Exception

    params:
    rhn                - authentication rhnapi.rhnSession
    chanlabel(str) - the channel label to check
    """
    try:
        return len(rhn.session.channel.software.listChildren(rhn.key, chanlabel)) != 0
    except Exception, E:
        return rhn.fail(E, 'check for children of channel %s' % channel_label)

def deleteRecursive(rhn, chanlabel):
    """
    API:
    none, custom method
    
    usage:
    deleteRecursive(rhn, chanlabel)

    description:
    deletes all children of a given custom channel, then the channel itself.
    This could cause utter mayhem, be careful.

    returns:
    Bool, or throws Exception

    params:
    rhn                 - authenticated rhnapi.rhnSession 
    chanlabel(str)  - label of parent channel
    """
    # I could call my other utility methods in here, but for portability, 
    # I'm using the API directly
    try:
        if hasChildren(rhn, chanlabel):
            for child in rhn.session.channel.software.listChildren(rhn.key, chanlabel):
                rhn.session.channel.software.delete(rhn.key, child['label'])
        # handily, this will fail if any of the child channels could not be deleted:
        return rhn.session.channel.software.delete(rhn.key, chanlabel) == 1
    except Exception, E:
        return rhn.fail(E, 'recursively delete channel %s and all its child channels' % channel_label)

def cloneRecursive(rhn, chanlabel, prefix=None, suffix=None):
    """
    API:
    none, custom method

    CUSTOM METHOD
    A placeholder for a custom method to recursively clone channels,
    adding either a prefix or suffix (or both) to their existing labels
    Mostly I envision this being a date (for example) or something like 'prod' or 'test'

    usage:
    cloneRecursive(rhn, parent_label, target_label, prefix=None, suffix=None)

    returns:
    list of dict, one per newly cloned channel. Or possibly just a bool. Who knows?

    params: ( * = optional )
    rhn                         - authenticated rhn session object
    chanlabel(str)              - the (parent) channel label to clone  
    *prefix(str)                - prefix (prepended to destination channel labels)
    *suffix(str)                - suffix (appended to destination channel labels)

    You really MUST provide one of prefix or suffix, as otherwise the cloning will fail,
    because source and target labels will be identical.
    """
    return 'Not Implemented Yet'
    
# --------------------------------------------------------------------------------- #
def channelExists(rhn, channel_label):
    """
    CUSTOM METHOD
    Custom RHN API method to confirm the existence of a channel label on your satellite.

    returns: bool

    params:
    rhn                 - authenticated rhnapi.rhnSession object
    channel_label(str)  - label of channel to look for
    """
    try:
        chanlist = [ x['label'] for x in listSoftwareChannels(rhn) ]
        if channel_label in chanlist:
            return True
        else:
            return False
    except Exception, E:
        return rhn.fail(E, 'check channel existence')


