#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An abstraction of the rhnapi.distchannel namespace.
This is part of the rhnapi module and most methods will
require an authenticated RHN session fron rhnapi.rhnSession
to actually do anything.
"""
def listDefaultMaps(rhn):
    """
    Lists all default distribution channel maps
    params:
    rhn                   - an authenticated rhn session
    """
    try:
        return rhn.session.distchannel.listDefaultMaps(rhn.key)
    except Exception, E:
        return rhn.fail(E,'List default distribution channel maps')

def setDefaultMap(rhn, os, release, arch_label, channel_label):
    """
    usage: setDefaultMap(rhn, channel_label)

    sets a default distribution channel for the given OS

    returns: True or exception

    params:
    rhn                   - an authenticated rhn session
    os                    - Operating System
    release               - Release version
    arch_label            - Channel Architecture
    channel_label         - Channel Label to add as a map
    """

    try:
        return rhn.session.distchannel.setDefaultMap(rhn.key, os, release, arch_label, channel_label) == 1
    except Exception, E:
        return rhn.fail(E,'add distchannel map')

def removeDefaultMap(rhn, os, release, arch_label):
    """
    usage: setDefaultMap(rhn, channel_label)

    sets a default distribution channel for the given OS

    returns: True or exception

    params:
    rhn                   - an authenticated rhn session
    os                    - Operating System
    release               - Release version
    arch_label            - Channel Architecture
    """

    try:
        return rhn.session.distchannel.setDefaultMap(rhn.key, os, release, arch_label, channel_label='') == 1
    except Exception, E:
        return rhn.fail(E,'remove distchannel map')




