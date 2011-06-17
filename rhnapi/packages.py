#!/usr/bin/env python
# -*- coding: utf-8 -*-
# a abstraction of the 'packages' namespace in the RHN API for sat 5.1.0
# import as rhnapi.packages

#  * findByNvrea
#  * getDetails
#  * listChangelog
#  * listDependencies
#  * listFiles
#  * listProvidingChannels
#  * listProvidingErrata
#  * removePackage

"""
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
def findByNvrea(rhn, pkgName, pkgVer, pkgRel, pkgArch, pkgEpoch=''):
	"""
    API: packages.findByNvrea

	usage: findByNvrea(rhn, name, version, release, arch, epoch=None)

	Find details about a package by Name Version Release (and possibly epoch)

	returns: list of dict, one per matched package
            { 'name' : str , 'version' : str , 'release' : str, 'epoch' : str,
              'id' : int, 'arch_label' : str,
              'path' : str (where the package is on the satellite, under /var/satellite),
              'provider' : str (determined by GPG signing key),
              'last_modified' : xmlrpclib.DateTime}

	parameters:
	rhn                      - an authenticated RHN session
	pkgname(str)             - the package name
	pkgVer(str)              - package version
	pkgRel(str)              - package release
	pkgArch(str)             - package architecture
	*pkgEpoch(str)           - package epoch. optional
	"""
	try:
		return rhn.session.packages.findByNvrea(rhn.key,pkgName, pkgVer, pkgRel, pkgEpoch, pkgArch)
	except Exception, E:
		return rhn.fail(E, 'find package %s-%s-%s.%s' % (pkgName, pkgVer, pkgRel, pkgArch,))

def getDetails(rhn, package_id):
	"""
    API: packages.getDetails

	usage: getDetailsByID(RHN, package_id)

	Retrieves package information based on a package ID

	returns: dict
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
     'version': '4.1.2'}

	parameters:
	rhn                      - an authenticated RHN session
	package_id(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.getDetails(rhn.key, package_id)
	except Exception, E:
		return rhn.fail(E, 'find package with ID %d' % package_id)

def getPackage(rhn, package_id):
    """
    API: packages.getPackage

    usage: getPackage(rhn, package_id)

    Retrieve the package file associated with a package.

    returns: the binary package file, base64 encoded.

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
	package_id(int)               - Package ID number
    """
    try:
        return rhn.session.packages.getPackage(rhn.key, package_id)
    except Exception, E:
        return rhn.fail(E, 'fetch package with ID %d' % package_id)

def getPackageUrl(rhn, package_id):
    """
    API: packages.getPackageUrl

    usage: getPackageUrl(rhn, package_id)

    returns: string

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
	package_id(int)          - Package ID number
    """
    try:
        return rhn.session.packages.getPackageUrl(rhn.key, package_id)
    except Exception, E:
        return rhn.fail(E, 'find download URL for package ID %d' % package_id)

def listChangelog(rhn, package_id):
	"""
    API: packages.listChangelog

	usage: listChangelog(rhn, package_id)

	Retrieves package changelog for package ID

	returns: list of dicts, one per entry
            {'author': str
            'date': str
            'text': str }

	parameters:
	rhn                      - an authenticated RHN session
	package_id(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.listChangelog(rhn.key, package_id)
	except Exception, E:
		return rhn.fail(E, 'get changelog for package ID %d' % package_id)

def listDependencies(rhn, package_id):
	"""
    API: packages.listDependencies

	usage: listDependencies(rhn, package_id)

	Retrieves dependency info for a package ID

	returns: list of dicts, one per dependency
             {'dependency': '/bin/sh',
              'dependency_modifier': ' ',
              'dependency_type': 'requires'},

	parameters:
	rhn                      - an authenticated RHN session
	package_id(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.listDependencies(rhn.key, package_id)
	except Exception, E:
		return rhn.fail(E, 'get changelog for package ID %d' % package_id)


def listFiles(rhn, package_id):
	"""
    API: packages.listFiles

	usage: listFiles(rhn, package_id)

	Retrieves file listing for package ID

	returns: list of dicts, one per file
        { 'checksum': '55e10cb00b262abf4a13e91e0bbb6040e1da2e428c9fb844430f4d0650c21ec0',
          'checksum_type': 'sha256',
          'last_modified_date': '2010-06-22 20:49:51',
          'linkto': '',
          'path': '/usr/share/man/man1/wait.1.gz',
          'size': 40,
          'type': 'file'},

	parameters:
	rhn                      - an authenticated RHN session
	package_id(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.listFiles(rhn.key, package_id)
	except Exception, E:
		return rhn.fail(E, 'get file list for package ID %d' % package_id)

def listProvidingChannels(rhn, package_id):
	"""
    API: packages.listProvidingChannels

	usage: listProvidingChannels(rhn, package_id)

	Lists channels providing a package ID

	returns: list of dicts, one per channel
        { 'label': 'rhel-x86_64-server-6',
          'name': 'Red Hat Enterprise Linux Server (v. 6 for 64-bit x86_64)',
          'parent_label': ' '}

	parameters:
	rhn                      - an authenticated RHN session
	package_id(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.listProvidingChannels(rhn.key, package_id)
	except Exception, E:
		return rhn.fail(E, 'get channel list for package ID %d' % package_id)

def listProvidingErrata(rhn, package_id):
	"""
    API: packages.listProvidingErrata

	usage: listProvidingErrata(rhn, package_id)

	Displays which Errata provide a given package.

	returns: list of dicts, one per entry

	parameters:
	rhn                      - an authenticated RHN session
	package_id(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.listProvidingErrata(rhn.key, package_id)
	except Exception, E:
		return rhn.fail(E, 'find errata providing package ID %d' % package_id)

def removePackage(rhn, package_id):
	"""
    API: packages.removePackage

	usage: removePackage(rhn, package_id)

	Removes a package from the satellite completely, from ALL channels.

	returns: 1 on success (!?)

	parameters:
	rhn                      - an authenticated RHN session
	package_id(int)               - Package ID number
	"""
	try:
		return rhn.session.packages.removePackage(rhn.key, package_id)
	except Exception, E:
		return rhn.fail(E, 'remove Package ID %d' % package_id)

## --------------- package.provider ------------------- ##
def associateKey(rhn, provider, key='', keytype='gpg'):
    """
    API: packages.provider.associateKey

    usage: associateKey(rhn, provider, key, keytype='gpg')

    Associate a package security key and with the package provider.
    *  If the provider or key doesn't exist, it is created.
    *  User executing the request must be a Satellite administrator. 

    returns: True, or throws exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    provider(str)            - provider name
    key(str)                 - the key content
    keytype(str)             - key type. Currently only understands 'gpg'
    """
    try:
        return rhn.session.packages.provider.associateKey(rhn.key, provider, key, keytype)
    except Exception, E:
        return rhn.fail(E, 'associate new key with package provider %s' % provider)

def listProviders(rhn):        
    """
    API: packages.provider.list

    usage: listProviders(rhn)

    lists all package providers

    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.packages.provider.list(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list all package providers')

def listKeys(rhn, provider):
    """
    API: packages.provider.listKeys

    usage: listKeys(rhn, provider)

    List all security keys associated with a package provider.
    User executing the request must be a Satellite administrator.

    returns: list/dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    provider(str)            - provider name
    """
    try:
        return rhn.session.packages.provider.listKeys(rhn.key, provider)
    except Exception, E:
        return rhn.fail(E, 'get list of package security keys for provider %s' % provider)

## --------------- packages.search ----------------------------- ##
def search(rhn, luceneQuery):
    """
    API: packages.search.advanced

    usage: advancedSearch(rhn, luceneQuery)

    Advanced method to search lucene indexes with a passed in query written in
    Lucene Query Parser syntax.
    Fields searchable for Packages:
    name, epoch, version, release, arch, description, summary
    Lucene Query Example: "name:kernel AND version:2.6.18 AND -description:devel" 


    returns: list of dict, one per matching package

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    luceneQuery(str)         - query string
    """
    try:
        return rhn.session.packages.search.advanced(rhn.key, luceneQuery)
    except Exception, E:
        return rhn.fail(E, 'search for packages using query "%s"' % luceneQuery)

def searchActivationKey(rhn, luceneQuery, actkey):
    """
    API: packages.search.advancedWithActKey

    usage: searchActivationKey(rhn, luceneQuery, actkey)

    Advanced method to search lucene indexes with a passed in query written in
    Lucene Query Parser syntax, additionally this method will limit results
    to those which are associated with a given activation key.

    returns: list of dict, one per matched package

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    luceneQuery(str)         - query string
    actkey(Str)              - activation key (hex id)
    """
    try:
        return rhn.session.packages.search.advancedWithActKey(rhn.key, luceneQuery, actkey)
    except Exception, E:
        return rhn.fail(E, 'find packages in activation key "%s" using query "%s"' %(actkey, luceneQuery))

def searchChannel(rhn, luceneQuery, chanlabel):        
    """
    API: packages.search.advancedWithChannel

    usage: searchChannel(rhn, luceneQuery, chanlabel)

    Advanced method to search lucene indexes with a passed in query written in
    Lucene Query Parser syntax, additionally this method will limit results
    to those which are in the passed in channel label

    returns: list of dict, one per matched package

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    luceneQuery(str)         - query string
    chanlabel(str)           - software channel label
    """
    try:
        return rhn.session.packages.search.advancedWithChannel(rhn.key, luceneQuery, chanlabel)
    except Exception, E:
        return rhn.fail(E, 'search for packages in channel "%s" using query "%s"' %(chanlabel, luceneQuery))

def searchName(rhn, package_name):
    """
    API: packages.search.name

    usage: searchName(rhn, package_name)

    Search the lucene package indexes for all packages which match the given name

    returns: list of dict, one per matched package (or throws exception)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    luceneQuery(str)         - query string
    package_name(str)        - name to search for
    """
    try:
        return rhn.session.packages.search.name(rhn.key, package_name)
    except Exception, E:
        return rhn.fail(E, 'search for packages matching name "%s"' % package_name)

def searchNameAndDescription(rhn, query):
    """
    API: packages.search.nameAndDescription

    usage: searchNameAndDescription(rhn, query)

    Search the lucene package indexes for all packages which match the given
    query in name or description

    returns: list of dict, one per matched package (or throws exception)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    query(str)               - string to search for
    """
    try:
        return rhn.session.packages.search.nameAndDescription(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search packages names and descriptions using query "%s"' % query)

def searchNameAndSummary(rhn, query):
    """
    API: packages.search.nameAndSummary

    usage: searchNameAndSummary(rhn, query)

    Search the lucene package indexes for all packages which match the given
    query in name or summary

    returns: list of dict, one per matched package (or throws exception)

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    query(str)               - string to search for
    """
    try:
        return rhn.session.packages.search.nameAndSummary(rhn.key, query)
    except Exception, E:
        return rhn.fail(E, 'search packages names and summaries using query "%s"' % query)
