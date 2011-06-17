#!/usr/bin/env python
# -*- coding: utf-8 -*-
# an abstraction of the configchannel API from RHN.
# based on RHN Satellite 5.1.0
# updated for RHN Satellite 5.4.0

# channelExists 
# create 
# createOrUpdatePath 
# createOrUpdateSymlink 
# deleteChannels 
# deleteFiles 
# deployAllSystems 
# deployAllSystems 
# getDetails 
# getDetails 
# listFiles 
# listGlobals 
# listSubscribedSystems 
# lookupChannelInfo 
# lookupFileInfo 
# scheduleFileComparisons 
# update 
# --------------
#
# def create(rhn, channel_label, channel_name, channel_desc):
# def createConfigChannel(rhn, channel_label, channel_name, channel_desc):
# def deleteConfigChannels(rhn, channel_list):
# def deleteConfigChannel(rhn, channel_label):
# def updateConfigChannel(rhn, channel_label, channel_name, channel_desc):
# def detailsByID(rhn, channel_id):
# def detailsByLabel(rhn, channel_label):
# def createPath(rhn, channel_label, path, isdir=False, content='', owner='root', group='root', permissions='', macro_start='', macro_end=''):
# def updatePath(rhn,channel_label,file_path, isdir=False, content=None, permissions=None, macro_start=None, macro_end=None):
# def deletePaths(rhn, channel_label, path_list):
# def deletePath(rhn, channel_label, path):
# def getPathInfo(rhn, channel_label, path_list):
# def getChannelInfo(rhn, channel_list):
# def listGlobalChannels(rhn):

def channelExists(rhn, channel_label):
    """
    Checks whether a given configuration channel label exists
    """
    try:
        return rhn.session.configchannel.channelExists(rhn.key, channel_label) == 1
    except Exception, E:
        return rhn.fail(E, 'Check for existence of config channel %s' % channel_label)

def create(rhn, channel_label, channel_name, channel_desc):
    """
    wrapper around createConfigChannel
    """
    return  createConfigChannel(rhn, channel_label, channel_name, channel_desc)

def createConfigChannel(rhn, channel_label, channel_name, channel_desc):
    """
    API: configchannel.create

    usage: createConfigChannel(rhn, channel_label, channel_name, channel_desc)

    returns: dict (the new config channel object)
    
    description:
    Creates a new Configuration Channel

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    channel_name(str)       - channel name
    channel_desc(str)       - channel label to merge into
    """
    try:
        return rhn.session.configchannel.create(rhn.key, channel_label, channel_name, channel_desc)
    except Exception, E:
        return rhn.fail(E, 'create new configuration channel %s' %(channel_label))

def deleteConfigChannels(rhn, channel_list):
    """
    API: configchannel.deleteChannels

    usage: deleteConfigChannels(rhn, channel_list)

    returns: bool, or throws exception

    description:
    Deletes a list of existing Configuration Channels

    parameters:
    rhn                     - an authenticated RHN session.
    channel_list(list)      - list of channel labels
    """
    try:
        return rhn.session.configchannel.deleteChannels(rhn.key, channel_list) == 1
    except Exception, E:
        return rhn.fail(E, 'delete configuration channels %s' %(','.join(channel_list) ) )

def deleteConfigChannel(rhn, channel_label):
    """
    usage: deleteConfigChannel(rhn, channel_label)

    Deletes an existing Configuration Channel

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    """
    return deleteConfigChannels(rhn, [channel_label])

def updateConfigChannel(rhn, channel_label, channel_name, channel_desc):
    """
    usage: updateConfigChannel(rhn, label, name, description)

    Updates an existing Configuration Channel

    returns: dict containing updated information.

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    channel_name(str)       - channel name
    channel_desc(str)       - channel label to merge into
    """
    try:
        return rhn.session.configchannel.update(rhn.key, channel_label, channel_name, channel_desc) 
    except Exception, E:
        return rhn.fail(E, 'update configuration channel %s' %(channel_label))

def detailsByID(rhn, channel_id):
    """
    usage: detailsByID(rhn, channel_id)

    Shows Config Channel information based on a channel ID

    parameters:
    rhn                     - an authenticated RHN session.
    channel_id(int)         - channel ID number
    """
    try:
        return rhn.session.configchannel.getDetails(rhn.key, channel_id)
    except Exception, E:
        return rhn.fail(E, 'get info for configuration channel %d' %(channel_id) )

def getDetails(rhn, channel_label):
    """
    Wrapper around detailsByLabel (which is how most people will call this)
    """
    return detailsByLabel(rhn, channel_label)

def detailsByLabel(rhn, channel_label):
    """
    usage: detailsByLabel(rhn, channel_label)

    Shows Config Channel information based on a channel label.

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    """
    try:
        return rhn.session.configchannel.getDetails(rhn.key, channel_label)
    except Exception, E:
        return rhn.fail(E, 'get info for configuration channel %s' %(channel_label) )

def createOrUpdatePath(rhn, label, path, directory = False, **kwargs):
    """
    usage: createOrUpdatePath(rhn, label, path, directory, **kwargs)

    Creates a new Path (file or directory) in a config channel

    returns: bool, or throws exception (depends on RHN debug setting)

    parameters (* = optional)
    rhn                     - an authenticated RHN session.
    channel_label(str)      - which channel the path belongs to
    path(str)               - the absolute path on the target system, including filename.
    isdir(bool)             - this is a directory, not a file
    plus a selection of the following key=value arguments. (*=optional)
    owner(str)              - the owner of the file once deployed.
    group(str)              - the group associated with the file once deployed.
    permissions(str)        - octal permissions for the deployed file (e.g. 0644)
    * contents(str)         - the contents of the file (ignored for directories)
                              while this will work without content, it's not the best idea.
    * contents_enc64(bool)  - contents are base64 encoded (for binary files)
    * context(str)          - SELinux context
    * macro_start(str)      - string used to indicate beginning of macro expressions. Leave empty for default
    * macro_end(str)        - string used to indicate the end of macro expressions. Leave empty for default.
    * revision(int)         - revison of updated file (auto-incremented)
    """
    try:
        return isinstance(rhn.session.configchannel.createOrUpdatePath(rhn.key, channel_label, path, directory, kwargs), dict)
    except Exception, E:
        return rhn.fail(E, 'create or update path %s in channel %s with structure %s' %(path, channel_label, str(kwargs)))

def createOrUpdateObject(rhn, channel_label, objinfo):
    """
    API: configchannel.createOrUpdatePath

    usage: createOrUpdateObject(rhn, label, objinfo)

    description:
    As createOrUpdatePath, but takes a dict structure as a parameter instead
    handles files, directories or symlinks appropriately

    This was written to handle the output of export-configchannel.py, which has a lot of detail in it
    that the normal creation api calls do not expect.

    parameters
    rhn(rhnapi.rhnSession)      - authenticated RHN API session
    channel_label(str)          - the label of the (already existing) configuration channel
                                  you wish to add this object to
    objinfo(dict)               - object information (dict), 

    contents(str)               - Contents of the file (ignored for directories)
    contents_enc64(bool)        - Identifies base64 encoded content (default: false)
    owner(str)                  - Owner of the file/directory.
    group(str)                  - Group name of the file/directory.
    permissions                 - Octal file/directory permissions (eg: 644)
    selinux_ctx                 - SELinux Security context (optional)
    macro-start-delimiter       - Config file macro start delimiter. (ignored if working with a directory)
    macro-end-delimiter         - Config file macro end delimiter. Use null or empty string to accept the default. (ignored if working with a directory)
    * int "revision" - next revision number, auto increment for null
    """
    # strip out the stuff that we can't use
    for key in  [  'binary', 'channel', 'modified', 'md5', 'permissions_mode', 'creation' ]:
        if objinfo.has_key(key):
            del objinfo[key]

    # returns int, but expects string. Seriously?
    if objinfo.get('permissions') is not None:
        objinfo['permissions'] = str(objinfo['permissions'])
    
    if objinfo.has_key('path'):
        path = objinfo['path']
        del objinfo['path']
    
    if objinfo.get('type') == 'symlink':
        del objinfo['type']
        try:
            return rhn.session.configchannel.createOrUpdateSymlink(rhn.key, channel_label, path, objinfo)
        except Exception, E:
            return rhn.fail(E, 'create/update symbolic link %s' % path)
    else:
        ftype = objinfo.get('type', 'file')
        del objinfo['type']
        isDir = ftype == 'directory'
        
        try:
            return rhn.session.configchannel.createOrUpdatePath(rhn.key, channel_label, path, isDir, objinfo)
        except Exception, E:
            return rhn.fail(E, 'create/update %s %s' %(ftype ,path))


def createOrUpdateSymlink(rhn, channel_label, path, **kwargs):
    """
    usage: createOrUpdateSymlink(rhn, channel_label, path, isdir=False, content='', owner, group, permissions='', macro_start='', macro_end='')

    Creates or Updates a new Symlink (file or directory) in a config channel

    returns: dict showing path information

    parameters (*=optional)
    rhn                     - an authenticated RHN session.
    channel_label(str)      - which channel the path belongs to
    plus one or more key-value pairs as follows:
    target_path(str)        - the absolute path to the symlink's target
    *context(str)           - SELinux context for the symlink
    *revision(int)          - revison of updated file 
    """
    try:
        return isinstance(rhn.session.configchannel.createOrUpdatePath(rhn.key, channel_label,path, kwargs), dict)
    except Exception, E:
        return rhn.fail(E, 'create or update path %s in channel %s with parameters %s' %(path, channel_label, str(kwargs)))

def deletePaths(rhn, channel_label, path_list):
    """
    usage: deletePaths(rhn, channel_label, path_list)

    Delete a list of paths from a configuration channel

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    path_list               - a list of paths to delete
    """
    try:
        return rhn.session.configchannel.deleteFiles(rhn.key, channel_label, path_list)
    except Exception, E:
        return rhn.fail(E, 'delete files from configuration channel %s' %(channel_label))

def deletePath(rhn, channel_label, path):
    """
    usage: deletePath(rhn, channel_label, path)

    Delete an individual paths from a configuration channel

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - channel label
    path_list               - a list of paths to delete
    """
    return deletePaths(rhn, channel_label, [path])

def getPathInfo(rhn, channel_label, path_list):
    """
    usage: getPathInfo(rhn, channel_label, file_list)

    Shows information about a list of files/dirs in a config channel

    returns: list of dicts, one per path.
    
    parameters:
    rhn                     - an authenticated RHN session.
    label(str)              - channel label
    path_list(list/str)     - list of paths to report
    description(str)        - channel label to merge into
    """
    try:
        return rhn.session.configchannel.lookupFileInfo(rhn.key, channel_label, path_list)
    except Exception, E:
        return rhn.fail(E, 'find path information in %s' %(channel_label))

def lookupFileInfo(rhn, channel_label, path_list):
    return getPathInfo(rhn, channel_label, path_list)

def getChannelInfo(rhn, channel_list):
    """
    usage: getChannelInfo(rhn, channel_list)

    Look up information about configuration channels

    parameters:
    rhn                     - an authenticated RHN session.
    channel_list(list/str)  - list of channel labels
    """
    if not isinstance(channel_list, list):
        channel_list = [ channel_list ]
    try:
        return rhn.session.configchannel.lookupChannelInfo(rhn.key, channel_list)
    except Exception, E:
        return rhn.fail(E, 'look up channel information')

def lookupChannelInfo(rhn, channel_list):
    return getChannelInfo(rhn, channel_list)

def listGlobalChannels(rhn):
    """
    usage: listGlobalChannels(rhn)

    Lists globally subscribable config channels

    returns: list of dicts, one per channel.

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.configchannel.listGlobals(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list global configuration channels')

def listGlobals(rhn):
    return listGlobalChannels(rhn)

def listFiles(rhn, channel_label):
    """
    usage: listFiles(rhn, channel_list)

    Look up information about configuration channels

    parameters:
    rhn                     - an authenticated RHN session.
    channel_label(str)      - list of channel labels
    """
    try:
        return rhn.session.configchannel.listFiles(rhn.key, channel_label)
    except Exception, E:
        return rhn.fail(E, 'get file list for channel %s' % channel_label)
