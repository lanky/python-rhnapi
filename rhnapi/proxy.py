#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module
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
rhnapi.proxy

Abstraction of the 'proxy' namespeace in the RHN Satelite API
updated for satellite v 5.4

These calls all take an argument of 'syscert' which is the content of
a syscert file - open('/etc/sysconfig/rhn/syscert').read() should do.

This suggests that they are only useful when run from a system that is
* intended to become an RHN proxy
* already is a registered RHN proxy
"""

__author__ = "Stuart Sears"

def activateProxy(rhn, syscert, proxyver):
	"""
    API:
    proxy.activateProxy

	usage:
    activateProxy(rhn, syscert, proxyver)

    description:
	Activates a system as an RHN proxy server, using
	the given syscert file and proxy version

	returns:
    Bool, or throws exception

	params:
	rhn                     - an authenticated RHN session.
	syscert(str)            - /etc/sysconfig/rhn/systemid file content
	proxyver(str)           - the proxy version to be activated
	"""
	try:
		return rhn.session.proxy.activateProxy(syscert, proxyver) == 1
	except Exception, E:
		 return rhn.fail(E, 'activate system %d as an RHN proxy server')

# ---------------------------------------------------------------------------- #

def deactivateProxy(rhn, syscert, proxyver):
	"""
    API:
    proxy.deactivateProxy

	usage:
    activateProxy(rhn, syscert, proxyver)

    description:
	Activates a system as an RHN proxy server, using
	the given syscert file and proxy version

	returns: 
    Bool, or throws exception

	params:
	rhn                     - an authenticated RHN session.
	syscert(str)            - /etc/sysconfig/rhn/systemid file content
	proxyver(str)           - the proxy version to be activated
	"""
	try:
		return rhn.session.proxy.deactivateProxy(syscert, proxyver) == 1
	except Exception, E:
		 return rhn.fail(E, 'deactivate syscert %s as proxy server' % syscert)

# ---------------------------------------------------------------------------- #

def createMonitoringScout(rhn, syscert):
    """
    API:
    proxy.createMonitoringScout(rhn, syscert)

    usage:
    createMonitoringScout(rhn, syscert)

    description:
    Create Monitoring Scout for proxy

    returns:
    string

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
	syscert(str)            - /etc/sysconfig/rhn/systemid file content
    """
    try:
        return rhn.session.proxy.createMonitoringScout(syscert)
    except Exception, E:
        return rhn.fail(E, 'create monitoring scout for ')

# ---------------------------------------------------------------------------- #

def isProxy(rhn, syscert):
    """
    API:
    proxy.isProxy

    usage:
    isProxy(rhn, syscert)

    description:
    Checks if the given system is an RHN proxy or not.

    returns:
    Bool, or throws exception

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
	syscert(str)            - /etc/sysconfig/rhn/systemid file content
    """
    try:
        return rhn.session.proxy.isProxy(syscert) == 1
    except Exception, E:
        return rhn.fail(E, 'check if system is a proxy server')

# ---------------------------------------------------------------------------- #

def listAvailableProxyChannels(rhn, syscert):
    """
    API:
    proxy.listAvailableProxyChannels

    usage:
    listAvailableProxyChannels(rhn, syscert)

    description:
    List available version of proxy channel for system identified
    by the given client certificate i.e. syscert file

    returns:
    list of string (one per available version)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
	syscert(str)             - /etc/sysconfig/rhn/systemid file content
    """
    try:
        return rhn.session.proxy.listAvailableProxyVersions(syscert)
    except Exception, E:
        return rhn.fail(E, 'list proxy versions')

# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
