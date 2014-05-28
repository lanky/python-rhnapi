#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module providing additional general utilities
# primarily for serialisation, csv output etc
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
rhnapi.utils

utilities to use with rhnapi, to perform common tasks.

Some of these are generic, just placed here because they are used a lot

Some require an rhnapi.rhnSession object.
"""

__author__ = "Stuart Sears"

# handle the renaming of simplejson -> json in later python versions
try:
    import json
except ImportError:
    import simplejson as json

from operator import itemgetter
import time
from xmlrpclib import DateTime as xmlrpcDateTime
import csv
import sys

# presumes the existence of the rhnapi module on your PYTHONPATH
from rhnapi.satellite import listEntitlements
from rhnapi.system import listSystems, getBaseChannel

# --------------------------------------------------------------------------------- #

def showEntitlements(rhn):
	"""
    usage:
    showEntitlements(rhn)

    description:
	print a summary of the entitlement usage on a satellite.

    returns:
    text output to stdout

	params:
	rhn                    - an authenticated rhn session
	"""
	try:
		satents =  listEntitlements(rhn)
		# deal with system entitlements first
		# title line:
		print "%-45s %6s %6s %6s" %('System Entitlement','used','free','total')
		print "%s %s %s %s" %('=' * 45,'=' * 6,'=' * 6,'=' * 6)

		# cycle through the system entitlements
		for ent in sorted(satents['system'], key = itemgetter('name')):
			print "%-45s %6d %6d %6d" %(ent['name'], ent['used_slots'], ent['free_slots'], ent['total_slots'])
		# separator
		print "\n\n"

		# title
		print "%-45s %6s %6s %6s" %('Software Channel Entitlement','used','free','total')
		print "%s %s %s %s" %('=' * 45,'=' * 6,'=' * 6,'=' * 6)

		# now show channels to which the client has entitlements
		validchans = [ x for x in satents['channel'] if x['total_slots'] != 0 ]

		for ent in sorted(validchans, key = itemgetter('label')):
			print "%-45s %6d %6d %6d" %(ent['label'], ent['used_slots'], ent['free_slots'], ent['total_slots'])

	except Exception, E:
		return rhn.fail(E, 'list entitlement usage on satellite %s' % rhn.hostname)
        
# --------------------------------------------------------------------------------- #

def showChannelUsage(rhn):
	"""
    usage:
    showChannelUsage(rhn)

    description:
	pull system list from RHN/Satellite, look up base channels 
	count of systems subscribed to each.
	This can take a long time!

    returns:
    text to stdout

    parameters:
	rhn - an authenticated RHN session
	"""
	# from rhnapi.channel import getEntitlements
	try:
		syslist = listSystems(rhn)
		systemcount = len(syslist)
		chanusage = {}
		for s in syslist:
			id = int(s["id"])
			basechan = getBaseChannel(rhn, id)
			if chanusage.has_key(basechan):
				chanusage[basechan] += 1
			else:
				chanusage[basechan] = 1
		print "count\tchannel label"
		print "=====\t============="
		for k in chanusage.keys():
			print "%d\t%s" %( chanusage[k], k )
		print "-----------------------"
		print 'system count: %d' % len(syslist)
	except Exception, E:
		return rhn.fail(E, "list channel subscriptions and usage" )
        
# --------------------------------------------------------------------------------- #

class RhnJSONEncoder(json.JSONEncoder):
    """
    description:
    Custom JSON encoder class, to handle python objects that do not serialise cleanly
    by default.

    Currently supported elements:
    * xmlrpclib.DateTime objects : serialised as str - obj.value
    Converts <DateTime 'YYYYMMDDTHH:MM:SS' at memaddr> objects to str
    (which handily returns the quoted string above)

    * python sets                : converted to lists - list(obj)
    """
    def default(self, obj):
        """
        xmlrpclib.DateTime is non-serializable, but its 'value' is a unicode str, so...
        """
        if isinstance(obj, xmlrpcDateTime):
            return obj.value

        if isinstance(obj, set):
            return list(obj)

        return json.JSONEncoder.default(self, obj)
        
# --------------------------------------------------------------------------------- #

def dumpJSON(obj, outputfile, indent = 2, verbose = False, customenc = RhnJSONEncoder):
    """
    Serialises the chosen object as JSON.
    
    Normally I'd expect this to be a list of dict structures
    This does not technically require an RHN instance, but is a useful utility

    parameters:
    obj(object)         - the object to serialise.
    outputfile(str)     - path to output file
    indent(int)         - number of spaces to indent elements in output.
                          intended to ease reading of the files this produces
    verbose(bool)       - be more verbose
    customenc           - custom JSON encoding class (here defaulting to our
                          locally-defined DateTimeEncoder class)
    """
    try:
        fd = open(outputfile, 'wb')
        try:
            data = json.dumps(obj, indent = indent, cls = customenc)
        except:
            if verbose:
                print "could not serialise object"
            return False
        fd.write(data)
        fd.close()
        return True
    except IOError, E:
        if verbose:
            print "Could not open file %s for writing. Check permissions"
            print E.strerror
        return False
        
# --------------------------------------------------------------------------------- #

def loadJSON(inputfile, verbose = False, logger = None):
    """
    Loads data from a JSON file (probably but not necessarily 
    exported with dumpJSON above) and returns it.

    returns dataobject, or None

    parameters:
    inputfile(str)          - path to JSON file
    """
    try:
        data = open(inputfile).read()
        try:
            jsondata = json.loads(data)
            return jsondata
        except ValueError, E:
            if logger is not None:
                logger.warn("ERROR: exception raised, '%s'" % E.__str__())
                logger.exception("could not read in data from %s" % inputfile)
    except IOError, E:
        if logger is not None:
            logger.warn(E.__str__())
            logger.exception("could not open file %s for reading. Check permissions?" % inputfile)
        return None
        
# --------------------------------------------------------------------------------- #

def promptMissing(promptstr):
    """
    prompt for a missing element
    """
    return str(raw_input(promptstr))

# --------------------------------------------------------------------------------- #
def promptConfirm(action, default='Y'):
    """
    prompt for a yes/no answer to an action
    """
    ans = raw_input('Really %s (y/n) [%s]? ' %(action, default))
    # if we type in the default answer, then return True
    if str(ans).lower() == default.lower():
        return True
    # it's the default, so return true if we just hit enter:
    elif len(str(ans).lower().strip()) == 0:
        return True
    # anything else, return False
    else:
        return False

# --------------------------------------------------------------------------------- #
def csvReport(objectlist, outputfile,  fields = None):
    """
    Creates a CSV report, with a header line from the data provided
    This uses the python stdlib csv.DictWriter class, where each line is constructed from
    dictionary key/value pairs

    This will write a header line with field names too.


    parameters:
    objectlist  - list of dict/hash objects, as much of the satellite output appears to be
    outputfile  - a filename/path (not a file descriptor) to write data to. Will be overwritten if it exists.
    fields      - the list of dictionary keys (in order) to put in each row. This can be a subset of the keys
                  in each object. 

    """
    fd = None
    try:
        # attempt to open the output file for writing
        if isinstance(outputfile, file):
            fd = outputfile
        else:
            try:
                fd = open(outputfile, 'wb')
            except:
                raise

        if fields is None:
            # assume we want all the possible fields in the input dict
            # and that all entries match the first one.
            fields = objectlist[0].keys()

        headerline = {}
        # generate a header line
        for f in fields:
            headerline[f] = f
        
        mywriter = csv.DictWriter(fd, fields, restval='', extrasaction = 'ignore')
        mywriter.writerow(headerline)
        mywriter.writerows(objectlist)

        try:
            print "------------------------"
            if not fd.isatty():
                fd.close()
        except ValueError:
            pass
        
        return True

    except:
        raise

# ---------------------------------------------------------------------------- #

def getMaxLen(dictlist):
    """
    parses a list of dict (common output from RHN API) and calculates the longest
    entry for each key it finds.
    Currently does not do recursion, so dicts of dicts are not supported.
    TODO: add this in future release.

    This is useful for formatting output

    returns:
    dict { 'key' : maxlength(int) }

    parameters:
    dictlist(list of dict)  - list of dictionary structures.
    """
    maxlen = {}
    for d in dictlist:
        for k, v in d.iteritems():
            curval = maxlen.get(k, 0)
            try:
                mylen = len(v)
# for objects that don't support len():
            except:
                mylen = len(str(v))

            if mylen > curval:
                maxlen[k] = mylen

    return maxlen

# ---------------------------------------------------------------------------- #

def get_pkgstr(pkgobj):
    """
    returns E:NVR.A or NVR.A for a given package object, 
    depending on whether it has an epoch or not
    
    parameters:
        pkgobj(dict): a dict representing a package in RHN, usually from
                      channel.list(AllPackages) or a similar API call.

    returns:
        string:  E:NVR.A or NVR.A, depending on the presence of an epoch
    """
    # this bit is always the same
    keys = [ "%(name)s-%(version)s-%(release)s" ]
    # arch or arch_label? (thanks, RHN!)
    if pkgobj.get('arch_label', False):
        keys.append(".%(arch_label)s")
    else:
        keys.append(".%(arch)s")

    # epoch?
    if len(pkgobj.get('epoch').strip()) != 0:
        keys.insert(0, "%(epoch)s:")

    return ''.join(keys) % pkgobj

# ---------------------------------------------------------------------------- #

def get_errid(errobj):
    """
    fetch the YYYY:NNNN part from an errata dict object
    basically strips off the CLA/RHSA etc prefix

    parameters:
        errobj(dict): dict representing an erratum in RHN

    returns:
        string: YYYY:NNNN from an erratum
    """
    return errobj.get('advisory').split('-')[1]

# ---------------------------------------------------------------------------- #

def index_dictlist(dictlist, keyfunc):
    """
    generate an index for a list of dict, using a key function.
    key MUST be a function that can take a dict as an argument.

    Useful for generating an index from lists of packages etc

    parameters:
        dictlist(list of dict): list of dictionary objects (packages, errata etc)
        keyfunc(function): a function that extracts data from a dict.
            must take a dict as an argument.
    """
    try:
        return dict( zip ((keyfunc(entry) for entry in dictlist), dictlist))
    except:
        return None

# ---------------------------------------------------------------------------- #

def batch_iterate(iterable, batchsize):
    """
    takes an arbitrary iterable (list, set, string etc) and returns an iterator
    that yields the input in fixed size batches (e.g. split a list into groups of
    50 items for batch processing)
    if there are fewer than 'batchsize' elements remaining, return the incomplete
    final portion

    Shamelessly based on:
    http://stackoverflow.com/questions/312443/
    and the recipes here: (for "grouper")
    http://docs.python.org/2/library/itertools.html?highlight=itertools#recipes
    
    parameters:
    iterable        - an iterable object, such as a set or list
    batchsize       - the number of elements to return in each batch

    returns:
    generator/iterator object, which we can loop over.
    raises StopIteration at end

    this will not pad the final batch if it is smaller than 'batchsize'
    """
    # harmless if already imported
    import itertools

    it = iter(iterable)
    while True:
       yield tuple(itertools.islice(it, batchsize)) or it.next()


# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
