#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the 'preferences.locale' namespace
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
Abstraction of the 'preferences.locale' namespace.
Who knows, there might be other preferences namespaces eventually.
Flattened for ease of use.
Actual API calls listed in the individual methods
"""

__author__ = "Stuart Sears"

# ---------------------------------------------------------------------------- #

def listLocales(rhn):
	"""
    API:
    preferences.locale.listLocales

    usage:
    listLocales(rhn)

    description:
    List of all understood locales. Can be used as input to setLocale

    returns:
    list of strings (recognised local/language abbreviations)
    
	params:
	rhn                     - an authenticated RHN session.
	"""
	try:
		return rhn.session.preferences.locale.listLocales()
	except Exception, E:
		return rhn.fail(E, 'list available locales')

# ---------------------------------------------------------------------------- #

def listTimeZones(rhn):
	"""
    API:
    preferences.locale.listTimeZones

    usage:
    listTimeZones(rhn)

    description:
    lists recognised timezones

    returns:
    list of dict, one per timezone.
            {
             'olson_name': 'Pacific/Norfolk',i
             'time_zone_id': 7021
            }
	params:
	rhn                     - an authenticated RHN session.
	"""
	try:
		return rhn.session.preferences.locale.listTimeZones()
	except Exception, E:
		return rhn.fail(E, 'list available Timezones on RHN server %s' % rhn.hostname)

# ---------------------------------------------------------------------------- #

def setTimeZone(rhn, username, tzid):
	"""
    API:
    preferences.locale.setTimeZone

    usage:
    setTimeZone(rhn, username, tzid)

    description:
    Sets the default timezone for the given RHN username.

    returns:
    True, or throws exception

	params:
	rhn                     - an authenticated RHN session.
	username(str)           - user username
	tzid(int)               - A valid timezone identifier, from listTimeZones()
	"""
	try:
		return rhn.session.preferences.locale.setTimeZone(rhn.key, username, tzid) == 1
	except Exception, E:
		return rhn.fail(E, 'set timezone for user %s' % username)

# ---------------------------------------------------------------------------- #

def setLocale(rhn, username, locale):
	"""
    API:
    preferences.locale.setLocale

    usage:
    setLocale(rhn, username, locale)

    description:
    sets the default locale for the given RHN username

    returns:
    True, or throws exception

	params:
	rhn                     - an authenticated RHN session.
	username(str)           - user username
	locale(str)             - A valid locale name from listLocales()
	"""
	try:
		return rhn.session.preferences.locale.setLocale(rhn.key, username, locale) == 1
	except Exception, E:
		return rhn.fail(E, 'set locale %s for user %s' %(locale, username))

# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
