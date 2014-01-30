#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the configchannel namespace
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


# --------------------------------------------------------------------------------- #

def channelExists(rhn, chanlabel):
    """
    API:
    configchannel.channelExists

    usage:
    channelExists(rhn, chanlabel)

    description:
    Checks whether a given configuration channel label exists

    returns:
    bool

    parameters:
    rhn                     - authenticated rhn session object
    chanlabel(str)          - configuration channel label
    """
    try:
        return rhn.session.configchannel.channelExists(rhn.key, chanlabel) == 1
    except Exception, E:
        return rhn.fail(E, 'Check for existence of config channel %s' % chanlabel)

# --------------------------------------------------------------------------------- #

def createConfigChannel(rhn, chanlabel, channame, chandesc):
    """
    wrapper around createConfigChannel for backwards compatibility with older scripts
    """
    return  create(rhn, chanlabel, channame, chandesc)

# --------------------------------------------------------------------------------- #

def create(rhn, chanlabel, channame, chandesc):
    """
    API:
    config.create

    usage:
    createConfigChannel(rhn, chanlabel, channame, chandesc)

    description:
    Creates a new Configuration Channel

    returns:
    dict (the new config channel object)

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - channel label
    channame(str)           - channel name
    chandesc(str)           - channel label to merge into
    """
    try:
        return rhn.session.configchannel.create(rhn.key, chanlabel, channame, chandesc)
    except Exception, E:
        return rhn.fail(E, 'create new configuration channel %s' %(chanlabel))

# --------------------------------------------------------------------------------- #

def deleteConfigChannels(rhn, chanlist):
    """
    alias for deleteChannels (script compat)
    """
    return deleteChannels(rhn, chanlist)

# --------------------------------------------------------------------------------- #

def deleteChannels(rhn, chanlist):
    """
    API:
    configchannel.deleteChannels

    usage:
    deleteConfigChannels(rhn, chanlist)

    description:
    Deletes a list of existing Configuration Channels

    returns:
    bool, or throws exception

    parameters:
    rhn                     - an authenticated RHN session.
    chanlist(list)          - list of channel labels
    """
    try:
        return rhn.session.configchannel.deleteChannels(rhn.key, chanlist) == 1
    except Exception, E:
        return rhn.fail(E, 'delete configuration channels %s' %(','.join(chanlist) ) )

# --------------------------------------------------------------------------------- #

def deleteConfigChannel(rhn, chanlabel):
    """
    API:
    
    usage:
    deleteConfigChannel(rhn, chanlabel)

    Deletes an existing Configuration Channel

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - channel label
    """
    return deleteConfigChannels(rhn, [chanlabel])

# --------------------------------------------------------------------------------- #

def delete(rhn, chanspec):
    """
    API:
    none, custom wrapper around deleteChannel(s)
    
    usage:
    delete(rhn, chanlabel) OR
    delete(rhn, [ chanlabel1, chanlabel2,...])

    description:
    deletes the specified channel or channels

    parameters:
    rhn                     - an authenticated RHN session.
    chanspec(str)           - channel label
    OR
    chanspec(list of str)   - list of channel labels
    """
    if isinstance(chanspec, str):
        chanlist = [ chanspec ]
    elif isinstance(chanspec, list):
        chanlist = chanspec
    return deleteChannels(rhn, chanlist)       

# --------------------------------------------------------------------------------- #

def update(rhn, chanlabel, channame, chandesc):
    """
    API:
    configchannel.update

    usage:
    updateConfigChannel(rhn, label, name, description)

    description:
    Updates an existing Configuration Channel

    returns:
    dict containing updated information.

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - channel label
    channame(str)           - channel name
    chandesc(str)           - channel label to merge into
    """
    try:
        return rhn.session.configchannel.update(rhn.key, chanlabel, channame, chandesc) 
    except Exception, E:
        return rhn.fail(E, 'update configuration channel %s' %(chanlabel))

def updateConfigChannel(rhn, chanlabel, channame, chandesc):
    """
    wrapper around configchannel.update for backwards compat with scripts.
    """
    return update(rhn, chanlabel, channame, chandesc)
    

# --------------------------------------------------------------------------------- #

def detailsByID(rhn,  chanid):
    """
    usage: detailsByID(rhn,  chanid)

    Shows Config Channel information based on a channel ID

    parameters:
    rhn                     - an authenticated RHN session.
     chanid(int)            - channel ID number
    """
    try:
        return rhn.session.configchannel.getDetails(rhn.key,  chanid)
    except Exception, E:
        return rhn.fail(E, 'get info for configuration channel %d' %( chanid) )

def getDetails(rhn, chanspec):
    """
    API:
    configchannel.getDetails

    usage:
    getDetails(rhn, chanspec)

    description:
    gets detailed configuration channel information

    returns:
    dict

    parameters:
    rhn                     - an authenticated RHN session.
    chanspec(str/int)       - channel label or channel ID
    """
    try:
        return rhn.session.configchannel.getDetails(rhn.key, chanspec)
    except Exception, E:
        return rhn.fail(E, 'get details for channel %r' % chanspec)

# --------------------------------------------------------------------------------- #

def detailsByLabel(rhn, chanlabel):
    """
    usage: detailsByLabel(rhn, chanlabel)

    Shows Config Channel information based on a channel label.

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - channel label
    """
    try:
        return rhn.session.configchannel.getDetails(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E, 'get info for configuration channel %s' %(chanlabel) )

# --------------------------------------------------------------------------------- #

def createOrUpdatePath(rhn, chanlabel, path, directory=False, **kwargs):
    """
    API:
    custom implementation of the 
    configchannel.createOrUpdatePath API using optional args

    usage:
    createOrUpdatePath(rhn, label, path, directory, **kwargs)

    description:
    Creates a new Path (file or directory) in a config channel

    returns:
    bool, or throws exception (depends on RHN debug setting)

    parameters (* = optional)
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - which channel the path belongs to
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
        return isinstance(rhn.session.configchannel.createOrUpdatePath(rhn.key, chanlabel, path, directory, kwargs), dict)
    except Exception, E:
        return rhn.fail(E, 'create or update path %s in channel %s with structure %s' %(path, chanlabel, str(kwargs)))

# --------------------------------------------------------------------------------- #

def createOrUpdateObject(rhn, chanlabel, objinfo):
    """
    API:
    configchannel.createOrUpdatePath

    usage:
    createOrUpdateObject(rhn, label, objinfo)

    description:
    As createOrUpdatePath, but takes a dict structure as a parameter instead
    handles files, directories or symlinks appropriately

    This was written to handle the output of spw_export_configchannel, which has a lot of detail in it
    that the normal creation api calls do not expect.

    parameters
    rhn(rhnapi.rhnSession)  - authenticated RHN API session
    chanlabel(str)          - the label of the (already existing) configuration channel
                              you wish to add this object to
    objinfo(dict)           - object information (dict), 

    contents(str)           - Contents of the file (ignored for directories)
    contents_enc64(bool)    - Identifies base64 encoded content (default: false)
    owner(str)              - Owner of the file/directory.
    group(str)              - Group name of the file/directory.
    permissions             - Octal file/directory permissions (eg: 644)
    selinux_ctx             - SELinux Security context (optional)
    macro-start-delimiter   - Config file macro start delimiter. (ignored if working with a directory)
    macro-end-delimiter     - Config file macro end delimiter. Use null or empty string to accept the default. (ignored if working with a directory)
    * int "revision"        - next revision number, auto increment for null
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
            return rhn.session.configchannel.createOrUpdateSymlink(rhn.key, chanlabel, path, objinfo)
        except Exception, E:
            return rhn.fail(E, 'create/update symbolic link %s' % path)
    else:
        ftype = objinfo.get('type', 'file')
        del objinfo['type']
        isDir = ftype == 'directory'
        
        try:
            return rhn.session.configchannel.createOrUpdatePath(rhn.key, chanlabel, path, isDir, objinfo)
        except Exception, E:
            return rhn.fail(E, 'create/update %s %s' %(ftype ,path))


# --------------------------------------------------------------------------------- #

def createOrUpdateSymlink(rhn, chanlabel, path, **kwargs):
    """
    API:
    configchannel.createOrUpdateSymlink

    usage:
    createOrUpdateSymlink(rhn, chanlabel, path, isdir=False, content='', owner, group, permissions='', macro_start='', macro_end='')

    description:
    Creates or Updates a new Symlink (file or directory) in a config channel

    returns:
    dict showing path information

    parameters (*=optional):
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - which channel the path belongs to

    plus one or more key-value pairs as follows:
    target_path(str)        - the absolute path to the symlink's target
    *context(str)           - SELinux context for the symlink
    *revision(int)          - revison of updated file 
    """
    try:
        return isinstance(rhn.session.configchannel.createOrUpdateSymlink(rhn.key, chanlabel,path, kwargs), dict)
    except Exception, E:
        return rhn.fail(E, 'create or update symlink %s in channel %s with parameters %s' %(path, chanlabel, str(kwargs)))

# ---------------------------------------------------------------------------- #

def deleteFiles(rhn, chanlabel, pathlist):
    """
    API:
    configchannel.deleteFiles

    usage:
    deletePaths(rhn, chanlabel, pathlist)

    description:
    Delete a list of paths from a configuration channel

    returns:
    bool

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - channel label
    pathlist(list of str)   - a list of paths to delete
    """
    try:
        return rhn.session.configchannel.deleteFiles(rhn.key, chanlabel, pathlist) == 1
    except Exception, E:
        return rhn.fail(E, 'delete files from configuration channel %s' %(chanlabel))

# ---------------------------------------------------------------------------- #

def deleteFile(rhn, chanlabel, path):
    """
    API:
    custom method, special case of configchannel.deleteFiles

    usage:
    deletePath(rhn, chanlabel, path)

    description:
    Delete an individual paths from a configuration channel

    returns:
    bool

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - channel label
    pathlist(list of str)   - a list of paths to delete
    """
    return deleteFiles(rhn, chanlabel, [path])

# --------------------------------------------------------------------------------- #

def lookupFileInfo(rhn, chanlabel, pathlist):
    """
    API:
    configchannel.lookupFileInfo

    usage:
    lookupFileInfo(rhn, chanlabel, pathlist)

    description:
    Shows information about a list of files/dirs in a config channel

    returns:
    list of dicts, one per path.
    
    parameters:
    rhn                     - an authenticated RHN session.
    label(str)              - channel label
    pathlist(list/str)      - list of paths to report
    description(str)        - channel label to merge into
    """
    try:
        return rhn.session.configchannel.lookupFileInfo(rhn.key, chanlabel, pathlist)
    except Exception, E:
        return rhn.fail(E, 'find path information in %s' %(chanlabel))
        
# --------------------------------------------------------------------------------- #

def getFileInfo(rhn, chanlabel, pathlist):       
    """
    special case of lookupFileInfo for the sake of commonsense naming.
    """
    return lookupFileInfo(rhn, chanlabel, pathlist)

# --------------------------------------------------------------------------------- #

def getPathInfo(rhn, chanlabel, pathlist):
    """
    alias for lookupFileInfo for backwards compat with scripts.
    """
    return lookupFileInfo(rhn, chanlabel, pathlist)

# --------------------------------------------------------------------------------- #

def lookupChannelInfo(rhn, chanlist):
    """
    API:
    configchannel.lookupChannelInfo

    usage:
    lookupChannelInfo(rhn, chanlist)

    description:
    Look up information about configuration channels

    returns:
    list of dict

    parameters:
    rhn                     - an authenticated RHN session.
    chanlist(list/str)      - list of channel labels
    """
    if not isinstance(chanlist, list):
        chanlist = [ chanlist ]
    try:
        return rhn.session.configchannel.lookupChannelInfo(rhn.key, chanlist)
    except Exception, E:
        return rhn.fail(E, 'look up channel information')

# --------------------------------------------------------------------------------- #

def getChannelInfo(rhn, chanlist):
    return lookupChannelInfo(rhn, chanlist)

# --------------------------------------------------------------------------------- #

def listGlobals(rhn):
    """
    API:
    configchannel.listGlobals

    usage:
    listGlobalChannels(rhn)

    description:
    Lists globally subscribable config channels

    returns:
    list of dict, one per channel.

    parameters:
    rhn                     - an authenticated RHN session.
    """
    try:
        return rhn.session.configchannel.listGlobals(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list global configuration channels')

# --------------------------------------------------------------------------------- #

def listGlobalChannels(rhn):
    return listGlobals(rhn)

# --------------------------------------------------------------------------------- #

def listFiles(rhn, chanlabel):
    """
    API:
    configchannel.listFiles

    usage:
    listFiles(rhn, chanlabel)

    description:
    Look up information about configuration channels

    returns:
    list of dict

    parameters:
    rhn                     - an authenticated RHN session.
    chanlabel(str)          - list of channel labels
    """
    try:
        return rhn.session.configchannel.listFiles(rhn.key, chanlabel)
    except Exception, E:
        return rhn.fail(E, 'get file list for channel %s' % chanlabel)

# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
