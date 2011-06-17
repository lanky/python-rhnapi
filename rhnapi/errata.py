#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# an abstraction of the 'errata' namespace from the RHN API
# from satellite 5.1.0.
# earlier versions may behave oddly
# later versions may change the output.

# to provide the parent RHN class.
# current methods to cover:
#    * addPackages
#    * applicableToChannels
#    * bugzillaFixes
#    * clone
#    * create
#    * delete
#    * findByCve
#    * getDetails
#    * listAffectedSystems
#    * listByDate
#    * listCves
#    * listKeywords
#    * listPackages
#    * listUnpublishedErrata
#    * publish
#    * publishAsOriginal
#    * removePackages
#    * setDetails


def addPackages(rhn, advisory, packages):
    """
    API: errata.addPackages

    usage: addPackages(rhn, advisory, packages)

    description:
    Add a set of packages to an erratum with the given advisory name.
    This method will only allow for modification of custom errata created either through the UI or API

    returns: int (number of packages successfully added) or exception

    parameters:
    rhn                         - an authenticated RHN session
    advisory(str)               - errata advisory name
    packages(list of int)       - list of package ids

    returns int (number of packages added)
    """
    try:
        return rhn.session.errata.addPackages(rhn.key, advisory, packages)
    except Exception, E:
        return rhn.fail(E, 'add packages to erratum %s' % advisory)
        
def applicableToChannels(rhn, advisory):
    """
    API: errata.applicableToChannels

    usage: applicableToChannels(rhn, advisory)

    description:
    Lists the channels that an advisory applies to.

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    """
    try:
        return rhn.session.errata.applicableToChannels(rhn.key, advisory)
    except Exception, E:
        return rhn.fail(E, 'list channels affected by erratum %s' % advisory)
# errata.bugzillaFixes
def bugzillaFixes(rhn, advisory):
    """
    usage: bugzillaFixes(rhn, advisory)

    Lists the bugzilla fixes that an advisory applies to.

    returns: list of bugzilla IDs

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    """
    try:
        return rhn.session.errata.bugzillaFixes(rhn.key, advisory)
    except Exception, E:
        return rhn.fail(E, 'list bugzilla fixes provided by by erratum %s' % advisory)

# errata.clone
def clone(rhn, channel_label, advisorys):
    """
    usage: cloneErrata(RHN, channel_label, advisorys)

    Clones errata from into a given channel

    returns: list of dicts, one per erratum

    parameters:
    rhn                      - an authenticated RHN session
    channel_label(str)       - the target channel
    advisorys(list/str)  - list of errata advisory names
    """
    try:
        return rhn.session.errata.clone(rhn.key, channel_label, advisorys)
    except Exception, E:
        return rhn.fail(E, 'clone errata %s into channel %s' % (','.join(advisorys), channel_label))

def create(rhn, erratum_info, bugs = [], keywords = [] , packages = [], publish = False, channels = None  ):
    """
    usage: createErrata(rhn, ARGS)

    creates an erratum. This is far too complicated atm, so is not yet implemented.
    At a basic level, this creates an erratum with no associated  bugs
    Expects a dict argument to create the basic erratum.

    parameters:
    rhn                           - authenticated rhnapi.rhnSession
    errata_info(dict)             - erratum expressed as a dict: { synopsis(str) , advisory_name(str),
                                    advisory_release(int) ,
                                    advisory_type(str) - one of ['Security Advisory',
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
    )

    THis may have to be put into several methods!

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    """
    try:
        return rhn.session.errata.create(rhn.key, erratum_info, bugs, keywords, packages, channels)
    except Exception, E:
        return rhn.fail(E, 'create new erratum %s' % errata_info['advisory_name'])

def createErratum(rhn, synopsis, name, release, erratatype, product = '', topic = '' , description = '', references = '' , notes = '', solution = ''):
    """
    usage: createErratum(rhn, synopsis, name, release,
                         erratatype, product, topic = '' ,
                         descroption = '', references = '' ,
                         notes = '', solution = '')
    create a dict from the parameters passed and then pass that onto rhnapi.errata.create() above
    Intended to create a basic erratum object, which we can then manipulate.
    unpublished, with no associated bugs, packages, or channels.

    returns dict, or throws exception

    parameters:
    rhn                             - authenticated rhnapi.rhnSession object
    synopsis(str)                   - short summary of the erratum
    name(str)                       - name of the erratum
    release(int)                    - release of the erratum
    erratumtype(str)                - one of ['Security Advisory',
                                              'Product Enhancement Advisory',
                                              'Bug Fix Advisory'],
    product(str)                    - what does this erratum affect? (RPM name, OS etc)
    topic(str)                      - erratum topic
    description(str)                - longer description of the erratum
    references(str)                 - erratum refs, possibly internalt ticket numbers, URLs etc
    notes(str)                      - freeform notes str
    solutionn(str)                  - how the 'bug' was fixed (i.e. what the erratum does)
    """
    return create(rhn, { 'synopsis' : synopsis, 'advisory_name' : name, 'advisory_release' : release,
                         'advisory_type' : erratumtype, 'product' : product, 'topic' : topic,
                         'description' : description, 'references' : references, 'solution' : solution} )

def delete(rhn, advisory):
    """
    usage: delete(rhn, advisory)

    deletes an erratum

    returns: True, or exception thrown

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    """
    try:
        return rhn.session.errata.delete(rhn.key, advisory) == 1
    except Exception, E:
        return rhn.fail(E, 'delete erratum %s' % advisory)

def findByCve(rhn, cveName):        
    """
    usage: findByCve(rhn, cveName)

    Lookup the details for errata associated with the given CVE (e.g. CVE-2008-3270)

    returns: list of dict (errata)

    parameters:
    rhn                      - an authenticated RHN session
    findByCve(str)        - errata advisory name
    """
    try:
        return rhn.session.errata.findByCve(rhn.key, cveName)
    except Exception, E:
        return rhn.fail(E, 'find errata for CVE %s' % cveName)

def getDetails(rhn, advisory):
    """
    usage: getDetails(RHN, advisory)

    Retrieves details for the given erratum

    returns: dict

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    """
    try:
        return rhn.session.errata.getDetails(rhn.key, advisory)
    except Exception, E:
        return rhn.fail(E, 'list details for erratum %s' % advisory)

def listAffectedSystems(rhn, advisory):
    """
    API: errata.

    usage: 

    Lists the system 

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    """
    try:
        return rhn.session.errata.listAffectedSystems(rhn.key, advisory)
    except Exception, E:
        return rhn.fail(E, 'list systems affected by erratum %s' % advisory)
    
def listByDate(rhn, channel_label):
    """
    usage: listByDate(rhn, channel_label)

    Lists Errata in date order.

    returns: list of dicts:
    { id, date, type, name, advisory }

    parameters:
    rhn                      - an authenticated RHN session
    channel_label(str)       - the affected channel
    """
    try:
        return rhn.session.errata.listByDate(rhn.key, channel_label)
    except Exception, E:
        return rhn.fail(E, 'list errata by date for channel %s' % (channel_label) )

def listCVEs(rhn, advisory):
    """
    usage: listCVEs(rhn, advisory)

    Lists the CVEs assosicated with an erratum

    returns: list of CVE strings

    parameters:
    rhn                      - an authenticated RHN session
    advisory             - the name an advisory
    """
    try:
        return rhn.session.errata.listCves(rhn.key, advisory)
    except Exception, E:
        return rhn.fail(E, 'list CVEs for advisory %s' % advisory)

def listKeywords(rhn, advisory):
    """
    usage: listKeywords(rhn, advisory)

    Lists the package filenames affected by a given erratum

    returns: list of keywords(str)

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    """
    try:
        return rhn.session.errata.listKeywords(rhn.key, advisory)
    except Exception, E:
        return rhn.fail(E, 'list keywords for erratum %s' % advisory)

def listPackages(rhn, advisory):
    """
    usage: listPackages(rhn, advisory)

    Lists the packages affected by an erratum

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    """
    try:
        return rhn.session.errata.listPackages(rhn.key, advisory)
    except Exception, E:
        return rhn.fail(E, 'list packages affected by erratum %s' % advisory)

# custom method
def listPackageNames(rhn, advisory):
    """
    usage: listPackages(rhn, advisory)

    Lists the package filenames affected by a given erratum
    (custom method)

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    """
    try:
        return sorted([ "%(name)s-%(version)s-%(release)s" % x for x in rhn.session.errata.listPackages(rhn.key, advisory)])
    except Exception, E:
        return rhn.fail(E, 'list packages affected by erratum %s' % advisory)

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
                               * advisory name/number
    """
    if rhn.satellite_version >= '5.4.0':
        return "This method is deprecated in Satellite 5.4 and no longer works."
    try:
        return rhn.session.errata.getOval(rhn.key, errata_id)
    except Exception, E:
        return rhn.fail(E, 'get info for the erratum %s' % errata_id)

def listUnpublishedErrata(rhn):
    """
    usage: listUnpublishedErrata(rhn)

    Returns a list of unpublished errata 

    returns: list of dict

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.errata.listUnpublishedErrata(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list unpublished errata')

def publish(rhn, advisory, channels):
    """
    usage: publishErrata(rhn, advisory, channels)

    Publishes an erratum into a list of channels

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    advisory             - the erratum to publish
    channels(list/str)   - the channels to puclish this erratum to
    """
    try:
        return rhn.session.errata.publish(rhn.key, advisory, channels)
    except Exception, E:
        return rhn.fail(E, 'publish erratum %s to channels %s' % (advisory, ','.join(channels)))

def publishAsOriginal(rhn, advisory, channels):        
    """
    usage: publishAsOriginal(rhn, advisory, channels)
    
    Publishes an existing (unpublished) cloned errata to a set of cloned channels according to its original erratum 

    returns: dict

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    channels(list of str) - list of channel labels to publish erratum into
    """
    try:
        return rhn.session.errata.publishAsOriginal(rhn.key, advisory, channels)
    except Exception, E:
        return rhn.fail(E, 'publish erratum %s' % advisory)

def removePackages(rhn, advisory, packages):        
    """
    usage: removePackages(rhn, advisory, packages)

    Remove a set of packages from an erratum with the given advisory name.
    This method will only allow for modification of custom errata created either through the UI or API. 

    returns: list of keywords(str)

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    packages(list of int) - list of package IDs to remove.
    """
    try:
        return rhn.session.errata.removePackages(rhn.key, advisory, packages)
    except Exception, E:
        return rhn.fail(E, 'remove packages from erratum %s' % advisory)

def setDetails(rhn, advisory, errata_dict):        
    """
    usage: setDetails(rhn, advisory, errata_dict)

    Lists the package filenames affected by a given erratum

    returns: True, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    advisory(str)        - errata advisory name
    errata_dict(dict)        - erratum in dict form
    """
    try:
        return rhn.session.errata.setDetails(rhn.key, advisory, errata_dict) == 1
    except Exception, E:
        return rhn.fail(E, 'set details for erratum %s' % advisory)
        
