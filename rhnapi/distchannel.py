#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the distchannel namespace.
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

__doc__ = """
An abstraction of the rhnapi.distchannel namespace.
This is part of the rhnapi module and most methods will
require an authenticated RHN session fron rhnapi.rhnSession
to actually do anything.
"""
__author__ = "Stuart Sears"

def listDefaultMaps(rhn):
    """
    API:
    distchannel.listDefaultMaps

    usage:
    listDefaultMaps(rhn)

    description:
    Lists all default distribution channel maps

    parameters:
    rhn                   - an authenticated rhn session
    """
    try:
        return rhn.session.distchannel.listDefaultMaps(rhn.key)
    except Exception, E:
        return rhn.fail(E,'List default distribution channel maps')

def setDefaultMap(rhn, os, release, archlabel, chanlabel):
    """
    API:
    distchannel.setDefaultMap

    usage:
    setDefaultMap(rhn, os, release, archlabel, chanlabel)

    description:
    sets a default distribution channel for the given OS

    returns:
    Bool

    params:
    rhn                     - an authenticated rhn session
    os(str)                 - Operating System
    release(str)            - Release version
    archlabel(str)         - Channel Architecture
    chanlabel(str)      - Channel Label to add as a map
    """

    try:
        return rhn.session.distchannel.setDefaultMap(rhn.key, os, release, archlabel, chanlabel) == 1
    except Exception, E:
        return rhn.fail(E,'add distchannel map')

def removeDefaultMap(rhn, os, release, archlabel):
    """
    API:
    none, custom version of setDefaultMap

    usage:
    setDefaultMap(rhn, chanlabel)

    description:
    sets a default distribution channel for the given OS

    returns:
    Bool

    params:
    rhn                     - an authenticated rhn session
    os(str)                 - Operating System
    release(str)            - Release version
    archlabel(str)         - Channel Architecture
    """

    try:
        return rhn.session.distchannel.setDefaultMap(rhn.key, os, release, archlabel, channelLabel='') == 1
    except Exception, E:
        return rhn.fail(E,'remove distchannel map')

# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
