#!/usr/bin/env python
# -*- coding: utf-8 -*-
# and abstraction of the 'satellite' namespace
# in the RHN API for sat version 5.1.0

"""
rhnapi.satellite

An abstraction of the RHN API 'satellite' namespace for use
in python scripts

Updated for satellite 5.4.
"""

def listEntitlements(rhn):
	"""
    API: satellite.listEntitlements

	Usage: listEntitlements(rhn)
	
	Lists the available entitlements on a satellite server.

	Returns: 2x dict, system and channel
        { 'system' : [
            {'free_slots': 2657,
             'label': 'enterprise_entitled',
             'name': 'RHN Management Entitled Servers',
             'total_slots': 2658,
             'used_slots': 1},...
            ],
          'channel' : [
            {'free_flex': 0,
             'free_slots': 515,
             'label': 'rhx-alfresco ',
             'name': 'Alfresco Enterprise 2.0 (for RHEL Server v.5 x86) ',
             'total_flex': 515,
             'total_slots': 515,
             'used_flex': 0,
             'used_slots': 0}
            ]
        }

	params:
	rhn                     - an authenticated RHN session.
	"""
	try:
		return rhn.session.satellite.listEntitlements(rhn.key)
	except Exception, E:
		return rhn.fail(E, 'list entitlements on RHN server %s' % rhn.hostname)

def listProxies(rhn):
	"""
    API: satellite.listProxies

	Usage: listProxies(rhn)
	
	Lists the available entitlements on a satellite server.

	Returns: list of dict, one per system that is an activated proxy
            {'id': int (system id),
             'last_checkin': <DateTime '20110309T14:04:56' at 308d2d8>,
             'name': 'system name'}]

	params:
	rhn                     - an authenticated RHN session.
	"""
	try:
		return rhn.session.satellite.listProxies(rhn.key)
	except Exception, E:
		return rhn.fail(E, 'list proxies registered with RHN server %s' % rhn.hostname)

## ----------- updates for satellite 5.4 ------------------------------------ ##
def getCertificateExpirationDate(rhn):
    """
    API: satellite.getCertificateExpirationDate

    usage: getCertificateExpirationDate(rhn)

    description: Retrieves the certificate expiration date of the activated certificate.

    returns: dateTime.iso8601 (xmlrpclib.DateTime) - cast to str for parseable output.
            <DateTime '20110727T00:00:00' at 2ce8488>

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.satellite.getCertificateExpirationDate(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'get cert expiry date for satellite %s' % rhn.hostname)
