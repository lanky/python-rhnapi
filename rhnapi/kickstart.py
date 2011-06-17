#!/usr/bin/env python
# -*- coding: utf-8 -*-
# an abstraction of the kickstart namespace from the RHN API for sat 5.1.0
# import as rhnapi.kickstart
# first, import container, which gives us the rhnSession object.

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
    usage: cloneProfile(rhn, kslabel)

    clone an existing kickstart pofile with a new name

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    clonela                  - The kickstart profile label for the new clone
    """
    try:
        return rhn.session.kickstart.cloneProfile(rhn.key, kslabel, clonelabel) == 1
    except Exception, E:
        return rhn.fail(E, 'clone kickstart profile %s as %s' % kslabel)

def createProfile(rhn, ksLabel, ksTree, rootPass, ksHost = '', vtType = 'none'):
    """
    usage: createProfile(rhn, ksLabel, vtType, kstree_label, ksHost, rootPass)

    Creates a new kickstart profile.

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    ksLabel(str)             - the kickstart profile label to create
    vtType(str)              - virtualization type, one of:
                               ['fully_virtualized', 'para_virtualized', 'none']
    ksTree(str)              - kickstart tree label to be used
    ksHost(str)              - the host to kicktart from.on
    rootPass(str)            - the root password to use in the kickstart
    """
    if ksHost == '':
        ksHost = rhn.hostname
    try:
        return rhn.session.kickstart.createProfile(rhn.key, ksLabel, vtType, ksTree, ksHost, rootPass) == 1
    except Exception, E:
        return rhn.fail(E, 'create new kickstart profile %s' % ksLabel)

def createProfileWithCustomUrl(rhn, ksLabel, vtType, ksTree, ksURL, rootPass):
    """
    usage: createProfileWithCustomUrl(rhn, ksLabel, vtType, ksTree, ksURL, rootPass)

    Lists the package filenames affected by a given erratum

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    ksLabel(str)             - the kickstart profile label to create
    vtType(str)              - virtualization type, one of:
                               ['fully_virtualized', 'para_virtualized', 'none']
    ksTree(str)              - kickstart tree label to be used
    ksURL(str)               - the custom url to use for this kickstart
                               'default' : use the system default URL
    rootPass(str)            - the root password to use in the kickstart
    """
    try:
        return rhn.session.kickstart.createProfileWithCustomUrl(rhn, ksLabel, vtType, ksTree, ksURL, rootPass) == 1
    except Exception, E:
        return rhn.fail(E, 'create kickstart %s with custom url %s' % (ksLabel, ksURL))

def deleteProfile(rhn, kslabel):
    """
    usage: deleteProfile(rhn, kslabel)

    delete an existing kickstart profile

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    clonela                  - The kickstart profile label for the new clone
    """
    try:
        return rhn.session.kickstart.deleteProfile(rhn.key, kslabel) == 1
    except Exception, E:
        return rhn.fail(E, 'Delete kickstart profile %s' % kslabel)

def importFile(rhn, ksLabel, vtType, ksTree, ksContent, ksHost=None):
    """
    usage: importFile(rhn, ksLabel, vtType, ksTree, ksContent, ksHost=None)

    Imports an existing kickstart file into the satellite.

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    ksLabel(str)             - the kickstart profile label to create
    vtType(str)              - virtualization type, one of:
                               ['fully_virtualized', 'para_virtualized', 'none']
    ksTree(str)              - kickstart tree label to be used
    ksContent(str)           - The kickstart file content.
    *ksHost(str)             - the host to kickstart from. Overrides any 'method' statements in the content.
    """
    try:
        if ksHost != None:
            rhn.session.kickstart.importFile(rhn.key, ksLabel, ksHost, vtType, ksTree, ksContent)
        else:
            rhn.session.kickstart.importFile(rhn.key, ksLabel, vtType, ksTree, ksContent)
    except Exception, E:
        return rhn.fail(E, 'create kicktart profile %s' % ksLabel)

def listKickstartableChannels(rhn):
    """
    usage: listKickstartableChannels(rhn)

    Lists the kickstartable channels for the logged-in user

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.kickstart.listKickstartableChannels(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list kickstartable channels for user %s' % rhn.login)

def listKsChannelNames(rhn):
    """
    usage: listKsChannelNames(rhn)

    Lists the kickstartable (labels only)

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    """
    return listKickstartableChannels(rhn)

def listKickstartableTrees(rhn, chanLabel):
    """
    usage: 

    Lists the kickstartable trees for a given channel

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    chanLabel                - a software channel label
    """
    return listKsTreeNames(rhn, chanLabel)

def listKsTreeNames(rhn, chanLabel):
    """
    usage: 

    Lists the kickstartable trees for a given channel

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    chanLabel                - a software channel label
    """
    try:
        return sorted([ x['label'] for x in rhn.session.kickstart.listKickstartableTrees(rhn.key, chanLabel)])
    except Exception, E:
        return rhn.fail(E, 'list kickstartable trees for channel %s' % chanLabel)

def listKickstarts(rhn):
    """
    usage: 

    Lists the kickstart profiles on the satellite

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    chanLabel                - a software channel label
    """
    try:
        return sorted(rhn.session.kickstart.listKickstarts(rhn.key), key=itemgetter('name'))
    except Exception, E:
        return  rhn.fail(E, 'list kickstarts on server %s' % rhn.hostname)

def renameProfile(rhn, ks_label, new_label) :
    """
    usage: renameProfile(rhn, profilelabel, newname)

    renames a kickstart profile

    returns: True, or throws exception 

    params:
    rhn                   - an authenticated rhn session
    ks_label              - Current label of the kickstart profile
    new_label             - Desired new label for the kickstart profile
    """
    try:
        return rhn.session.kickstart.renameProfile(rhn.key, ks_label, new_label) == 1
    except Exception, E:
        return rhn.fail(E, 'rename profile %s to %s' % (ks_label, new_label))


# kickstart.filepreservation
#     * create
#     * delete
#     * getDetails
#     * listAllFilePreservations

def createFilePreservation(rhn, fp_name, file_list):
    """
    usage : createFilePreservation(rhn, fp_name, file_list)

    Create a new named file preservation list

    returns: True, or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    fp_name(str)          - a name for the file preservation list
    file_list (list)      - a list file names
    """
    try:
        return rhn.session.kickstart.filepreservation.create(rhn.key, fp_name, file_list) == 1
    except Exception, E:
        return rhn.fail(E,'create new file preservation %s containing files [%s]' % (fp_name, ','.join(file_list)))

def deleteFilePreservation(rhn, fp_name):
    """
    usage : deleteFilePreservation(rhn, fp_name)

    Delete a new named file preservation list

    returns: True, or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    fp_name(str)          - the named file preservation list to delete
    """
    try:
        return rhn.session.kickstart.filepreservation.delete(rhn.key, fp_name) == 1
    except Exception, E:
        return rhn.fail(E,'delete file preservation %s' % fp_name)

def listAllFilePreservations(rhn):
    """
    usage : listAllFilePreservations(rhn)

    List all defined file preservation lists

    returns: list of dict
    
    params:
    rhn                   - an authenticated rhn session
    """
    try:
        return rhn.session.kickstart.filepreservation.listAllFilePreservations(rhn.key)
    except Exception, E:
        return rhn.fail(E,'List file preservations')
   
# kickstart.keys
#    * create
#    * delete
#    * getDetails
#    * listAllKeys
def createCryptoKey(rhn, keydesc, keytype, content):
    """
    usage : createCryptoKey(rhn, keydesc, type, content)

    creates a new stored GPG or SSL key

    returns: True, or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    keydesc(str)          - The key description
    keytype(str)          - one of ['GPG', 'SSL']
    content(str)          - the key itself
    """
    try:
        return rhn.session.kickstart.keys.create(rhn.key, keydesc, keytype, content) == 1
    except Exception, E:
        return rhn.fail(E,'create stored cryptokey %s' % keydesc)

def deleteCryptoKey(rhn, keydesc):
    """
    usage : deleteCryptoKey(rhn, keydesc)

    Delete a stored crypto key

    returns: True, or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    keydesc               - The key description (or name)
    """
    try:
        return rhn.session.kickstart.keys.delete(rhn.key, keydesc) == 1
    except Exception, E:
        return rhn.fail(E,'delete crypto key %s' % keydesc)

def getCryptoKeyDetails(rhn, keydesc):
    """
    usage : getCryptoKeyDetails(rhn, keydesc)

    Get details for the given GPG or SSL key

    returns: dict
    
    params:
    rhn                   - an authenticated rhn session
    keydesc(str)          - The key description (or name)
    """
    try:
        return rhn.session.kickstart.keys.getDetails(rhn.key, keydesc)
    except Exception, E:
        return rhn.fail(E,'get details for key %s' % keydesc)

def listAllCryptoKeys(rhn):
    """
    usage : listAllCryptoKeys(rhn)

    List all stored crypto (GPG/SSL) keys

    returns: list/dict
    
    params:
    rhn                   - an authenticated rhn session
    """
    try:
        return rhn.session.kickstart.keys.listAllKeys(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list all GPG and SSL keys')

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

def getAdvancedOptions(rhn, kslabel):
    """
    usage: getAdvancedOptions(rhn, kslabel)

    Fetches advanced options from the satellite for a given kickstart

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.getAdvancedOptions(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get advanced opts for kickstart %s' % kslabel)

def setAdvancedOptions(rhn, kslabel, option_list):
    """
    usage: setAdvancedOptions(rhn, kslabel, option_list)

    Fetches advanced options from the satellite for a given kickstart

    returns: True, or throws exception


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


    parameters:
    rhn(rhnSession)          - an authenticated RHN session
    kslabel(str)             - The kickstart profile label in RHN satellite
    option_list(list/dict)   - A list of dict, each representing a valid kickstart option.

    """
    try:
        return rhn.session.kickstart.profile.setAdvancedOptions(rhn.key, kslabel, option_list) == 1
    except Exception, E:
        return rhn.fail(E, 'set advanced opts for kickstart %s' % kslabel)

def getChildChannels(rhn, kslabel):
    """
    usage: getchildChannels(rhn, kslabel)

    Fetches child channels from the satellite for a given kickstart

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.getChildChannels(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get child channels for kickstart %s' % kslabel)

def setChildChannels(rhn, kslabel, child_channels):
    """
    usage: setchildChannels(rhn, kslabel, child_channels)

    Sets the list of child channels for the given kickstart label

    returns: True, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    child_channels           - List of child channel labels to set
    """
    try:
        return rhn.session.kickstart.profile.setChildChannels(rhn.key, kslabel, child_channels) == 1
    except Exception, E:
        return rhn.fail(E, 'set one or more of child channels %s for kickstart %s' % (','.join(child_channels), kslabel))

def getCustomOptions(rhn, kslabel):
    """
    usage: getCustomOptions(rhn, kslabel)

    Fetches custom options from the satellite for a given kickstart

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.getCustomOptions(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get custom opts for kickstart %s' % kslabel)

def setCustomOptions(rhn, kslabel, options_list):
    """
    usage: getCustomOptions(rhn, kslabel)

    Sets custom kickstart options (extra lines for the kickstart 'commands' section.
    e.g. $SNIPPET entries
    or anything else not covered in the 'Advanced Options' list

    returns: True or exception

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    options_list             - list of strings, each representing a line in the kickstart.
    """
    try:
        return rhn.session.kickstart.profile.setCustomOptions(rhn.key, kslabel, options_list) == 1
    except Exception, E:
        return rhn.fail(E, 'set custom opts for kickstart %s' % kslabel)

def getKickstartTree(rhn, kslabel):
    """
    usage: getCustomOptions(rhn, kslabel)

    Fetches kickstart tree from the satellite for a given kickstart

    returns: string (kstree label)

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.getKickstartTree(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get ks tree for kickstart %s' % kslabel)

def setKickstartTree(rhn, kslabel, kstree_label):
    """
    usage: setCustomOptions(rhn, kslabel, kstree_label)

    Fetches kickstart tree from the satellite for a given kickstart

    returns: True, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    kstree_label             - The kickstart tree label to set for this kickstart
    """
    try:
        return rhn.session.kickstart.profile.setKickstartTree(rhn.key, kslabel, kstree_label) == 1
    except Exception, E:
        return rhn.fail(E, 'get ks tree for kickstart %s' % kslabel)

def listIpRanges(rhn, kslabel):
    """
    usage: listIpRanges(rhn, kslabel)

    Lists the range of IP addresses for a given kickstart profile

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.listIpRanges(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get ip ranges for kickstart %s' % kslabel)

def addIpRange(rhn, kslabel, minip, maxip):
    """
    usage: AddIpRangs(rhn, kslabel, minip, maxip)

    Lists the range of IP addresses for a given kickstart profile

    returns: list of dicts, one per channel.

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

def listScripts(rhn, kslabel):
    """
    usage: listScripts(rhn, kslabel)

    Fetches The custom %pre and %post scripts for a given kickstart

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.listScripts(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'list scripts for kickstart %s' % kslabel)

def addScript(rhn, kslabel, contents, type, chroot = False, interpreter=''):
    """
    usage: AddScript(rhn, kslabel, contents, type, chroot = True, interpreter='')

    Add a custom script to a kickstart profile

    returns: Integer (script number) or errors

    parameters:
    rhn(rhnSession)          - an authenticated RHN session
    kslabel(str)             - The kickstart profile label in RHN satellite
    contents(str)            - The script content (e.g. from open(script).read())
    type(str)                - 'pre' or 'post'
    chroot(bool)             - does the script run chrooted (default: True)
    interpreter(str)         - The Interpreter used to run the script. leave blank for default.
    """
    try:
        return rhn.session.kickstart.profile.addScript(rhn.key, kslabel, contents, interpreter, type, chroot)
    except Exception, E:
        return rhn.fail(E, 'list scripts for kickstart %s' % kslabel)

def getVariables(rhn, kslabel):
    """
    usage: getVariables(rhn, kslabel)

    Fetches custom variables from the satellite for a given kickstart

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.getVariables(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get custom variables for kickstart %s' % kslabel)

def setVariables(rhn, kslabel, var_list):
    """
    usage: setVariables(rhn, kslabel)

    Fetches custom variables from the satellite for a given kickstart

    returns: True, or throws exception

    parameters:
    rhn(rhnSession)          - an authenticated RHN session
    kslabel(str)             - The kickstart profile label in RHN satellite
    var_list(list/dict)      - a list of key/value dicts for the variables you wish set.
    """
    try:
        return rhn.session.kickstart.profile.setVariables(rhn.key, kslabel, var_list) == 1
    except Exception, E:
        return rhn.fail(E, 'set custom variables for kickstart %s' % kslabel)

def compareActivationKeys(rhn, kslabel1, kslabel2):
    """
    usage : compareActivationKeys(rhn, kslabel1, kslabel2)

    compare activation keys between 2 kickstarts

    returns: dict
    
    params:
    rhn                   - an authenticated rhn session
    kslabel1              - label of first kickstart profile
    kslabel2              - label of second kickstart profile
    """
    try:
        return rhn.session.kickstart.profile.compareActivationKeys(rhn.key,kslabel1, kslabel2)
    except Exception, E:
        return rhn.fail(E,'compare keys between channels %s adn %s' % (kslabel1, kslabel2))


def compareAdvancedOptions(rhn, kslabel1, kslabel2):
    """
    usage : compareAdvancedOptions(rhn, kslabel1, kslabel2)

    compare advanced options between 2 kickstarts

    returns: dict
    
    params:
    rhn                   - an authenticated rhn session
    kslabel1              - label of first kickstart profile
    kslabel2              - label of second kickstart profile
    """
    try:
        return rhn.session.kickstart.profile.compareAdvancedOptions(rhn.key,kslabel1, kslabel2)
    except Exception, E:
        return rhn.fail(E,'compare advanced opts between channels %s adn %s' % (kslabel1, kslabel2))


def comparePackages(rhn, kslabel1, kslabel2):
    """
    usage : comparePackages(rhn, kslabel1, kslabel2)

    compare package lists between 2 kickstarts

    returns: dict
    
    params:
    rhn                   - an authenticated rhn session
    kslabel1              - label of first kickstart profile
    kslabel2              - label of second kickstart profile
    """
    try:
        return rhn.session.kickstart.profile.comparePackages(rhn.key,kslabel1, kslabel2)
    except Exception, E:
        return rhn.fail(E,'compare advanced opts between channels %s adn %s' % (kslabel1, kslabel2))

def downloadKickstart(rhn, kslabel, sathost):
    """
    usage : downloadKickstart(rhn, kslabel, host)

    download the full contents of the chosen kickstart profile
    The 'host' parameter is the host to use when referring to
    the satellite itself (Usually this should be the FQDN of
    the satellite, but could be the ip address or shortname
    of it as well.

    returns: string (kickstart with generated %post)
    
    params:
    rhn                   - an authenticated rhn session
    kslabel(str)          - the kickstart label
    host(str)             - the satellite name (FQDN/hostname/ip)
    """
    try:
        return rhn.session.kickstart.profile.downloadKickstart(rhn.key, kslabel, sathost)
    except Exception, E:
        return rhn.fail(E,'download kickstart %s' % kslabel)

def downloadRenderedKickstart(rhn, kslabel):
    """
    usage : downloadRenderedKickstart(rhn, kslabel)

    returns the cobbler-rendered kickstart file

    returns: string
    
    params:
    rhn                   - an authenticated rhn session
    kslabel(str)          - the kickstart label
    """
    try:
        return rhn.session.kickstart.profile.downloadRenderedKickstart(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E,'download kickstart %s' % kslabel)

def removeIpRange(rhn, kslabel, ipaddress):
    """
    usage : removeIpRange(rhn, kslabel, ipaddress)

    Delete a new named file preservation list

    returns: True, or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    kslabel(str)          - kickstart label 
    ipaddress(str)        - any ip address in the range you wish to remove
    """
    try:
        return rhn.session.kickstart.profile.removeIpRange(rhn.key, kslabel, ipaddress) == 1
    except Exception, E:
        return rhn.fail(E,'remove ip range containing %s from %s' %(ipaddress, kslabel))

def removeScript(rhn, kslabel, scriptid):
    """
    usage : removeScript(rhn, kslabel, scriptid)

    delete the script with id 'scriptid'
    
    returns: True, or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    kslabel(str)          - kickstart label 
    scriptid(int)         - the script id number
    """
    try:
        return rhn.session.kickstart.profile.removeScript(rhn.key, kslabel, scriptid) == 1
    except Exception, E:
        return rhn.fail(E,'remove script id %d from kickstart %s' % (scriptid, kslabel))

def setLogging(rhn, kslabel, log_pre=True, log_post=True):       
    """
    usage : setLogging(rhn, kslabel, log_pre=True, log_post=True)

    Enable logging of %pre and/or %post scripts to /root/ks-*log 
    for the given kickstart profile

    returns: True, or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    kslabel(str)          - kickstart label 
    log_pre(bool)         - whether to log %pre scripts (True)
    log_post(bool)        - whether to log %post scripts (True)
    """
    try:
        return rhn.session.kickstart.profile.setLogging(rhn.key, kslabel, log_pre, log_post) == 1
    except Exception, E:
        return rhn.fail(E,'Enable logging for kickstart %s' % kslabel)

# kickstart.profile.keys
#     * addActivationKey
#     * getActivationKeys
#     * removeActivationKey

def getActivationKeys(rhn, kslabel):
    """
    usage: getActivationKeys(rhn, kslabel)

    Fetches Activation keys from the satellite 
    that are used for a given kickstart

    returns: list of dicts, one per activation key

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.keys.getActivationKeys(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get activation keys for kickstart %s' % kslabel)

def addActivationKey(rhn, kslabel, activationkey):
    """
    usage: getActivationKeys(rhn, kslabel)

    Adds an activation key to a kickstart profile.
    The key must already exist in the satellite.

    returns: True, or exception.

    parameters:
    rhn(rhnSession)          - an authenticated RHN session
    kslabel(str)             - The kickstart profile label in RHN satellite
    activationkey(str)       - The (already existing) activation key to add.
    """
    try:
        return rhn.session.kickstart.profile.keys.addActivationKey(rhn.key, kslabel, activationkey) == 1
    except Exception, E:
        return rhn.fail(E, 'add activation key %s to kickstart %s' % (activationkey, kslabel))

def removeActivationKey(rhn, kslabel, activationkey):
    """
    usage: getActivationKeys(rhn, kslabel)

    Adds an activation key to a kickstart profile.
    The key must already exist in the satellite.

    returns: True, or exception.

    parameters:
    rhn(rhnSession)          - an authenticated RHN session
    kslabel(str)             - The kickstart profile label in RHN satellite
    activationkey(str)       - The (already existing) activation key to remove.
    """
    try:
        return rhn.session.kickstart.profile.keys.removeActivationKey(rhn.key, kslabel, activationkey) == 1
    except Exception, E:
        return rhn.fail(E, 'remove activation key %s from kickstart %s' % (activationkey, kslabel))


# kickstart.profile.software
#     * appendToSoftwareList
#     * getSoftwareList
#     * setSoftwareList

def getSoftwareList(rhn, kslabel):
    """
    usage: getSoftwareList(rhn, kslabel)

    Fetches the software list for a given kickstart label

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.software.getSoftwareList(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get custom opts for kickstart %s' % kslabel)

def setSoftwareList(rhn, kslabel, sw_list):
    """
    usage: setSoftwareList(rhn, kslabel, sw_list)

    sets the software list for a kickstart profile

    returns: True, or errors

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    sw_list(list/str)        - List of package/group names(with @) to set as software list
    """
    try:
        return rhn.session.kickstart.profile.software.setSoftwareList(rhn.key, kslabel, sw_list) == 1
    except Exception, E:
        return rhn.fail(E, 'set software list for kickstart %s' % kslabel)
        
def appendToSoftwareList(rhn, kslabel, sw_list):
    """
    usage: appendToSoftwareList(rhn, kslabel, sw_list)

    appends packages to the software list for a kickstart profile

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    sw_list(list/str)        - List of package/group names(with @) to set as software list
    """
    try:
        return rhn.session.kickstart.profile.software.appendToSoftwareList(rhn.key, kslabel, sw_list) == 1
    except Exception, E:
        return rhn.fail(E, 'add packages to software list for kickstart %s' % kslabel)

# items from kickstart.profile.system:
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


def getLocale(rhn, kslabel):
    """
    usage: getLocale(rhn, kslabel)

    Retrieves the locale for a kickstart profile. 

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.getLocale(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get locale info opts for kickstart %s' % kslabel)

def setLocale(rhn, kslabel, locale, useUtc = False):
    """
    usage: setLocale(rhn, kslabel, locale, useUtc)

    sets the default locale for systems installing via the given ks profile.


    returns: list of dicts, one per channel.

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

def getPartitioningScheme(rhn, kslabel):
    """
    usage: getPartitioningScheme(rhn, kslabel)

    Fetches the partitioning commands from the given kickstart

    returns: string

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.getPartitioningScheme(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get custom opts for kickstart %s' % kslabel)

def setPartitioningScheme(rhn, kslabel, partcmd_list):
    """
    usage: setPartitioningScheme(rhn, kslabel, partcmd_list)

    sets the partitioning scheme for the given kickstart profile

    returns: True, or exception

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    partcmd_list(list/str)   - List of partitioning commands and their arguments
    """
    try:
        return rhn.session.kickstart.profile.system.setPartitioningScheme(rhn.key, kslabel, partcmd_list) == 1
    except Exception, E:
        return rhn.fail(E, 'set partitioning scheme for kickstart %s' % kslabel)

def getRegistrationType(rhn, kslabel):
    """
    usage: getRegistrationType(rhn, kslabel)

    Fetches the registration type
    Registration Type can be one of reactivation/deletion/none These types
    determine the behaviour of the registration when using this profile
    for reprovisioning

    returns: string ( one of ['reactivation', 'deletion', 'none' ])

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.getRegistrationType(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get registration type for kickstart %s' % kslabel)

def setRegistrationType(rhn, kslabel, regtype):
    """
    usage: setRegistrationType(rhn, kslabel, regtype)

    Sets the registration type for this kickstart profile
    Registration Type can be one of reactivation/deletion/none These types
    determine the behaviour of the registration when using this profile
    for reprovisioning

    returns: True, or exception

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    regtype(str)             - one of ['reactivation', 'deletion', 'none']
    """
    try:
        return rhn.session.kickstart.profile.system.setRegistrationType(rhn.key, kslabel, regtype) == 1
    except Exception, E:
        return rhn.fail(E, 'set registration type %s for kickstart %s' % (regtype,kslabel ))

def getSELinux(rhn, kslabel):
    """
    usage: getSELinux(rhn, kslabel)

    Fetches SELinux Status for the given kickstart

    returns: string (one of ['enforcing', 'permissive', 'disabled']

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.getSELinux(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'get custom opts for kickstart %s' % kslabel)

def setSELinux(rhn, kslabel, selinux_type):
    """
    usage: setSELinux(rhn, kslabel)

    sets SELinux Status for the given kickstart

    returns: string (one of ['enforcing', 'permissive', 'disabled']

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    selinux_type(str)        - one of ['enforcing', 'permissive', 'disabled']
    """
    try:
        return rhn.session.kickstart.profile.system.setSELinux(rhn.key, kslabel, selinux_type) == 1
    except Exception, E:
        return rhn.fail(E, 'set SELinux to %s  for kickstart %s' % (selinux_type,kslabel))

def addFilePreservations(rhn, kslabel, file_list):
    """
    usage: addFilePreservations(rhn, kslabel, file_list)

    Adds a new list of file preservatiions to the given kickstart profile

    returns: True, or exception

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    file_list(list/str)      - List of file preservation sets to add
    """
    try:
        return rhn.session.kickstart.profile.system.addFilePreservations(rhn.key, kslabel,file_list) == 1
    except Exception, E:
        return rhn.fail(E, 'set file preservation list %s for kickstart %s' % (','.join(file_list), kslabel))

def listFilePreservations(rhn, kslabel):
    """
    usage: listFilePreservations(rhn, kslabel)

    lists file preservations associated wth this kickstart

    returns: list/dict

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.listFilePreservations(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'list file preservations lists for %s' % kslabel)

def removeFilePreservations(rhn, kslabel, file_list):
    """
    usage: removeFilePreservations(rhn, kslabel, file_list)

    removes a list of file preservations from the given kickstart profile

    returns: True, or exception

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    file_list(list/str)      - List of file preservation sets to remove
    """
    try:
        return rhn.session.kickstart.profile.system.removeFilePreservations(rhn.key, kslabel,file_list) == 1
    except Exception, E:
        return rhn.fail(E, 'set file preservation list %s for kickstart %s' % (','.join(file_list), kslabel))

def listCryptoKeys(rhn, kslabel):
    """
    usage: listCryptoKeys(rhn, kslabel)

    Returns the set of GPG/SSL keys associated with the given kickstart profile.

    returns: list of dicts, one per key

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    """
    try:
        return rhn.session.kickstart.profile.system.listKeys(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E, 'List GPG/SSL keys for kickstart %s' % kslabel)

def addCryptoKeys(rhn, kslabel, cryptokeys):
    """
    usage: addCryptoKeys(rhn, kslabel, key_list)

    Adds a list of GPG/SSL keys to the given kickstart profile
    The GPG/SSL keys must already exist in satellite.

    returns: True, or exception.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    cryptokeys(list/str)     - List of key descriptions (or a single key description)
    """
    if not isinstance(cryptokeys, list):
        cryptokeys = [cryptokeys]
    try:
        return rhn.session.kickstart.profile.system.addKeys(rhn.key, kslabel, cryptokeys)
    except Exception, E:
        return rhn.fail(E, 'add GPG/SSL keys %s to kickstart %s' % (','.join(cryptokeys), kslabel))

def removeKeys(rhn, kslabel, cryptokeys):
    """
    usage: removeKeys(rhn, kslabel, key_list)

    Adds a list of GPG/SSL keys to the given kickstart profile
    The GPG/SSL keys must already exist in satellite.

    returns: True, or exception.

    parameters:
    rhn                      - an authenticated RHN session
    kslabel                  - The kickstart profile label in RHN satellite
    crtptokeys(list/str      - Key description, or List of key descriptions
    """
    if not isinstance(cryptokeys, list):
        cryptokeys = [cryptokeys]
    try:
        return rhn.session.kickstart.profile.system.removeKeys(rhn.key, kslabel, cryptokeys)
    except Exception, E:
        return rhn.fail(E, 'remove keys %s from kickstart %s' % (','.join(cryptokeys), kslabel))

def checkConfigManagement(rhn, kslabel):
    """
    usage : checkConfigManagement(rhn, kslabel)

    check if config management is enabled for this kickstart

    returns: True/False or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.checkConfigManagement(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E,'check config management settings for %s' % kslabel)

def enableConfigManagement(rhn, kslabel):
    """
    usage : enableConfigManagement(rhn, kslabel)

    enable config management for this kickstart

    returns: True/False or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.enableConfigManagement(rhn.key, kslabel) == 1
    except Exception, E:
        return rhn.fail(E,'enable config management settings for %s' % kslabel)

def disableConfigManagement(rhn, kslabel):
    """
    usage : disableConfigManagement(rhn, kslabel)

    disable config management for this kickstart

    returns: True/False or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.disableConfigManagement(rhn.key, kslabel) == 1
    except Exception, E:
        return rhn.fail(E,'disable config management settings for %s' % kslabel)

def checkRemoteCommands(rhn, kslabel):
    """
    usage : checkRemoteCommands(rhn, kslabel)

    check if remote commands are enabled for this kickstart

    returns: True/False or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.checkRemoteCommands(rhn.key, kslabel)
    except Exception, E:
        return rhn.fail(E,'check if remote commands are enabled for kickstart %s' % kslabel)

def enableRemoteCommands(rhn, kslabel):
    """
    usage : enableRemoteCommands(rhn, kslabel)

    enable remote commands for this kickstart

    returns: True or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.enableRemoteCommands(rhn.key, kslabel) == 1
    except Exception, E:
        return rhn.fail(E,'enable remote commands for kickstart %s' % kslabel)

def disableRemoteCommands(rhn, kslabel):
    """
    usage : disableRemoteCommands(rhn, kslabel)

    disable remote commands for this kickstart

    returns: True/False or throws exception
    
    params:
    rhn                   - an authenticated rhn session
    kslabel               - kickstart label
    """
    try:
        return rhn.session.kickstart.profile.system.disableRemoteCommands(rhn.key, kslabel) == 1
    except Exception, E:
        return rhn.fail(E,'disable remote commands for kickstart %s' % kslabel)

########## --------------------------------- #########
# kickstart.snippet
#     * createOrUpdate
#     * delete
#     * listAll
#     * listCustom
#     * listDefault
def createOrUpdateSnippet(rhn, snippetname, contents):
    """
    usage: createOrUpdateSnippet(rhn, snippetname, contents)

    Creates (or replaces) an existing kickstart snippet

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    snippetname(str)         - the snippet name
    contents(str)            - the snippet content
    """
    try:
        return rhn.session.kickstart.snippet.createOrUpdate(rhn.key, snippetname, contents)
    except Exception, E:
        return rhn.fail(E,'create/update snippet %s' % snippetname)

def deleteSnippet(rhn, snippetname):
    """
    usage: deleteSnippet(rhn, snippetname)

    deletes an existing snippet

    returns: True, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    snippetname(str)         - the snippet name
    """
    try:
        return rhn.session.kickstart.snippet.delete(rhn.key, snippetname) == 1
    except Exception, E:
        return rhn.fail(E,'delete snippet %s' % snippetname)

def listAllSnippets(rhn):
    """
    usage: listAllSnippets(rhn)

    Lists all cobbler snippets

    returns: list of dicts, one per snippet

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.kickstart.snippet.listAll(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list all snippets')

def listCustomSnippets(rhn):
    """
    usage: listCustomSnippets(rhn)

    Lists all custom cobbler snippets

    returns: list of dicts, one per snippet

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.kickstart.snippet.listCustom(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list custom snippets')

def listDefaultSnippets(rhn):
    """
    usage: listDefaultSnippets(rhn)

    Lists all default (rh-shipped) cobbler snippets

    returns: list of dicts, one per snippet

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.kickstart.snippet.listDefault(rhn.key)
    except Exception, E:
        return rhn.fail(E,'list all default snippets')
# kickstart.tree
#     * create
#     * delete
#     * deleteTreeAndProfiles
#     * getDetails
#     * list
#     * listInstallTypes
#     * rename
#     * update

def createTree(rhn, tree_label, kstree_path, chan_label, inst_type):
    """
    usage: createTree(rhn, tree_label, kstree_path, channel_label, inst_type)

    Creates a new kickstart tree (cobbler distribution) and associates it
    with the specified channel label. (Used for making custom channels directly
    kickstartable)

    returns: True, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    tree_label(str)          - The new kickstart tree label.
    kstree_path(str)         - Path to the base or root of the kickstart tree.
    chan_label(str)          - Label of channel to associate with the kickstart tree.
    inst_type                - Label for KickstartInstallType (rhel_2.1, rhel_3, rhel_4, rhel_5, fedora_9). 
    """
    try:
        return rhn.session.kickstart.tree.create(rhn.key,tree_label, kstree_path, chan_label, inst_type) == 1
    except Exception, E:
        return rhn.fail(E, 'create new kickstart distribution %s' % tree_label)

def deleteTree(rhn, tree_label):
    """
    usage: deleteTree(rhn, tree_label)

    deletes the chosen kickstart tree/distribution

    returns: True, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    tree_label(str)          - The new kickstart tree label.
    """
    try:
        return rhn.session.kickstart.tree.delete(rhn.key,tree_label) == 1
    except Exception, E:
        return rhn.fail(E, 'delete kickstart distribution %s' % tree_label)

def getTreeDetails(rhn, tree_label):
    """
    usage: 

    gets detailed info for the given kickstart tree/distribution

    returns: dict

    parameters:
    rhn                      - an authenticated RHN session
    tree_label(str)          - The new kickstart tree label.
    """
    try:
        return rhn.session.kickstart.tree.getDetails(rhn.key,tree_label)
    except Exception, E:
        return rhn.fail(E, 'get details for kickstart distribution %s' % tree_label)

def listTrees(rhn, chan_label):
    """
    usage: listTrees(rhn, chan_label)

    Lists kickstart trees / distributions for the given channel

    returns: list of dicts, one per tree.

    parameters:
    rhn                      - an authenticated RHN session
    chan_label(str)          - channel label
    """
    try:
        return rhn.session.kickstart.tree.list(rhn.key,chan_label)
    except Exception, E:
        return rhn.fail(E, 'list kickstartable trees for channel %s' % chan_label)

def listInstallTypes(rhn):
    """
    usage: listInstallTypes(rhn)

    Lists the install types available on the satellite server
    (which can be used when creating kickstart trees / distros)

    returns: list of dicts, one per channel.

    parameters:
    rhn                      - an authenticated RHN session
    """
    try:
        return rhn.session.kickstart.tree.listInstallTypes(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'List available install types')

def renameTree(rhn, tree_label, new_label):
    """
    usage: renameTree(rhn, tree_label, new_label)

    renames a kickstartable tree (distro)

    returns: True, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    tree_label               - the existing tree label
    new_label                - the desired new label
    """
    try:
        return rhn.session.kickstart.tree.rename(rhn.key, tree_label, new_label) == 1
    except Exception, E:
        return rhn.fail(E, 'rename tree %s to %s' %(tree_label, new_label))

def updateTree(rhn, tree_label, kstree_path, chan_label, inst_type):
    """
    usage: updateTree(rhn, tree_label, kstree_path, channel_label, inst_type)

    updates an existing kickstart tree (cobbler distribution) and associates it
    with the specified channel label. (Used for making custom channels directly
    kickstartable)

    returns: True, or throws exception

    parameters:
    rhn                      - an authenticated RHN session
    tree_label(str)          - The new kickstart tree label.
    kstree_path(str)         - Path to the base or root of the kickstart tree.
    chan_label(str)          - Label of channel to associate with the kickstart tree.
    inst_type                - Label for KickstartInstallType (rhel_2.1, rhel_3, rhel_4, rhel_5, fedora_9). 
    """
    try:
        return rhn.session.kickstart.tree.update(rhn.key,tree_label, kstree_path, chan_label, inst_type) == 1
    except Exception, E:
        return rhn.fail(E, 'update kickstart distribution %s' % tree_label)
