#!/usr/bin/env python
# -*- coding: utf-8 -*-
# abstraction of 'proxy' namespace from the RHN API
# for satellite 5.1.0
"""
rhnapi.proxy

Abstraction of the 'proxy' namespeace in the RHN Satelite API
updated for satellite v 5.4

These calls all take an argument of 'system_id' which is the content of
a systemid file - open('/etc/sysconfig/rhn/systemid').read() should do.

This suggests that they are only useful when run from a system that is
* intended to become an RHN proxy
* already is a registered RHN proxy

"""

def activateProxy(rhn, system_id, proxy_ver):
	"""
    API: proxy.activateProxy

	usage: activateProxy(rhn, system_id, proxy_ver)

	Activates a system as an RHN proxy server, using
	the given system_id file and proxy version

	returns: Bool, or throws exception

	params:
	rhn                     - an authenticated RHN session.
	system_id               - A system ID file (content of?)
	proxy_ver(str)          - the proxy version to be activated
	"""
	try:
		return rhn.session.proxy.activateProxy(system_id, proxy_ver) == 1
	except Exception, E:
		 return rhn.fail(E, 'activate system %d as an RHN proxy server')

def deactivateProxy(rhn, system_id, proxy_ver):
	"""
    API: proxy.deactivateProxy

	usage: activateProxy(rhn, system_id, proxy_ver)

	Activates a system as an RHN proxy server, using
	the given system_id file and proxy version

	returns: 

	params:
	rhn                      - an authenticated RHN session.
	system_id                - A system ID file (content of?)
	proxy_ver(str)           - the proxy version to be activated
	"""
	try:
		return rhn.session.proxy.deactivateProxy(system_id, proxy_ver) == 1
	except Exception, E:
		 return rhn.fail(E, 'deactivate systemid %s as proxy server' % system_id)

## ------ added for satellite 5.4 version ------------------- ##
def createMonitoringScout(rhn, system_id):
    """
    API: proxy.createMonitoringScout(rhn, system_id)

    usage: createMonitoringScout(rhn, system_id)

    description: Create Monitoring Scout for proxy

    returns: string

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
	system_id                - A system ID file (content of?)
    """
    try:
        return rhn.session.proxy.createMonitoringScout(system_id)
    except Exception, E:
        return rhn.fail(E, 'create monitoring scout for ')


def isProxy(rhn, system_id):
    """
    API: proxy.isProxy

    usage: isProxyrhn, system_id)

    description: checks if the given system is an RHN proxy or not.

    returns: Bool, or throws exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
	system_id                - A system ID file (content of?)
    """
    try:
        return rhn.session.proxy.isProxy(system_id) == 1
    except Exception, E:
        return rhn.fail(E, 'check if system is a proxy server')

def listAvailableProxyChannels(rhn, system_id):
    """
    API: proxy.listAvailableProxyChannels

    usage: listAvailableProxyChannels(rhn, system_id)

    description: List available version of proxy channel for system identified
    by the given client certificate i.e. systemid file

    returns: list of string (one per available version)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
	system_id                - A system ID file (content of?)
    """
    try:
        return rhn.session.proxy.listAvailableProxyVersions(system_id)
    except Exception, E:
        return rhn.fail(E, 'list proxy versions')


