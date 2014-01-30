#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the 'packages' namespace
# and its children / sub-namespaces
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
rhnapi.packages

A python interface to the 'packages' namespace in RHN Satellite 5.4+
That is to say, some of these may work on earlier versions, but haven't been
tested on them.

This file includes the methods from the following namespaces:
packages
packages.provider
packages.search

Some methods have been renamed to follow a sensible, understandable scheme
and to facilitate the flattening into a single file.
E.g. all packages.search.* methods now being with 'search':

packages.search namespace:
search -> packages.search.advanced
searchActivationKey -> packages.search.advancedWithActKey
searchChannel -> packages.search.advancedWithChannel
searchName -> packages.search.name
searchNameAndDescription -> packages.search.nameAndDescription
searchNameAndSummary -> packages.search.nameAndSummary
"""
__author__ = "Stuart Sears"

# ---------------------------------------------------------------------------- #

def findByNvrea(rhn, pkgname, pkgver, pkgrel, pkgarch, pkgepoch=''):
	"""
    API:
    packages.findByNvrea

	usage:
    findByNvrea(rhn, name, version, release, arch, epoch=None)

    description:
	Find details about a package by Name Version Release (and possibly epoch)

	returns:
    list of dict, one per matched package
        { 'name' : str ,
          'version' : str ,
          'release' : str,
          'epoch' : str,
          'id' : int,
          'arch_label' : str,
          'path' : str (where the package is on the satellite, under /var/satellite),
          'provider' : str (determined by GPG signing key),
          'last_modified' : xmlrpclib.DateTime,
        }

	parameters:
	rhn                     - an authenticated RHN session
	pkgname(str)            - the package name
	pkgver(str)             - package version
	pkgrel(str)             - package release
	pkgarch(str)            - package architecture
	*pkgepoch(str)          - package epoch. optional
	"""
	try:
		return rhn.session.packages.findByNvrea(rhn.key,pkgname, pkgver, pkgrel, pkgepoch, pkgarch)
	except Exception, E:
		return rhn.fail(E, 'find package %s-%s-%s.%s' % (pkgname, pkgver, pkgrel, pkgarch,))

# ---------------------------------------------------------------------------- #

def getDetails(rhn, pkgid):
	"""
    API:
    packages.getDetails

	usage:
    getDetailsByID(RHN, pkgid)

    description:
	Retrieves package information based on a package ID

	returns:
    dict
    {'arch_label': str
     'build_date': str
     'build_host': str
     'checksum': str
     'checksum_type': str
     'cookie': 'None',
     'description': str
     'epoch': str,
     'file': str (actual package filename)
     'id': int,
     'last_modified_date': str
     'license': str
     'name': 'bash',
     'path': str
     'payload_size': str,
     'providing_channels': [list of channels containing this package]
     'release': '3.el6',
     'size': '928344',
     'summary': 'The GNU Bourne Again shell\n',
     'vendor': 'Red Hat, Inc.',
     'version': '4.1.2'
    }

	parameters:
	rhn                      - an authenticated RHN session
	pkgid(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.getDetails(rhn.key, pkgid)
	except Exception, E:
		return rhn.fail(E, 'find package with ID %d' % pkgid)

# ---------------------------------------------------------------------------- #

def getPackage(rhn, pkgid):
    """
    API:
    packages.getPackage

    usage:
    getPackage(rhn, pkgid)

    description:
    Retrieve the package file associated with a package.

    returns:
    the binary package file, base64 encoded.

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
	pkgid(int)               - Package ID number
    """
    try:
        return rhn.session.packages.getPackage(rhn.key, pkgid)
    except Exception, E:
        return rhn.fail(E, 'fetch package with ID %d' % pkgid)

# ---------------------------------------------------------------------------- #

def getPackageUrl(rhn, pkgid):
    """
    API:
    packages.getPackageUrl

    usage:
    getPackageUrl(rhn, pkgid)

    description:
    Retrieve the url that can be used to download a package.i
    This will expire after a certain time period.

    returns:
    string

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
	pkgid(int)          - Package ID number
    """
    try:
        return rhn.session.packages.getPackageUrl(rhn.key, pkgid)
    except Exception, E:
        return rhn.fail(E, 'find download URL for package ID %d' % pkgid)

# ---------------------------------------------------------------------------- #

def listChangelog(rhn, pkgid):
	"""
    API:
    packages.listChangelog

	usage:
    listChangelog(rhn, pkgid)

    description:
	Retrieves package changelog for package ID

	returns:
    list of dicts, one per entry
            {'author': str
            'date': str
            'text': str }

	parameters:
	rhn                      - an authenticated RHN session
	pkgid(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.listChangelog(rhn.key, pkgid)
	except Exception, E:
		return rhn.fail(E, 'get changelog for package ID %d' % pkgid)

# ---------------------------------------------------------------------------- #

def listDependencies(rhn, pkgid):
	"""
    API:
    packages.listDependencies

	usage:
    listDependencies(rhn, pkgid)

    description:
	Retrieves dependency info for a package ID

	returns:
    list of dicts, one per dependency
        {
           'dependency': (str) usually file path or package name,
           'dependency_modifier': (str),
           'dependency_type': (str) one of {'requires', 'conflicts', 'obsoletes', 'provides'],
        }, 
	parameters:
	rhn                      - an authenticated RHN session
	pkgid(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.listDependencies(rhn.key, pkgid)
	except Exception, E:
		return rhn.fail(E, 'get changelog for package ID %d' % pkgid)

# ---------------------------------------------------------------------------- #

def listFiles(rhn, pkgid):
	"""
    API:
    packages.listFiles

	usage:
    listFiles(rhn, pkgid)

    description:
	Retrieves file listing for package ID

	returns:
    list of dict, one per file
        { 'checksum': (str) '55e10cb00b262abf4a13e91e0bbb6040e1da2e428c9fb844430f4d0650c21ec0',
          'checksum_type': (str) 'sha256',
          'last_modified_date': (str) '2010-06-22 20:49:51',
          'linkto': (str) '',
          'path': (str) '/usr/share/man/man1/wait.1.gz',
          'size': (int) 40,
          'type': (str) 'file'
        },

	parameters:
	rhn                      - an authenticated RHN session
	pkgid(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.listFiles(rhn.key, pkgid)
	except Exception, E:
		return rhn.fail(E, 'get file list for package ID %d' % pkgid)

# ---------------------------------------------------------------------------- #

def listProvidingChannels(rhn, pkgid):
	"""
    API:
    packages.listProvidingChannels

	usage:
    listProvidingChannels(rhn, pkgid)

    description:
	Lists channels providing a package ID

	returns:
    list of dicts, one per channel
        { 
          'label': 'rhel-x86_64-server-6',
          'name': 'Red Hat Enterprise Linux Server (v. 6 for 64-bit x86_64)',
          'parent_label': ' '
        }

	parameters:
	rhn                      - an authenticated RHN session
	pkgid(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.listProvidingChannels(rhn.key, pkgid)
	except Exception, E:
		return rhn.fail(E, 'get channel list for package ID %d' % pkgid)

# ---------------------------------------------------------------------------- #

def listProvidingErrata(rhn, pkgid):
	"""
    API:
    packages.listProvidingErrata

	usage:
    listProvidingErrata(rhn, pkgid)

    description:
	Displays which Errata provide a given package.

	returns:
    list of dicts, one per entry

	parameters:
	rhn                      - an authenticated RHN session
	pkgid(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.listProvidingErrata(rhn.key, pkgid)
	except Exception, E:
		return rhn.fail(E, 'find errata providing package ID %d' % pkgid)

# ---------------------------------------------------------------------------- #

def removePackage(rhn, pkgid):
	"""
    API:
    packages.removePackage

	usage:
    removePackage(rhn, pkgid)

    description:
	Removes a package from the satellite completely, from ALL channels.

	returns:
    bool, or throws exception

	parameters:
	rhn                      - an authenticated RHN session
	pkgid(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.removePackage(rhn.key, pkgid) == 1
	except Exception, E:
		return rhn.fail(E, 'remove Package ID %d' % pkgid)

# ----------------------------- package.provider ----------------------------- #

def associateKey(rhn, provider, key='', keytype='gpg'):
    """
    API:
    packages.provider.associateKey

    usage:
    associateKey(rhn, provider, key, keytype='gpg')

    Associate a package security key and with the package provider.
    *  If the provider or key doesn't exist, it is created.
    *  User executing the request must be a Satellite administrator. 

    returns:
    True, or throws exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    provider(str)            - provider name
    key(str)                 - the key content
    keytype(str)             - key type. Currently only understands 'gpg'
    """
    try:
        return rhn.session.packages.provider.associateKey(rhn.key, provider, key, keytype) == 1
    except Exception, E:
        return rhn.fail(E, 'associate new key with package provider %s' % provider)

# ---------------------------------------------------------------------------- #

def listProviders(rhn):        
    """
    API:
    packages.provider.list

    usage:
    listProviders(rhn)

    description:
    lists all package providers

    returns:
    list/dict
        {
          'name' : (str),
          'keys' : [
                     {
                        'key'  : (str)
                        'type' : (str)
                     }
                   ]
        }

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.packages.provider.list(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list all package providers')

# ---------------------------------------------------------------------------- #

def listKeys(rhn, provider):
    """
    API:
    packages.provider.listKeys

    usage:
    listKeys(rhn, provider)

    description:
    List all security keys associated with a package provider.
    User executing the request must be a Satellite administrator.

    returns:
    list/dict
        {
            'key'  : (str)
            'type' : (str)
        }

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    provider(str)            - provider name
    """
    try:
        return rhn.session.packages.provider.listKeys(rhn.key, provider)
    except Exception, E:
        return rhn.fail(E, 'get list of package security keys for provider %s' % provider)

# ----------------------------- packages.search ------------------------------ #

def search(rhn, query):
    """
    API:
    packages.search.advanced

    usage:
    advancedSearch(rhn, query)

    description:
    Advanced method to search lucene indexes with a passed in query written in
    Lucene Query Parser syntax.
    Fields searchable for Packages:
    name, epoch, version, release, arch, description, summary
    Lucene Query Example: "name:kernel AND version:2.6.18 AND -description:devel" 


    returns:
    list of dict, one per matching package

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    query(str)         - query string
    """
    try:
        return rhn.session.packages.search.advanced(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search for packages using query "%s"' % query)

def searchAdvanced(rhn, query):
    """
    wrapper around search to look more like the API :)
    """
    return search(rhn, query)

# ---------------------------------------------------------------------------- #

def searchActivationKey(rhn, query, actkey):
    """
    API:
    packages.search.advancedWithActKey

    usage:
    searchActivationKey(rhn, query, actkey)

    description:
    Advanced method to search lucene indexes with a passed in query written in
    Lucene Query Parser syntax, additionally this method will limit results
    to those which are associated with a given activation key.

    returns:
    list of dict, one per matched package

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    query(str)         - query string
    actkey(Str)              - activation key (hex id)
    """
    try:
        return rhn.session.packages.search.advancedWithActKey(rhn.key, query, actkey)
    except Exception, E:
        return rhn.fail(E, 'find packages in activation key "%s" using query "%s"' %(actkey, query))

# ---------------------------------------------------------------------------- #

def searchAdvancedWithActivationKey(rhn, query, actkey):
    """
    wrapper around searchActivationKey
    """
    return searchActivationKey(rhn, query, actkey)

# ---------------------------------------------------------------------------- #

def searchChannel(rhn, query, chanlabel):        
    """
    API:
    packages.search.advancedWithChannel

    usage:
    searchChannel(rhn, query, chanlabel)

    description:
    Advanced method to search lucene indexes with a passed in query written in
    Lucene Query Parser syntax, additionally this method will limit results
    to those which are in the passed in channel label

    returns:
    list of dict, one per matched package

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    query(str)         - query string
    chanlabel(str)           - software channel label
    """
    try:
        return rhn.session.packages.search.advancedWithChannel(rhn.key, query, chanlabel)
    except Exception, E:
        return rhn.fail(E, 'search for packages in channel "%s" using query "%s"' %(chanlabel, query))

# ---------------------------------------------------------------------------- #

def searchAdvancedWithChannel(rhn, query, chanlabel):
    """
    wrapper around searchChannel
    """
    return searchChannel(rhn, query, chanlabel)

# ---------------------------------------------------------------------------- #

def searchName(rhn, pkgname):
    """
    API:
    packages.search.name

    usage:
    searchName(rhn, pkgname)

    description:
    Search the lucene package indexes for all packages which match the given name

    returns:
    list of dict, one per matched package (or throws exception)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    query(str)         - query string
    pkgname(str)        - name to search for
    """
    try:
        return rhn.session.packages.search.name(rhn.key, pkgname)
    except Exception, E:
        return rhn.fail(E, 'search for packages matching name "%s"' % pkgname)

# ---------------------------------------------------------------------------- #

def searchNameAndDescription(rhn, query):
    """
    API:
    packages.search.nameAndDescription

    usage:
    searchNameAndDescription(rhn, query)

    description:
    Search the lucene package indexes for all packages which match the given
    query in name or description

    returns:
    list of dict, one per matched package (or throws exception)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    query(str)               - string to search for
    """
    try:
        return rhn.session.packages.search.nameAndDescription(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search packages names and descriptions using query "%s"' % query)

# ---------------------------------------------------------------------------- #

def searchNameAndSummary(rhn, query):
    """
    API:
    packages.search.nameAndSummary

    usage:
    searchNameAndSummary(rhn, query)

    description:
    Search the lucene package indexes for all packages which match the given
    query in name or summary

    returns:
    list of dict, one per matched package (or throws exception)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    query(str)               - string to search for
    """
    try:
        return rhn.session.packages.search.nameAndSummary(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search packages names and summaries using query "%s"' % query)
        
# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
