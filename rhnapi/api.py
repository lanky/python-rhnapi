#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the 'api' namespace
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

def getApiCallList(rhn):
    """
    API:
    api.getApiCallList

    usage:
    getApiCallList(rhn)

    description:
    Lists all available api calls grouped by namespace

    returns:
    list (dict)

    params:
    rhn               - authenticated rhnapi.rhnSession
    """
    try:
        return rhn.session.api.getApiCallList(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'unable to retrieve API call list')

def getApiNamespaceCallList(rhn, namespace):        
    """
    API:
    api.getApiNamespaceCallList

    usage:
    getApiNamespaceCallList(rhn, namespace)

    description:
    Lists all available api calls for the given namespace

    returns:
    list (dict)

    params:
    rhn               - authenticated rhnapi.rhnSession
    """
    try:
        return rhn.session.api.getApiNamespaceCallList(rhn.key, namespace)
    except Exception, E:
        return rhn.fail(E, 'get api calls for namespace %s' % namespace)

def getApiNamespaces(rhn):
    """
    API:
    api. getApiNamespaces

    usage:
    getApiNamespaces(rhn)

    description:
    Lists all available api namespaces

    returns:
    list (dict)

    params:
    rhn               - authenticated rhnapi.rhnSession
    """
    try:
        return rhn.session.api.getApiNamespaces(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'get api namespace list')

def getVersion(rhn):
    """
    API:
    api.getVersion

    usage:
    getVersion(rhn)

    description:
    returns the api version

    returns:
    string

    params:
    rhn               - authenticated rhnapi.rhnSession
    """
    return rhn.session.api.getVersion()


def systemVersion(rhn):
    """
    API:
    api.systemVersion

    usage:
    systemVersion(rhn)
    
    description:
    returns the spacewalk/satellite server version

    returns:
    string
    """
    return rhn.session.api.systemVersion()


# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
