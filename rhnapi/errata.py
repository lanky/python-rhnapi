#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the 'errata' namespace
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

# ---------------------------------------------------------------------------------- #

def addPackages(rhn, erratum, packagelist):
    """
    API:
    errata.addPackages

    usage:
    addPackages(rhn, erratum, packagelist)

    description:
    Add a set of packages to an erratum with the given erratum name.
    This method will only allow for modification of custom errata created either through the UI or API

    returns:
    int (number of packages successfully added)

    parameters:
    rhn                         - an authenticated RHN session
    erratum(str)                - erratum advisory name
    packagelist(list of int)    - list of package ids
    """
    try:
        return rhn.session.errata.addPackages(rhn.key, erratum, packagelist)
    except Exception, E:
        return rhn.fail(E, 'add packagelist to erratum %s' % erratum)

# ---------------------------------------------------------------------------------- #
        
def applicableToChannels(rhn, erratum):
    """
    API:
    errata.applicableToChannels

    usage:
    applicableToChannels(rhn, erratum)

    description:
    Lists the channels that an erratum applies to.

    returns:
    list of dict, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    erratum(str)        - errata erratum name
    """
    try:
        return rhn.session.errata.applicableToChannels(rhn.key, erratum)
    except Exception, E:
        return rhn.fail(E, 'list channels affected by erratum %s' % erratum)

# ---------------------------------------------------------------------------------- #

def bugzillaFixes(rhn, erratum):
    """
    API:
    errata.bugzillaFixes

    usage:
    bugzillaFixes(rhn, erratum)

    description:
    Lists the bugzilla fixes that an erratum applies to.

    returns:
    dict, using bugzilla IDs as keys.
    For example
     {'230295': "['CVE-2007-0998 HVM guest VNC server allows compromise of
     entire host OS by any VNC console user']"}

    parameters:
    rhn                     - an authenticated RHN session
    erratum(str)            - erratum advisory name
    """
    try:
        return rhn.session.errata.bugzillaFixes(rhn.key, erratum)
    except Exception, E:
        return rhn.fail(E, 'list bugzilla fixes provided by by erratum %s' % erratum)

# ---------------------------------------------------------------------------------- #

def clone(rhn, chanlabel, errlist):
    """
    API:
    errata.clone

    usage:
    clone(rhn, chanlabel, errlist)
    
    description:
    Clones errata from into a given channel

    returns:
    list of dict, one per erratum

    parameters:
    rhn                     - an authenticated RHN session
    chanlabel(str)          - the target channel
    errlist(list/str)       - list of erratum advisory names
    """
    try:
        return rhn.session.errata.clone(rhn.key, chanlabel, errlist)
    except Exception, E:
        return rhn.fail(E, 'clone errata %s into channel %s' % (','.join(errlist), chanlabel))

# ---------------------------------------------------------------------------------- #

def cloneAsync(rhn, chanlabel, errlist):
    """
    API:
    errata.cloneAsync

    usage:
    clone(rhn, chanlabel, errlist)
    
    description:
    Clones errata from into a given channel

    returns:
    bool

    parameters:
    rhn                     - an authenticated RHN session
    chanlabel(str)          - the target channel
    errlist(list/str)       - list of erratum advisory names
    """
    try:
        return rhn.session.errata.cloneAsync(rhn.key, chanlabel, errlist) == 1
    except Exception, E:
        return rhn.fail(E, 'clone errata %s into channel %s' % (','.join(errlist), chanlabel))

# ---------------------------------------------------------------------------------- #

def cloneAsOriginal(rhn, chanlabel, errlist):
    """
    API:
    errata.cloneAsOriginal

    usage:
    cloneAsOriginal(rhn, chanlabel, errlist)

    description:
    clones an erratum into a cloned channel with reference to the original source channel,
    pushing only packages that are relevant to the target channel.

    e.g.
    if an erratum contains packages affecting multiple RH channels and it is cloned into a
    channel that was cloned from RHEL5, this call only pushes *relevant* packages to the
    destination channel, not ALL of them.
    This should be used for preference over the basic errata.clone call.

    parameters:
    rhn                     - an authenticated RHN session
    chanlabel(str)          - the target channel
    errlist(list/str)       - list of erratum advisory names
    """
    try:
        return rhn.session.errata.cloneAsOriginal(rhn.key, chanlabel, errlist)
    except Exception, E:
        return rhn.fail(E, 'clone errata into channel %s' % chanlabel)

# ---------------------------------------------------------------------------- #

def cloneAsOriginalAsync(rhn, chanlabel, errlist):
    """
    API:
    errata.cloneAsOriginalAsync

    usage:
    cloneAsOriginalAsync(rhn, chanlabel errlist)

    description:
    Asynchronously clones a list of errata into a cloned channel with
    reference to the original source channel, pushing only packages that
    are relevant to the target channel.

    e.g.
    if an erratum contains packages affecting multiple RH channels and it is
    cloned into a channel that was cloned from RHEL5, this call only pushes
    *relevant* packages to the destination channel, not ALL of them.
    """
    try:
        return rhn.session.errata.cloneAsOriginalAsync(rhn.key, chanlabel, errlist) == 1
    except Exception, E:
        return rhn.fail(E, 'Asynchronously clone errata into channel %s', chanlabel)


# ---------------------------------------------------------------------------------- #

def create(rhn, errobj, bugs = [], keywords = [] , packages = [], publish = False, channels = None  ):
    """
    API:
    errata.create

    usage:
    createErrata(rhn, ARGS)

    creates an erratum. This is far too complicated atm, so is not yet implemented.
    At a basic level, this creates an erratum with no associated  bugs
    Expects a dict argument to create the basic erratum.

    parameters:
    rhn                           - authenticated rhnapi.rhnSession
    errobj(dict)                  - erratum expressed as a dict: { synopsis(str) , erratum_name(str),
                                    erratum_release(int) ,
                                    erratum_type(str) - one of ['Security Advisory',
                                            'Product Enhancement Advisory', 'Bug Fix Advisory'],
                                    product(str),
                                    topic(str),
                                    description(str),
                                    references(str),
                                    notes(str),
                                    solution(str) },
    * bugs(list/dict)             - list of bug dicts [ { 'id' : int, 'summary' : str },...]
    * keywords(list/str)          - arbitrary keywords[ keyword1, keyword2...],
    * packageslist(list/int)      - list of package IDs
    * publish(bool)               - whether to automatically publish the erratum (False)
    * channels(list/str)          - list of channel labels to publish into, if publish is True

    This may have to be put into several methods!

    returns:
    list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    erratum(str)        - errata erratum name
    """
    try:
        return rhn.session.errata.create(rhn.key, errobj, bugs, keywords, packages, channels)
    except Exception, E:
        return rhn.fail(E, 'create new erratum %(erratum_name)s' % errobj)

# ---------------------------------------------------------------------------------- #

def createErratum(rhn, synopsis, name, release, errtype, product = '', topic = '' , description = '', references = '' , notes = '', solution = ''):
    """
    API:
    none, special simplified case of errata.create
    
    usage:
    createErratum(rhn, synopsis, name, release,
                         erratatype, product, topic = '' ,
                         descroption = '', references = '' ,
                         notes = '', solution = '')

    description:
    creates a dict from the parameters passed and then pass that onto rhnapi.errata.create() above
    Intended to create a basic erratum object, which we can then manipulate.
    unpublished, with no associated bugs, packages, or channels.

    returns dict, or throws exception

    parameters:
    rhn                             - authenticated rhnapi.rhnSession object
    synopsis(str)                   - short summary of the erratum
    name(str)                       - name of the erratum
    release(int)                    - release of the erratum
    errtype(str)                    - one of ['Security Advisory',
                                              'Product Enhancement Advisory',
                                              'Bug Fix Advisory'],
    product(str)                    - what does this erratum affect? (RPM name, OS etc)
    topic(str)                      - erratum topic
    description(str)                - longer description of the erratum
    references(str)                 - erratum refs, possibly internalt ticket numbers, URLs etc
    notes(str)                      - freeform notes str
    solutionn(str)                  - how the 'bug' was fixed (i.e. what the erratum does)
    """
    return create(rhn, { 'synopsis' : synopsis, 'erratum_name' : name, 'erratum_release' : release,
                         'erratum_type' : errtype, 'product' : product, 'topic' : topic,
                         'description' : description, 'references' : references, 'solution' : solution} )

# ---------------------------------------------------------------------------------- #

def delete(rhn, erratum):
    """
    API:
    errata.delete

    usage: 
    delete(rhn, erratum)

    description:
    deletes an erratum

    returns:
    Boolean

    parameters:
    rhn                     - an authenticated RHN session
    erratum(str)            - errata erratum name
    """
    try:
        return rhn.session.errata.delete(rhn.key, erratum) == 1
    except Exception, E:
        return rhn.fail(E, 'delete erratum %s' % erratum)

# ---------------------------------------------------------------------------------- #

def findByCve(rhn, cvename):        
    """
    API:
    errata.findByCve

    usage:
    findByCve(rhn, cvename)

    description:
    Lookup the details for errata associated with the given CVE (e.g. CVE-2008-3270)

    returns:
    list of dict (errata)

    parameters:
    rhn                     - an authenticated RHN session
    cvename(str)            - errata erratum name
    """
    try:
        return rhn.session.errata.findByCve(rhn.key, cvename)
    except Exception, E:
        return rhn.fail(E, 'find errata for CVE %s' % cvename)

# ---------------------------------------------------------------------------------- #

def getDetails(rhn, erratum):
    """
    API:
    errata.getDetails

    usage:
    getDetails(RHN, erratum)

    description:
    Retrieves details for the given erratum

    returns:
    dict

    parameters:
    rhn                     - an authenticated RHN session
    erratum(str)            - errata erratum name
    """
    try:
        return rhn.session.errata.getDetails(rhn.key, erratum)
    except Exception, E:
        return rhn.fail(E, 'list details for erratum %s' % erratum)

# ---------------------------------------------------------------------------------- #

def listAffectedSystems(rhn, erratum):
    """
    API:
    errata.listAffectedSystems

    usage:
    listAffectedSystems(rhn, erratum)

    description:
    Lists the systems affected by the given erratum

    returns:
    list of dict, one per system

    parameters:
    rhn                     - an authenticated RHN session
    erratum(str)            - errata erratum name
    """
    try:
        return rhn.session.errata.listAffectedSystems(rhn.key, erratum)
    except Exception, E:
        return rhn.fail(E, 'list systems affected by erratum %s' % erratum)

# ---------------------------------------------------------------------------------- #
    
def listByDate(rhn, chanlabel):
    """
    API:
    errata.listByDate

    usage:
    listByDate(rhn, chanlabel)

    description:
    Lists Errata in date order.
    This method is deprecated, see channel.listErrata instead

    returns:
    list of dict, one per erratum
    { id, date, type, name, erratum }

    parameters:
    rhn                      - an authenticated RHN session
    chanlabel(str)       - the affected channel
    """
    try:
        return rhn.session.errata.listByDate(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E, 'list errata by date for channel %s' % (chanlabel) )

# ---------------------------------------------------------------------------------- #

def listCVEs(rhn, erratum):
    """
    API:
    errata.listCves

    usage:
    listCVEs(rhn, erratum)

    description:
    Lists the CVEs assosicated with an erratum

    returns:
    list of CVE strings

    parameters:
    rhn                     - an authenticated RHN session
    erratum                 - the name an erratum
    """
    try:
        return rhn.session.errata.listCves(rhn.key, erratum)
    except Exception, E:
        return rhn.fail(E, 'list CVEs for erratum %s' % erratum)

# ---------------------------------------------------------------------------------- #

def listKeywords(rhn, erratum):
    """
    API:
    errata.listKeywords

    usage:
    listKeywords(rhn, erratum)

    description:
    Lists the keywords associated with an erratum

    returns:
    list of keywords(str)

    parameters:
    rhn                     - an authenticated RHN session
    erratum(str)            - errata erratum name
    """
    try:
        return rhn.session.errata.listKeywords(rhn.key, erratum)
    except Exception, E:
        return rhn.fail(E, 'list keywords for erratum %s' % erratum)

# ---------------------------------------------------------------------------------- #

def listPackages(rhn, erratum):
    """
    API:
    errata.listPackages

    usage:
    listPackages(rhn, erratum)

    description:
    Lists the packages affected by an erratum

    returns:
    list of dict, one per package

    parameters:
    rhn                     - an authenticated RHN session
    erratum(str)            - errata erratum name
    """
    try:
        return rhn.session.errata.listPackages(rhn.key, erratum)
    except Exception, E:
        return rhn.fail(E, 'list packages affected by erratum %s' % erratum)

# ---------------------------------------------------------------------------------- #

def listPackageNames(rhn, erratum):
    """
    API:
    none, custom method (special case of listPackages)

    usage:
    listPackageNames(rhn, erratum)

    description:
    Lists the package filenames in a given erratum

    returns:
    list of str (filenames)

    parameters:
    rhn                      - an authenticated RHN session
    erratum(str)        - errata erratum name
    """
    try:
        return sorted([ "%(name)s-%(version)s-%(release)s.%(arch_label)s.rpm" % x for x in rhn.session.errata.listPackages(rhn.key, erratum)])
    except Exception, E:
        return rhn.fail(E, 'list packages provided by erratum %s' % erratum)

def getOval(rhn, errata_id):
    """
    usage: getOval(rhn, errata_id)

    Gives OVAL metadata (XML) for the specified erratum

    returns: string (XML metadata)
    although I have singularly failed to get this working now :)
    'unhandled exception:null' appears to be the best it can provide :(

    parameters:
    rhn                      - an authenticated RHN session
    errata_id(str)           - errata identifier: one of
                               * errata ID
                               * CVE/CAN (remove all dashes)
                               * erratum name/number
    """
    if rhn.satellite_version >= '5.4.0':
        return "This method is no longer available from Satellite 5.4 onwards."
    try:
        return rhn.session.errata.getOval(rhn.key, errata_id)
    except Exception, E:
        return rhn.fail(E, 'get Oval info for the erratum %s' % errata_id)

# ---------------------------------------------------------------------------------- #

def listUnpublishedErrata(rhn):
    """
    API:
    errata.listUnpublishedErrata

    usage:
    listUnpublishedErrata(rhn)

    description:
    Returns a list of unpublished (custom) errata 

    returns:
    list of dict

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.errata.listUnpublishedErrata(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list unpublished errata')

# ---------------------------------------------------------------------------------- #

def publish(rhn, erratum, chanlist):
    """
    API:
    errata.publish

    usage:
    publish(rhn, erratum, chanlist)

    description:
    Publishes an erratum into a list of channels

    returns:
    list of dict, one per channel.

    parameters:
    rhn                     - an authenticated RHN session
    erratum                 - the erratum to publish
    chanlist(list/str)      - the chanlist to puclish this erratum to
    """
    try:
        return rhn.session.errata.publish(rhn.key, erratum, chanlist)
    except Exception, E:
        return rhn.fail(E, 'publish erratum %s to chanlist %s' % (erratum, ','.join(chanlist)))

# ---------------------------------------------------------------------------------- #

def publishAsOriginal(rhn, erratum, chanlist):        
    """
    API:
    errata.publishAsOriginal

    usage:
    publishAsOriginal(rhn, erratum, chanlist)

    description:    
    Publishes an existing (unpublished) cloned errata to a set of cloned chanlist according to its original erratum
    (i.e. only pushes packages appropriate to the destination channels)

    returns:
    dict

    parameters:
    rhn                     - an authenticated RHN session
    erratum(str)            - errata erratum name
    chanlist(list of str)   - list of channel labels to publish erratum into
    """
    try:
        return rhn.session.errata.publishAsOriginal(rhn.key, erratum, chanlist)
    except Exception, E:
        return rhn.fail(E, 'publish erratum %s' % erratum)

# ---------------------------------------------------------------------------------- #

def removePackages(rhn, erratum, packageids):        
    """
    API:
    errata.removePackages

    usage:
    removePackages(rhn, erratum, pkglist)

    description:
    Remove a set of packages from an erratum with the given erratum name.
    This method will only allow for modification of custom errata created either through the UI or API. 

    returns:
    list of keywords(str)

    parameters:
    rhn                     - an authenticated RHN session
    erratum(str)            - errata erratum name
    pkglist(list of int)    - list of package IDs to remove.
    """
    try:
        return rhn.session.errata.removePackages(rhn.key, erratum, packageids)
    except Exception, E:
        return rhn.fail(E, 'remove packages from erratum %s' % erratum)

def setDetails(rhn, erratum, errdict):        
    """
    API:
    errata.setDetails

    usage:
    setDetails(rhn, erratum, errdict)

    description:
    sets details for the specified erratum. Info is provided in a dict format.
    Any omitted keys are unaffected
    This method will only allow for modification of custom errata created either through the UI or API.

    returns:
    Boolean

    parameters:
    rhn                     - an authenticated RHN session
    erratum(str)            - errata erratum name
    errdict(dict)           - erratum in dict form
    """
    try:
        return rhn.session.errata.setDetails(rhn.key, erratum, errdict) == 1
    except Exception, E:
        return rhn.fail(E, 'set details for erratum %s' % erratum)

def modifyDetails(rhn, erratum, **kwargs):
    """
    API:
    none, custom method (special case of setDetails)

    usage:
    modifyDetails(rhn, erratum, **kwargs)
    where **kwargs is a number of key=value pairs (see parameters below)

    description:
    special case of errata.setDetails

    returns:
    Boolean

    parameters:
    rhn                     - an authenticated RHN session
    erratum(str)            - errata erratum name

    plus one or more of the following as KEY=VAL pairs
    synopsis (str)          - description of the erratum
    advisory_name(str)      - name of erratum (trad: PREFIX-YYYY:NNNN)
    advisory_release(int)   - Advisory Release
    advisory_type(str)      - Type of advisory (one of the following: 'Security Advisory', 'Product Enhancement Advisory', or 'Bug Fix Advisory'
    product(str)
    topic(str)
    description(str)
    references(str)
    notes(str)
    solution(str)
    bugs(list/dict)         - List of dict, one per bug { 'id' : (int) , 'summary' : (str) }
    keywords(list/str)      - List of keywords to associate with the errata.
    CVEs(list/str)          - List of CVEs to associate with the errata
    """
    try:
        return rhn.session.errata.setDetails(rhn.key, erratum, kwargs) == 1
    except Exception, E:
        return rhn.fail(E, 'modify details for erratum %s' % erratum)
        
# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
