#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstrating the kickstart namespace
# as well as all its sub-namespaces / children
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

from operator import itemgetter

#     * cloneProfile
#     * createProfile
#     * createProfileWithCustomUrl
#     * deleteProfile
#     * findKickstartForIp
#     * importFile
#     * importRawFile
#     * listAllIpRanges
#     * listKickstartableChannels
#     * listKickstartableTrees
#     * listKickstarts
#     * renameProfile

def cloneProfile(rhn, kslabel, clonelabel):
    """
    API:
    kickstart.cloneProfile

    usage:
    cloneProfile(rhn, kslabel)

    description:
    clone an existing kickstart pofile with a new name

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    clonelabel               - The kickstart profile label for the new clone
    """
    try:
        return rhn.session.kickstart.cloneProfile(rhn.key, kslabel, clonelabel) == 1
    except Exception, E:
        return rhn.fail(E, 'clone kickstart profile %s as %s' % kslabel)

# ---------------------------------------------------------------------------- #

def createProfile(rhn, kslabel, kstree, rootpass, kshost = '', virttype = 'none'):
    """
    API:
    kickstart.createProfile

    usage:
    createProfile(rhn, kslabel, virttype, kstreelabel, kshost, rootpass)

    description:
    Creates a new kickstart profile.

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel(str)             - the kickstart profile label to create
    virttype(str)              - virtualization type, one of:
                               ['fully_virtualized', 'para_virtualized', 'none']
    kstree(str)              - kickstart tree label to be used
    kshost(str)              - the host to kicktart from.on
    rootpass(str)            - the root password to use in the kickstart
    """
    if kshost == '':
        kshost = rhn.hostname
    try:
        return rhn.session.kickstart.createProfile(rhn.key, kslabel, virttype, kstree, kshost, rootpass) == 1
    except Exception, E:
        return rhn.fail(E, 'create new kickstart profile %s' % kslabel)

# ---------------------------------------------------------------------------- #

def createProfileWithCustomUrl(rhn, kslabel, virttype, kstree, ksurl, rootpass):
    """
    API:
    kickstart.createProfileWithCustomUrl

    usage:
    createProfileWithCustomUrl(rhn, kslabel, virttype, kstree, ksurl, rootpass)

    description:
    creates a kickstartprofile with a custom URL (custom install location)
    Lists the package filenames affected by a given erratum

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel(str)             - the kickstart profile label to create
    virttype(str)              - virtualization type, one of:
                               ['fully_virtualized', 'para_virtualized', 'none']
    kstree(str)              - kickstart tree label to be used
    ksurl(str)               - the custom url to use for this kickstart
                               'default' : use the system default URL
    rootpass(str)            - the root password to use in the kickstart
    """
    try:
        return rhn.session.kickstart.createProfileWithCustomUrl(rhn, kslabel, virttype, kstree, ksurl, rootpass) == 1
    except Exception, E:
        return rhn.fail(E, 'create kickstart %s with custom url %s' % (kslabel, ksurl))

# ---------------------------------------------------------------------------- #

def deleteProfile(rhn, kslabel):
    """
    API:
    kickstart.deleteProfile

    usage:
    deleteProfile(rhn, kslabel)

    description:
    delete an existing kickstart profile

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.deleteProfile(rhn.key, kslabel) == 1
    except Exception, E:
        return rhn.fail(E, 'Delete kickstart profile %s' % kslabel)

# ---------------------------------------------------------------------------- #

def importFile(rhn, kslabel, virttype, kstree, kscontent, kshost=None):
    """
    API:
    kickstart.importFile

    usage:
    importFile(rhn, kslabel, virttype, kstree, kscontent, kshost=None)

    description:
    Imports an existing kickstart file into the satellite.

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel(str)             - the kickstart profile label to create
    virttype(str)              - virtualization type, one of:
                               ['fully_virtualized', 'para_virtualized', 'none']
    kstree(str)              - kickstart tree label to be used
    kscontent(str)           - The kickstart file content.
    *kshost(str)             - the host to kickstart from. Overrides any 'method' statements in the content.
    """
    try:
        if kshost != None:
            return rhn.session.kickstart.importFile(rhn.key, kslabel, kshost, virttype, kstree, kscontent) == 1
        else:
            return rhn.session.kickstart.importFile(rhn.key, kslabel, virttype, kstree, kscontent) == 1
    except Exception, E:
        return rhn.fail(E, 'create kicktart profile %s' % kslabel)

# ---------------------------------------------------------------------------- #

def importRawFile(rhn, kslabel,virttype,kstree,kscontent):
    """
    API:
    kickstart.importRawFile

    usage:
    importRawFile(rhn, kslabel,virttype,kstree,kscontent)

    description:
    importRawFile(rhn, kslabel,virttype,kstree,kscontent)

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel(str)             - the kickstart profile label to create
    virttype(str)              - virtualization type, one of:
                               ['fully_virtualized', 'para_virtualized', 'none']
    kstree(str)              - kickstart tree label to be used
    kscontent(str)           - The kickstart file content.
    """
    try:
        return rhn.session.kickstart.importFile(rhn.key, kslabel, virttype, kstree, kscontent) == 1
    except Exception, E:
        return rhn.fail(E, 'import kickstart file into satellite')

# ---------------------------------------------------------------------------- #

def isProfileDisabled(rhn, kslabel):
    """
    API:
    kickstart.isProfileDisabled

    usage:
    isProfileDisabled(rhn, kslabel)

    description:
    returns True if profile is disabled

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel(str)             - kickstart profile label
    """
    try:
        return rhn.session.isProfileDisabled(rhn.key, kslabel)
    except Exception, E:        
        return rhn.fail(E, 'check if kickstart profile %s is disabled' % kslabel)

# ---------------------------------------------------------------------------- #

def listAllIpRanges(rhn):
    """
    API:
    kickstart.listAllIpRanges

    usage:
    listAllIpRanges(rhn)

    description:
    List all Ip Ranges and their associated kickstarts available in the user's org

    returns:
    list of dict

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.listAllIpRanges(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list all defined IP Ranges for your organisation')

# ---------------------------------------------------------------------------- #

def listKickstartableChannels(rhn):
    """
    API:
    kickstart.listKickstartableChannels

    usage:
    listKickstartableChannels(rhn)

    description:
    Lists the kickstartable channels for the logged-in user

    returns:
    list of dict, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.kickstart.listKickstartableChannels(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list kickstartable channels available to user %s' % rhn.login)

# ---------------------------------------------------------------------------- #

def listKsChannelNames(rhn):
    """
    API:
    none, special case of kickstart.listKickstartableChannels

    usage:
    listKsChannelNames(rhn)

    description:
    Lists the kickstartable channel labels for the current user

    returns:
    list of string (channel label)

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return sorted([ x['label'] for x in listKickstartableChannels(rhn) ])
    except Exception, E:
        return rhn.fail(E, 'list kickstartable channels available to user %s' % rhn.login)

# ---------------------------------------------------------------------------- #

def listKickstartableTrees(rhn, chanlabel):
    """
    API:
    kickstart.listKickstartableTrees

    usage:
    listKickstartableTrees(rhn, chanlabel)

    description:
    Lists the kickstartable trees for a given channel

    returns:
    list of dict, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    chanlabel                - a software channel label
    """
    try:
        return rhn.session.kickstart.listKickstartableTrees(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E, 'list kickstartable trees for channel %s' % chanlabel)

# ---------------------------------------------------------------------------- #

def listKsTreeNames(rhn, chanlabel):
    """
    API:
    none, special case of kickstart.listKickstartableTrees

    usage:
    listKsTreeNames(rhn, chanlabel)

    description:
    Lists the available kickstartable tree labels for a given channel

    returns:
    list of string (kickstart label)

    parameters:
    rhn                      - an authenticated RHN session
    chanlabel                - a software channel label
    """
    try:
        return sorted([ x['label'] for x in rhn.session.kickstart.listKickstartableTrees(rhn.key, chanlabel)])
    except Exception, E:
        return rhn.fail(E, 'list kickstartable trees for channel %s' % chanlabel)

# ---------------------------------------------------------------------------- #

def listKickstarts(rhn):
    """
    API:
    kickstart.listKickstarts

    usage: 
    listKickstarts(rhn)

    description:
    Lists the kickstart profiles on the satellite

    returns:
    list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    chanlabel                - a software channel label
    """
    try:
        return sorted(rhn.session.kickstart.listKickstarts(rhn.key), key=itemgetter('name'))
    except Exception, E:
        return  rhn.fail(E, 'list kickstarts on server %s' % rhn.hostname)

# ---------------------------------------------------------------------------- #

def renameProfile(rhn, kslabel, newlabel):
    """
    API:
    kickstart.renameProfile

    usage:
    renameProfile(rhn, kslabel, newlabel)

    description:
    renames a kickstart profile

    returns:
    Bool

    parameters:
    rhn                   - an authenticated rhn session
    kslabel              - Current label of the kickstart profile
    newlabel             - Desired new label for the kickstart profile
    """
    try:
        return rhn.session.kickstart.renameProfile(rhn.key, kslabel, newlabel) == 1
    except Exception, E:
        return rhn.fail(E, 'rename profile %s to %s' % (kslabel, newlabel))

# ------------------------ kickstart.filepreservation ------------------------ #

def createFilePreservation(rhn, fpname, filelist):
    """
    API:
    kickstart.filepreservation.create

    usage:
    createFilePreservation(rhn, fpname, filelist)

    description:
    Create a new named file preservation list

    returns:
    Bool
    
    parameters:
    rhn                   - an authenticated rhn session
    fpname(str)          - a name for the file preservation list
    filelist (list)      - a list file names
    """
    try:
        return rhn.session.kickstart.filepreservation.create(rhn.key, fpname, filelist) == 1
    except Exception, E:
        return rhn.fail(E,'create new file preservation %s containing files [%s]' % (fpname, ','.join(filelist)))

# ---------------------------------------------------------------------------- #

def deleteFilePreservation(rhn, fpname):
    """
    API:
    kickstart.filepreservation.delete

    usage:
    deleteFilePreservation(rhn, fpname)

    description:
    Delete a new named file preservation list

    returns:
    Bool
    
    parameters:
    rhn                   - an authenticated rhn session
    fpname(str)          - the named file preservation list to delete
    """
    try:
        return rhn.session.kickstart.filepreservation.delete(rhn.key, fpname) == 1
    except Exception, E:
        return rhn.fail(E,'delete file preservation %s' % fpname)

# ---------------------------------------------------------------------------- #

def listAllFilePreservations(rhn):
    """
    API:
    kickstart.filepreservation.listAllFilePreservations

    usage:
    listAllFilePreservations(rhn)

    description:
    List all defined file preservation lists

    returns:
    list of dict
    
    parameters:
    rhn                   - an authenticated rhn session
    """
    try:
        return rhn.session.kickstart.filepreservation.listAllFilePreservations(rhn.key)
    except Exception, E:
        return rhn.fail(E,'List file preservations')

# ---------------------------------------------------------------------------- #
def getFilePreservationDetails(rhn, fpname):
    """
    API:
    kickstart.filepreservation.getDetails

    usage:
    getFilePreservationDetails(rhn, fpname)

    description:
    Returns all of the data associated with the given file preservation list

    parameters:
    rhn                   - an authenticated rhn session
    fpname(str)           - file preservation list name  
    """
    try:
        return rhn.session.kickstart.filepreservation.getDetails(rhn, fpname)
    except Exception, E:
        return rhn.fail(E, 'get details for file preservation list %s' % fpname)
   
# ------------------------- kickstart.keys namespace ------------------------- #
# This namespace handles global GPG/SSL keys.
# methods renamed slightly to handle the clash with kickstart.profile.keys   

# ---------------------------------------------------------------------------- #

def createCryptoKey(rhn, keydesc, keytype, content):
    """
    API:
    kickstart.keys.create

    usage:
    createCryptoKey(rhn, keydesc, keytype, content)

    description:
    creates a new stored GPG or SSL key

    returns:
    Bool
    
    parameters:
    rhn                   - an authenticated rhn session
    keydesc(str)          - The key description
    keytype(str)          - one of ['GPG', 'SSL']
    content(str)          - the key itself
    """
    try:
        return rhn.session.kickstart.keys.create(rhn.key, keydesc, keytype, content) == 1
    except Exception, E:
        return rhn.fail(E,'create stored cryptokey %s' % keydesc)

# ---------------------------------------------------------------------------- #

def deleteCryptoKey(rhn, keydesc):
    """
    API:
    kickstart.keys.delete

    usage:
    deleteCryptoKey(rhn, keydesc)

    description:
    deletes a stored GPG or SSL key

    returns:
    Bool
    
    parameters:
    rhn                   - an authenticated rhn session
    keydesc               - The key description (or name)
    """
    try:
        return rhn.session.kickstart.keys.delete(rhn.key, keydesc) == 1
    except Exception, E:
        return rhn.fail(E,'delete crypto key %s' % keydesc)

# ---------------------------------------------------------------------------- #

def getCryptoKeyDetails(rhn, keydesc):
    """
    API:
    kickstart.keys.getDetails

    usage:
    getCryptoKeyDetails(rhn, keydesc)

    description:
    Get details for the given GPG or SSL key

    returns:
    dict
    
    parameters:
    rhn                   - an authenticated rhn session
    keydesc(str)          - The key description (or name)
    """
    try:
        return rhn.session.kickstart.keys.getDetails(rhn.key, keydesc)
    except Exception, E:
        return rhn.fail(E,'get details for key %s' % keydesc)

# ---------------------------------------------------------------------------- #

def listAllCryptoKeys(rhn):
    """
    API:
    kickstart.keys.listAllKeys

    usage:
    listAllCryptoKeys(rhn)

    description:
    List all stored crypto (GPG/SSL) keys

    returns:
    list of dict, one per key
    
    parameters:
    rhn                   - an authenticated rhn session
    """
    try:
        return rhn.session.kickstart.keys.listAllKeys(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list all GPG and SSL keys')

# ---------------------------------------------------------------------------- #

def updateCryptoKey(rhn, keydesc, keytype, keycontent):
    """
    API:
    kickstart.keys.update

    usage:
    updateCryptoKey(rhn, keydesc, keytype, keycontent)

    description:
    updates type and content of the specified key

    returns:
    Bool

    parameters:
    rhn                     - authenticated rhnapi session
    keydesc(str)            - Key description (name)
    keytype(str)            - Key Type (GPG or SSL)
    keycontent(str)         - the new key content
    """
    try:
        return rhn.session.kickstart.keys.update(rhn.key, keydesc, keytype, keycontent) == 1
    except Exception, E:
        return rhn.fail(E,'update %s key "%s"' %(keytype, keydesc))

# ----------------------- kickstart.profile namespace ------------------------ #

# kickstart.profile
##     * addIpRange
##     * addScript
##     * compareActivationKeys
##     * compareAdvancedOptions
##     * comparePackages
##     * downloadKickstart
##     * downloadRenderedKickstart
##     * getAdvancedOptions
##     * getChildChannels
##     * getCustomOptions
##     * getKickstartTree
##     * getVariables
##     * listIpRanges
##     * listScripts
##     * removeIpRange
##     * removeScript
##     * setAdvancedOptions
##     * setChildChannels
##     * setCustomOptions
##     * setKickstartTree
#     * setLogging
##     * setVariables

# ---------------------------------------------------------------------------- #

def addIpRange(rhn, kslabel, minip, maxip):
    """
    API:
    kickstart.profile.addIpRange

    usage:
    AddIpRangs(rhn, kslabel, minip, maxip)

    description:
    Adds a range of IP addresses to a given kickstart profile

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    minip                    - The first IP in the range being added
    maxip                    - The last IP in the range being added
    """
    try:
        return rhn.session.kickstart.profile.addIpRange(rhn.key, kslabel, minip, maxip) == 1
    except Exception, E:
        return rhn.fail(E, 'add iprange for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def addScript(rhn, kslabel, name, contents, scripttype, chroot = True, interpreter='', template = False):
    """
    API:
    kickstart.profile.addScript

    usage (* indicates optional parameters):
    AddScript(rhn, kslabel, contents, scripttype, *chroot, *interpreter, *template)

    description:
    Add a custom pre/post script to a kickstart profile

    returns:
    Bool 

    parameters (* = optional):
    rhn(rhnSession)          - an authenticated RHN session
    kslabel(str)             - The kickstart profile label in RHN satellite
    name(str)                - The script name.
    contents(str)            - The script content (e.g. from open(script).read())
    scripttype(str)          - 'pre' or 'post'
    *chroot(bool)             - does the script run chrooted (default: True)
    *interpreter(str)         - The Interpreter used to run the script. 
    *template(bool)           - enable cobbler templating in this script (default: False)
    """
    try:
        scriptid = rhn.session.kickstart.profile.addScript(rhn.key, kslabel, name, contents, interpreter, scripttype, chroot, template)
        return isinstance(scriptid, int)
    except Exception, E:
        return rhn.fail(E, 'Add kickstart %s script to kickstart %s' % (scripttype, kslabel))

# ---------------------------------------------------------------------------- #

def compareActivationKeys(rhn, kslabel1, kslabel2):
    """
    API:
    kickstart.profile.compareActivationKeys

    usage:
    compareActivationKeys(rhn, kslabel1, kslabel2)

    description:
    compare activation keys between 2 kickstarts

    returns:
    dict
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel1              - label of first kickstart profile
    kslabel2              - label of second kickstart profile
    """
    try:
        return rhn.session.kickstart.profile.compareActivationKeys(rhn.key,kslabel1, kslabel2)
    except Exception, E:
        return rhn.fail(E,'compare keys between channels %s adn %s' % (kslabel1, kslabel2))

# ---------------------------------------------------------------------------- #

def compareAdvancedOptions(rhn, kslabel1, kslabel2):
    """
    API:
    kickstart.profile.compareAdvancedOptions

    usage:
    compareAdvancedOptions(rhn, kslabel1, kslabel2)

    description:
    compare advanced options between 2 kickstarts

    returns:
    dict
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel1              - label of first kickstart profile
    kslabel2              - label of second kickstart profile
    """
    try:
        return rhn.session.kickstart.profile.compareAdvancedOptions(rhn.key,kslabel1, kslabel2)
    except Exception, E:
        return rhn.fail(E,'compare advanced opts between channels %s adn %s' % (kslabel1, kslabel2))

# ---------------------------------------------------------------------------- #

def comparePackages(rhn, kslabel1, kslabel2):
    """
    API:
    kickstart.profile.comparePackages

    usage:
    comparePackages(rhn, kslabel1, kslabel2)

    description:
    compare package lists between 2 kickstarts

    returns:
    dict
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel1              - label of first kickstart profile
    kslabel2              - label of second kickstart profile
    """
    try:
        return rhn.session.kickstart.profile.comparePackages(rhn.key,kslabel1, kslabel2)
    except Exception, E:
        return rhn.fail(E,'compare advanced opts between channels %s adn %s' % (kslabel1, kslabel2))

# ---------------------------------------------------------------------------- #

def downloadKickstart(rhn, kslabel, sathost):
    """
    API:
    kickstart.profile.downloadKickstart

    usage:
    downloadKickstart(rhn, kslabel, host)

    description:
    download the full contents of the chosen kickstart profile
    The 'sathost' parameter is the host to use when referring to
    the satellite itself (Usually this should be the FQDN of
    the satellite, but could be the ip address or shortname
    of it as well.

    This does not process any cobbler snippets, so if cobbler templating is in use, will
    simply contain a lot of '$SNIPPET' statements

    returns:
    string (the entire kickstart content)
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel(str)          - the kickstart label
    sathost(str)             - the satellite name (FQDN/hostname/ip)
    """
    try:
        return rhn.session.kickstart.profile.downloadKickstart(rhn.key, kslabel, sathost)
    except Exception, E:
        return rhn.fail(E,'download kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def downloadRenderedKickstart(rhn, kslabel):
    """
    API:
    kickstart.profile.downloadRenderedKickstart

    usage:
    downloadRenderedKickstart(rhn, kslabel)

    description:
    returns the cobbler-rendered kickstart file content, processing any variables
    or cobbler snippets.

    returns:
    string
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel(str)          - the kickstart label
    """
    try:
        return rhn.session.kickstart.profile.downloadRenderedKickstart(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E,'download kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def getAdvancedOptions(rhn, kslabel):
    """
    API:
    kickstart.profile.getAdvancedOptions

    usage:
    getAdvancedOptions(rhn, kslabel)

    description:
    Fetches advanced options from the satellite for a given kickstart

    returns:
    list of dicts, one per option ({'name' : optname, 'arguments' : optargs })

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.getAdvancedOptions(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get advanced opts for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def getChildChannels(rhn, kslabel):
    """
    API:
    kickstart.profile.getChildChannels

    usage:
    getchildChannels(rhn, kslabel)

    description:
    Fetches child channels from the satellite for a given kickstart

    returns:
    list of string (channel label)

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.getChildChannels(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get child channels for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def getCustomOptions(rhn, kslabel):
    """
    API:
    kickstart.profile.getCustomOptions

    usage:
    getCustomOptions(rhn, kslabel)

    description:
    Fetches custom options from the satellite for a given kickstart
    These are strings from the custom options box in the web interface
    The RHN Satellite API docs are incorrect on this subject

    returns:
    list of dict, one per custom option ({ 'name' : 'custom', 'arguments': optargs })
    each entry has the same 'name' ('custom').

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.getCustomOptions(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get custom opts for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def getKickstartTree(rhn, kslabel):
    """
    API:
    kickstart.profile.getKickstartTree

    usage:
    getCustomOptions(rhn, kslabel)

    description:
    Fetches kickstart tree from the satellite for a given kickstart

    returns:
    string (kstree label)

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.getKickstartTree(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get ks tree for kickstart %s' % kslabel)
        
# ---------------------------------------------------------------------------- #

def getVariables(rhn, kslabel):
    """
    API:
    kickstart.profile.getVariables

    usage:
    getVariables(rhn, kslabel)

    description:
    Fetches custom variables from the satellite for a given kickstart

    returns:
    dict, keyed on variable names

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.getVariables(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get custom variables for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def listIpRanges(rhn, kslabel):
    """
    API:
    kickstart.profile.listIpRanges

    usage:
    listIpRanges(rhn, kslabel)

    description:
    Lists the range of IP addresses for a given kickstart profile

    returns:
    list of dicts, one per IP Range ({ 'ksLabel' : label, 'min', 'max' })

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.listIpRanges(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get ip ranges for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def listScripts(rhn, kslabel):
    """
    API:
    kickstart.profile.listScripts

    usage:
    listScripts(rhn, kslabel)

    description:
    Fetches The custom %pre and %post scripts for a given kickstart

    returns:
    list of dict, one per script

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.listScripts(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'list scripts for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def removeIpRange(rhn, kslabel, ipaddress):
    """
    API:
    kickstart.profile.removeIpRange

    usage:
    removeIpRange(rhn, kslabel, ipaddress)

    description:
    Delete a new named file preservation list

    returns:
    True, or throws exception
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel(str)          - kickstart label 
    ipaddress(str)        - any ip address in the range you wish to remove
    """
    try:
        return rhn.session.kickstart.profile.removeIpRange(rhn.key, kslabel, ipaddress) == 1
    except Exception, E:
        return rhn.fail(E,'remove ip range containing %s from %s' %(ipaddress, kslabel))

# ---------------------------------------------------------------------------- #

def removeScript(rhn, kslabel, scriptid):
    """
    API:
    kickstart.profile.removeScript

    usage:
    removeScript(rhn, kslabel, scriptid)

    description:
    delete the script with id 'scriptid'
    
    returns:
    True, or throws exception
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel(str)          - kickstart label 
    scriptid(int)         - the script id number
    """
    try:
        return rhn.session.kickstart.profile.removeScript(rhn.key, kslabel, scriptid) == 1
    except Exception, E:
        return rhn.fail(E,'remove script id %d from kickstart %s' % (scriptid, kslabel))

# ---------------------------------------------------------------------------- #

def setAdvancedOptions(rhn, kslabel, optionlist):
    """
    API:
    kickstart.profile.setAdvancedOptions

    usage:
    setAdvancedOptions(rhn, kslabel, optionlist)

    description:
    sets advanced options from the satellite for the chosen kickstart profile
    You MUST provide a list containing the mandatory options

    Each dict in the options list has 2 keys:
    * string "name", one of
        [ autostep, interactive, install, upgrade, text, network,
        cdrom, harddrive, nfs, url, lang, langsupport keyboard,
        mouse, device, deviceprobe, zerombr, clearpart, bootloader,
        timezone, auth, rootpw, selinux, reboot, firewall, xconfig,
        skipx, key, ignoredisk, autopart, cmdline, firstboot, graphical
        iscsi, iscsiname, logging, monitor, multipath, poweroff, halt,
        service, shutdown, user, vnc, zfcp ]
    * string "arguments" - Arguments of the option

    REQUIRED OPTIONS (your list must include at least these)
    bootloader
    auth
    keyboard
    lang
    rootpw
    timezone


    returns:
    Bool

    parameters:
    rhn(rhnSession)          - an authenticated RHN session
    kslabel(str)             - The kickstart profile label in RHN satellite
    optionlist(list/dict)   - A list of dict, each representing a valid kickstart option.

    """
    try:
        return rhn.session.kickstart.profile.setAdvancedOptions(rhn.key, kslabel, optionlist) == 1
    except Exception, E:
        return rhn.fail(E, 'set advanced opts for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def setChildChannels(rhn, kslabel, chanlabels):
    """
    API:
    kickstart.profile.setChildChannels

    usage:
    setchildChannels(rhn, kslabel, chanlabels)

    description:
    Sets the list of child channels for the given kickstart label

    returns:
    Bool

    parameters:
    rhn                     - an authenticated RHN session
    kslabel                 - The kickstart profile label in RHN satellite
    chanlabels              - List of child channel labels to set
    """
    try:
        return rhn.session.kickstart.profile.setChildChannels(rhn.key, kslabel, chanlabels) == 1
    except Exception, E:
        return rhn.fail(E, 'set one or more of child channels %s for kickstart %s' % (','.join(chanlabels), kslabel))

# ---------------------------------------------------------------------------- #

def setCustomOptions(rhn, kslabel, optslist):
    """
    API:
    kickstart.profile.setCustomOptions

    usage:
    setCustomOptions(rhn, kslabel, optslist)

    Sets custom kickstart options (extra lines for the kickstart 'commands' section.
    e.g. $SNIPPET entries
    or anything else not covered in the 'Advanced Options' list
    Warning: broken kickstart instructions here will break the kickstart!

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    optionslist              - list of strings, each representing a line in the kickstart.
    """
    try:
        return rhn.session.kickstart.profile.setCustomOptions(rhn.key, kslabel, optslist) == 1
    except Exception, E:
        return rhn.fail(E, 'set custom opts for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def setKickstartTree(rhn, kslabel, kstreelabel):
    """
    API:
    kickstart.profile.setKickstartTree

    usage:
    setCustomOptions(rhn, kslabel, kstreelabel)

    description:
    Fetches kickstart tree from the satellite for a given kickstart

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    kstreelabel              - The kickstart tree label to set for this kickstart
    """
    try:
        return rhn.session.kickstart.profile.setKickstartTree(rhn.key, kslabel, kstreelabel) == 1
    except Exception, E:
        return rhn.fail(E, 'get ks tree for kickstart %s' % kslabel)

def setLogging(rhn, kslabel, log_pre=True, log_post=True):       
    """
    API:
    kickstart.profile.setLogging

    usage:
    setLogging(rhn, kslabel, log_pre=True, log_post=True)

    description:
    Enable logging of %pre and/or %post scripts to /root/ks-*log 
    for the given kickstart profile

    returns:
    True, or throws exception
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel(str)          - kickstart label 
    log_pre(bool)         - whether to log %pre scripts (True)
    log_post(bool)        - whether to log %post scripts (True)
    """
    try:
        return rhn.session.kickstart.profile.setLogging(rhn.key, kslabel, log_pre, log_post) == 1
    except Exception, E:
        return rhn.fail(E,'Enable logging for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def setVariables(rhn, kslabel, varlist):
    """
    API:
    kickstart.profile.setVariables

    usage:
    setVariables(rhn, kslabel)

    description:
    Fetches custom variables from the satellite for a given kickstart

    returns:
    Bool

    parameters:
    rhn(rhnSession)          - an authenticated RHN session
    kslabel(str)             - The kickstart profile label in RHN satellite
    varlist(list/dict)       - a list of key/value dicts for the variables you wish set.
    """
    try:
        return rhn.session.kickstart.profile.setVariables(rhn.key, kslabel, varlist) == 1
    except Exception, E:
        return rhn.fail(E, 'set custom variables for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

# -------------------------- kickstart.profile.keys -------------------------- #

def getActivationKeys(rhn, kslabel):
    """
    API:
    kickstart.profile.keys.getActivationKeys

    usage:
    getActivationKeys(rhn, kslabel)

    description:
    Fetches Activation keys from the satellite 
    that are used for a given kickstart

    returns:
    list of dicts, one per activation key

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.keys.getActivationKeys(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get activation keys for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def addActivationKey(rhn, kslabel, activationkey):
    """
    API:
    kickstart.profile.keys.addActivationKey

    usage:
    addActivationKey(rhn, kslabel, activationkey)

    description:
    Adds an activation key to a kickstart profile.
    The key must already exist in the satellite.

    returns:
    Bool

    parameters:
    rhn(rhnSession)          - an authenticated RHN session
    kslabel(str)             - The kickstart profile label in RHN satellite
    activationkey(str)       - The (already existing) activation key to add.
    """
    try:
        return rhn.session.kickstart.profile.keys.addActivationKey(rhn.key, kslabel, activationkey) == 1
    except Exception, E:
        return rhn.fail(E, 'add activation key %s to kickstart %s' % (activationkey, kslabel))

# ---------------------------------------------------------------------------- #

def removeActivationKey(rhn, kslabel, activationkey):
    """
    API:
    kickstart.profile.keys.removeActivationKey

    usage:
    removeActivationKey(rhn, kslabel, activationkey)

    description:
    Adds an activation key to a kickstart profile.
    The key must already exist in the satellite.

    returns:
    Bool

    parameters:
    rhn(rhnSession)          - an authenticated RHN session
    kslabel(str)             - The kickstart profile label in RHN satellite
    activationkey(str)       - The (already existing) activation key to remove.
    """
    try:
        return rhn.session.kickstart.profile.keys.removeActivationKey(rhn.key, kslabel, activationkey) == 1
    except Exception, E:
        return rhn.fail(E, 'remove activation key %s from kickstart %s' % (activationkey, kslabel))

# ---------------------------------------------------------------------------- #




# ------------------------ kickstart.profile.software ------------------------ #
def getSoftwareList(rhn, kslabel):
    """
    API:
    kickstart.profile.software.getSoftwareList

    usage:
    getSoftwareList(rhn, kslabel)

    description:
    Fetches the software list for a given kickstart label

    returns:
    string

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.software.getSoftwareList(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get custom opts for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def setSoftwareList(rhn, kslabel, swlist):
    """
    API:
    kickstart.profile.software.setSoftwareList

    usage:
    setSoftwareList(rhn, kslabel, swlist)

    description:
    sets the software list for a kickstart profile

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    swlist(list/str)         - List of package/group names(with @) to set as software list
    """
    try:
        return rhn.session.kickstart.profile.software.setSoftwareList(rhn.key, kslabel, swlist) == 1
    except Exception, E:
        return rhn.fail(E, 'set software list for kickstart %s' % kslabel)
        
# ---------------------------------------------------------------------------- #

def appendToSoftwareList(rhn, kslabel, swlist):
    """
    API:
    kickstart.profile.software.appendToSoftwareList

    usage:
    appendToSoftwareList(rhn, kslabel, swlist)

    description:
    appends packages to the software list for a kickstart profile

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    swlist(list/str)        - List of package/group names(with @) to set as software list
    """
    try:
        return rhn.session.kickstart.profile.software.appendToSoftwareList(rhn.key, kslabel, swlist) == 1
    except Exception, E:
        return rhn.fail(E, 'add packages to software list for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

# ------------------------ kickstart.profile.system: ------------------------- #
#     * addFilePreservations
#     * addKeys
#     * checkConfigManagement
#     * checkRemoteCommands
#     * disableConfigManagement
#     * disableRemoteCommands
#     * enableConfigManagement
#     * enableRemoteCommands
#     * getLocale
#     * getPartitioningScheme
#     * getRegistrationType
#     * getSELinux
#     * listFilePreservations
#     * listKeys
#     * removeFilePreservations
#     * removeKeys
#     * setLocale
#     * setPartitioningScheme
#     * setRegistrationType
#     * setSELinux

def addFilePreservations(rhn, kslabel, fplist):
    """
    API:
    kickstart.profile.system.addFilePreservations

    usage:
    addFilePreservations(rhn, kslabel, fplist)

    description:
    Adds a new list of file preservatiions to the given kickstart profile
    These are references to existing file preservation lists in satellite (not lists of filenames)

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    fplist(list/str)       - List of file preservation sets to add
    """
    try:
        return rhn.session.kickstart.profile.system.addFilePreservations(rhn.key, kslabel,fplist) == 1
    except Exception, E:
        return rhn.fail(E, 'set file preservation list %s for kickstart %s' % (','.join(fplist), kslabel))

# ---------------------------------------------------------------------------- #

def addCryptoKeys(rhn, kslabel, cryptokeys):
    """
    API:
    kickstart.profile.system.addKeys

    usage:
    addCryptoKeys(rhn, kslabel, keylist)

    description:
    Adds a list of GPG/SSL keys to the given kickstart profile
    The GPG/SSL keys must already exist in satellite.

    returns:
    True, or exception.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    cryptokeys(list/str)     - List of key descriptions (or a single key description)
    """
    if not isinstance(cryptokeys, list):
        cryptokeys = [cryptokeys]
    try:
        return rhn.session.kickstart.profile.system.addKeys(rhn.key, kslabel, cryptokeys) == 1
    except Exception, E:
        return rhn.fail(E, 'add GPG/SSL keys %s to kickstart %s' % (','.join(cryptokeys), kslabel))

# ---------------------------------------------------------------------------- #

def checkConfigManagement(rhn, kslabel):
    """
    API:
    kickstart.profile.system.checkConfigManagement

    usage:
    checkConfigManagement(rhn, kslabel)

    description:
    reports whether config management is enabled for the specified kickstart.
    Does not change any settings.

    returns:
    Bool
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.checkConfigManagement(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E,'check config management settings for %s' % kslabel)

# ---------------------------------------------------------------------------- #

def checkRemoteCommands(rhn, kslabel):
    """
    API:
    kickstart.profile.system.checkRemoteCommands

    usage:
    checkRemoteCommands(rhn, kslabel)

    description:
    reports whether remote commands are enabled for the chosen kickstart.
    Does not change any settings.

    returns:
    Bool
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.checkRemoteCommands(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E,'check if remote commands are enabled for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def disableConfigManagement(rhn, kslabel):
    """
    API:
    kickstart.profile.system.disableConfigManagement

    usage:
    disableConfigManagement(rhn, kslabel)

    description:
    disables config management for the specified kickstart

    returns:
    Bool
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.disableConfigManagement(rhn.key, kslabel) == 1
    except Exception, E:
        return rhn.fail(E,'disable config management settings for %s' % kslabel)

# ---------------------------------------------------------------------------- #

def disableRemoteCommands(rhn, kslabel):
    """
    API:
    kickstart.profile.system.disableRemoteCommands

    usage:
    disableRemoteCommands(rhn, kslabel)

    description:
    disables remote commands for the specified kickstart

    returns:
    Bool
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.disableRemoteCommands(rhn.key, kslabel) == 1
    except Exception, E:
        return rhn.fail(E,'disable remote commands for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def enableConfigManagement(rhn, kslabel):
    """
    API:
    kickstart.profile.system.enableConfigManagement

    usage:
    enableConfigManagement(rhn, kslabel)

    description:
    enable config management for the specified kickstart

    returns:
    Bool
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.enableConfigManagement(rhn.key, kslabel) == 1
    except Exception, E:
        return rhn.fail(E,'enable config management settings for %s' % kslabel)

# ---------------------------------------------------------------------------- #

def enableRemoteCommands(rhn, kslabel):
    """
    API:
    kickstart.profile.system.enableRemoteCommands

    usage:
    enableRemoteCommands(rhn, kslabel)

    description:
    enable remote commands for the specified kickstart

    returns:
    True or throws exception
    
    parameters:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.enableRemoteCommands(rhn.key, kslabel) == 1
    except Exception, E:
        return rhn.fail(E,'enable remote commands for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def getLocale(rhn, kslabel):
    """
    API:
    kickstart.profile.system.getLocale

    usage:
    getLocale(rhn, kslabel)

    description:
    Retrieves the locale for a kickstart profile. 

    returns:
    dict ( {'locale' : locale, 'useUtc' : bool } )

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.getLocale(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get locale info opts for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def getPartitioningScheme(rhn, kslabel):
    """
    API:
    kickstart.profile.system.getPartitioningScheme

    usage:
    getPartitioningScheme(rhn, kslabel)

    description:
    Fetches the partitioning commands from the given kickstart

    returns:
    string

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.getPartitioningScheme(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get custom opts for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def getRegistrationType(rhn, kslabel):
    """
    API:
    kickstart.profile.system.getRegistrationType

    usage:
    getRegistrationType(rhn, kslabel)

    description:
    Fetches the registration type
    Registration Type can be one of reactivation/deletion/none These types
    determine the behaviour of the registration when using this profile
    for reprovisioning

    returns:
    string ( one of ['reactivation', 'deletion', 'none' ])

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.getRegistrationType(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get registration type for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def getSELinux(rhn, kslabel):
    """
    API:
    kickstart.profile.system.getSELinux

    usage:
    getSELinux(rhn, kslabel)

    description:
    Reports SELinux status for the given kickstart

    returns:
    string (one of ['enforcing', 'permissive', 'disabled']

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.getSELinux(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get custom opts for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def listFilePreservations(rhn, kslabel):
    """
    API:
    kickstart.profile.system.listFilePreservations

    usage:
    listFilePreservations(rhn, kslabel)

    description:
    lists file preservations associated wth this kickstart

    returns:
    list of dict, one per file preservation list
     - {'name' : name, 'file_names' : list/string }

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.listFilePreservations(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'list file preservations lists for %s' % kslabel)

# ---------------------------------------------------------------------------- #

def listCryptoKeys(rhn, kslabel):
    """
    API:
    kickstart.profile.system.listKeys

    usage:
    listCryptoKeys(rhn, kslabel)

    description:
    Returns the set of GPG/SSL keys associated with the given kickstart profile.

    returns:
    list of dict, one per key (description, type, content)

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.listKeys(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'List GPG/SSL keys for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def removeFilePreservations(rhn, kslabel, fplist):
    """
    API:
    kickstart.profile.system.removeFilePreservations

    usage:
    removeFilePreservations(rhn, kslabel, fplist)

    description:
    removes a list of file preservations from the given kickstart profile

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    fplist(list/str)      - List of file preservation sets to remove
    """
    try:
        return rhn.session.kickstart.profile.system.removeFilePreservations(rhn.key, kslabel,fplist) == 1
    except Exception, E:
        return rhn.fail(E, 'set file preservation list %s for kickstart %s' % (','.join(fplist), kslabel))

# ---------------------------------------------------------------------------- #

def removeCryptoKeys(rhn, kslabel, cryptokeys):
    """
    API:
    kickstart.profile.system.removeKeys
    (renamed for consistency. And sanity.)

    usage:
    removeCryptoKeys(rhn, kslabel, cryptokeys)

    description:
    Adds a list of GPG/SSL keys to the given kickstart profile
    The GPG/SSL keys must already exist in satellite.

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    cryptokeys(list/str)     - Key description, or List of key descriptions
    """
    if not isinstance(cryptokeys, list):
        cryptokeys = [cryptokeys]
    try:
        return rhn.session.kickstart.profile.system.removeKeys(rhn.key, kslabel, cryptokeys)
    except Exception, E:
        return rhn.fail(E, 'remove keys %s from kickstart %s' % (','.join(cryptokeys), kslabel))

# ---------------------------------------------------------------------------- #

def setLocale(rhn, kslabel, locale, useUtc = False):
    """
    API:
    kickstart.profile.system.setLocale

    usage:
    setLocale(rhn, kslabel, locale, useUtc)

    description:
    sets the default locale for systems installing via the given ks profile.

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    locale(str)              - The Locale Entry (e.g. 'Europe/London')
    useUtc(bool)             - Whether the hardware clock is set to UTC or not (Def: False)
    """
    try:
        return rhn.session.kickstart.profile.system.setLocale(rhn.key, kslabel, locale, useUtc) == 1
    except Exception, E:
        return rhn.fail(E, 'set locale info opts for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def setPartitioningScheme(rhn, kslabel, partcmdlist):
    """
    API:
    kickstart.profile.system.setPartitioningScheme

    usage:
    setPartitioningScheme(rhn, kslabel, partcmdlist)

    description:
    sets the partitioning scheme for the given kickstart profile

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    partcmdlist(list/str)   - List of partitioning commands and their arguments
    """
    try:
        return rhn.session.kickstart.profile.system.setPartitioningScheme(rhn.key, kslabel, partcmdlist) == 1
    except Exception, E:
        return rhn.fail(E, 'set partitioning scheme for kickstart %s' % kslabel)

# ---------------------------------------------------------------------------- #

def setRegistrationType(rhn, kslabel, regtype):
    """
    API:
    kickstart.profile.system.setRegistrationType

    usage:
    setRegistrationType(rhn, kslabel, regtype)

    description:
    Sets the registration type for the specified kickstart profile
    Registration Type is one of ['reactivation', 'deletion', 'none' ]
    This determines the behaviour of the registration when using this
    profile for reprovisioning

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    regtype(str)             - one of ['reactivation', 'deletion', 'none']
    """
    try:
        return rhn.session.kickstart.profile.system.setRegistrationType(rhn.key, kslabel, regtype) == 1
    except Exception, E:
        return rhn.fail(E, 'set registration type %s for kickstart %s' % (regtype,kslabel ))

def setSELinux(rhn, kslabel, selinux_type):
    """
    API:
    kickstart.profile.system.setSELinux

    usage:
    setSELinux(rhn, kslabel)

    description:
    sets SELinux Status for the given kickstart

    returns:
    string (one of ['enforcing', 'permissive', 'disabled']

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    selinux_type(str)        - one of ['enforcing', 'permissive', 'disabled']
    """
    try:
        return rhn.session.kickstart.profile.system.setSELinux(rhn.key, kslabel, selinux_type) == 1
    except Exception, E:
        return rhn.fail(E, 'set SELinux to %s  for kickstart %s' % (selinux_type,kslabel))

# ---------------------------------------------------------------------------- #

# ---------------------------- kickstart.snippet ----------------------------- #

def createOrUpdateSnippet(rhn, snippetname, contents):
    """
    API:
    kickstart.snippet.createOrUpdate (renamed)

    usage:
    createOrUpdateSnippet(rhn, snippetname, contents)

    description:
    Creates (or replaces) an existing kickstart snippet

    returns:
    dict ( name(str), contents(str), fragment(str), file(str) )

    parameters:
    rhn                      - an authenticated RHN session
    snippetname(str)         - the snippet name
    contents(str)            - the snippet content
    """
    try:
        return rhn.session.kickstart.snippet.createOrUpdate(rhn.key, snippetname, contents)
    except Exception, E:
        return rhn.fail(E,'create/update snippet %s' % snippetname)

# ---------------------------------------------------------------------------- #

def deleteSnippet(rhn, snippetname):
    """
    API:
    kickstart.snippet.delete (renamed)

    usage:
    deleteSnippet(rhn, snippetname)

    description:
    deletes an existing snippet

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    snippetname(str)         - the snippet name
    """
    try:
        return rhn.session.kickstart.snippet.delete(rhn.key, snippetname) == 1
    except Exception, E:
        return rhn.fail(E,'delete snippet %s' % snippetname)

# ---------------------------------------------------------------------------- #

def listAllSnippets(rhn):
    """
    API:
    kickstart.snippet.listAll

    usage:
    listAllSnippets(rhn)

    description:
    Lists all cobbler snippets

    returns:
    list of dict, one per snippet

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.kickstart.snippet.listAll(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list all snippets')

def listCustomSnippets(rhn):
    """
    API:
    kickstart.snippet.listCustom

    usage:
    listCustomSnippets(rhn)

    description:
    Lists all custom cobbler snippets

    returns:
    list of dict, one per snippet

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.kickstart.snippet.listCustom(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list custom snippets')

# ---------------------------------------------------------------------------- #

def listDefaultSnippets(rhn):
    """
    API:
    kickstart.snippet.listDefault

    usage:
    listDefaultSnippets(rhn)

    description:
    Lists all default (rh-shipped) cobbler snippets

    returns:
    list of dict, one per snippet

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.kickstart.snippet.listDefault(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list all default snippets')

# ------------------------------ kickstart.tree ------------------------------ #

def createTree(rhn, treelabel, kstree_path, chanlabel, insttype):
    """
    API:
    kickstart.tree.create

    usage:
    createTree(rhn, treelabel, kstree_path, channellabel, insttype)

    description:
    Creates a new kickstart tree (cobbler distribution) and associates it
    with the specified channel label. (Used for making custom channels directly
    kickstartable)

    returns:
    Bool

    parameters:
    rhn                     - an authenticated RHN session
    treelabel(str)          - The new kickstart tree label.
    kstree_path(str)        - Path to the base or root of the kickstart tree.
    chanlabel(str)          - Label of channel to associate with the kickstart tree.
    insttype                - Label for KickstartInstallType (rhel_2.1, rhel_3, rhel_4, rhel_5, fedora_9). 
    """
    try:
        return rhn.session.kickstart.tree.create(rhn.key,treelabel, kstree_path, chanlabel, insttype) == 1
    except Exception, E:
        return rhn.fail(E, 'create new kickstart distribution %s' % treelabel)

# ---------------------------------------------------------------------------- #

def deleteTree(rhn, treelabel):
    """
    API:
    kickstart.tree.delete

    usage:
    deleteTree(rhn, treelabel)

    description:
    deletes the chosen kickstart tree/distribution

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    treelabel(str)          - The new kickstart tree label.
    """
    try:
        return rhn.session.kickstart.tree.delete(rhn.key,treelabel) == 1
    except Exception, E:
        return rhn.fail(E, 'delete kickstart distribution %s' % treelabel)

# ---------------------------------------------------------------------------- #

def getTreeDetails(rhn, treelabel):
    """
    API:
    kickstart.tree.getDetails

    usage: 
    getTreeDetails(rhn, treelabel)

    description:
    gets detailed info for the given kickstart tree/distribution

    returns:
    dict

    parameters:
    rhn                      - an authenticated RHN session
    treelabel(str)          - The new kickstart tree label.
    """
    try:
        return rhn.session.kickstart.tree.getDetails(rhn.key,treelabel)
    except Exception, E:
        return rhn.fail(E, 'get details for kickstart distribution %s' % treelabel)

# ---------------------------------------------------------------------------- #

def listTrees(rhn, chanlabel):
    """
    API:
    kickstart.tree.list

    usage:
    listTrees(rhn, chanlabel)

    description:
    Lists kickstart trees / distributions for the given channel

    returns:
    list of dict, one per tree.

    parameters:
    rhn                      - an authenticated RHN session
    chanlabel(str)          - channel label
    """
    try:
        return rhn.session.kickstart.tree.list(rhn.key,chanlabel)
    except Exception, E:
        return rhn.fail(E, 'list kickstartable trees for channel %s' % chanlabel)

# ---------------------------------------------------------------------------- #

def listInstallTypes(rhn):
    """
    API:
    kickstart.tree.listInstallTypes

    usage:
    listInstallTypes(rhn)

    description:
    Lists the install types available on the satellite server
    These can be used when creating kickstart trees / distros
    (e.g. rhel2,3,4,5,6 fedora9 etc)

    returns:
    list of dict, one per install type

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.kickstart.tree.listInstallTypes(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'List available install types')

# ---------------------------------------------------------------------------- #

def renameTree(rhn, treelabel, newlabel):
    """
    API:
    kickstart.tree.rename

    usage:
    renameTree(rhn, treelabel, newlabel)

    description:
    renames a kickstartable tree (distro)

    returns:
    Bool

    parameters:
    rhn                      - an authenticated RHN session
    treelabel               - the existing tree label
    newlabel                - the desired new label
    """
    try:
        return rhn.session.kickstart.tree.rename(rhn.key, treelabel, newlabel) == 1
    except Exception, E:
        return rhn.fail(E, 'rename tree %s to %s' %(treelabel, newlabel))

# ---------------------------------------------------------------------------- #

def updateTree(rhn, treelabel, treepath, chanlabel, insttype):
    """
    API:
    kickstart.tree.update

    usage:
    updateTree(rhn, treelabel, treepath, channellabel, insttype)

    description:
    updates an existing kickstart tree (cobbler distribution) and associates it
    with the specified channel label. (Used for making custom channels directly
    kickstartable)

    returns:
    Bool

    parameters:
    rhn                     - an authenticated RHN session
    treelabel(str)          - The new kickstart tree label.
    treepath(str)           - Path to the base or root of the kickstart tree.
    chanlabel(str)          - Label of channel to associate with the kickstart tree.
    insttype                - Label for KickstartInstallType (rhel_2.1, rhel_3, rhel_4, rhel_5, fedora_9). 
    """
    try:
        return rhn.session.kickstart.tree.update(rhn.key,treelabel, treepath, chanlabel, insttype) == 1
    except Exception, E:
        return rhn.fail(E, 'update kickstart distribution %s' % treelabel)
        
# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
