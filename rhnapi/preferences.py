#!/usr/bin/env python
# -*- coding: utf-8 -*-
# an abstraction of the preferences.locale namespace
# from the RHN API for Satellite 5.1.0

"""
Abstraction of the 'preferences.locale' namespace.
Flattened for ease of use.
Actual API calls listed in the individual methods

"""

def listLocales(rhn):
	"""
    usage: listLocales(rhn)

    preferences.locale.listLocales

    List of all understood locales. Can be used as input to setLocale

    returns: list of strings (recognised local/language abbreviations)
    
	params:
	rhn                     - an authenticated RHN session.
	"""
	try:
		return rhn.session.preferences.locale.listLocales()
	except Exception, E:
		return rhn.fail(E, 'list available locales')

def listTimeZones(rhn):
	"""
    preferences.locale.listTimeZones

    lists recognised timezones

    returns: list of dict, one per timezone.
            {'olson_name': 'Pacific/Norfolk', 'time_zone_id': 7021}
	params:
	rhn                     - an authenticated RHN session.
	"""
	try:
		return rhn.session.preferences.locale.listTimeZones()
	except Exception, E:
		return rhn.fail(E, 'list available Timezones on RHN server %s' % rhn.hostname)

def setTimeZone(rhn, login, tzid):
	"""
    preferences.locale.setTimeZone

    usage: setTimeZone(rhn, login, tzid)

    Sets the default timezone for the given RHN login.

    returns: True, or throws exception

	params:
	rhn                     - an authenticated RHN session.
	login(str)              - user login
	tzid(int)               - A valid timezone identifier, from listTimeZones()
	"""
	try:
		return rhn.session.preferences.locale.setTimeZone(rhn.key, login, tzid) == 1
	except Exception, E:
		return rhn.fail(E, 'set timezone for user %s' % login)

def setLocale(rhn, login, locale):
	"""
    preferences.locale.setLocale

    sets the default locale for the given RHN login

    returns: True, or throws exception

	params:
	rhn                     - an authenticated RHN session.
	login(str)              - user login
	locale(str)             - A valid locale name from listLocales()
	"""
	try:
		return rhn.session.preferences.locale.setLocale(rhn.key, login, locale) == 1
	except Exception, E:
		return rhn.fail(E, 'set locale %s for user %s' %(locale, login))

