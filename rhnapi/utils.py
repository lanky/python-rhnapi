#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module providing additional general utilities
# primarily for serialisation, csv output etc
#
# Copyright 2009-2012 Stuart Sears
#
# This file is part of python-rhnapi
#
# python-rhnapi is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
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
from  xmlrpclib import DateTime as xmlrpcDateTime
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

class DateTimeEncoder(json.JSONEncoder):
    """
    description:
    Custom encoder for xmlrpclib.DateTime objects, which are not directly
    serialisable.
    Converts <DateTime 'YYYYMMDDTHH:MM:SS' at memaddr> objects to str
    (which handily returns the quoted string above)
    """
    def default(self, obj):
        """
        xmlrpclib.DateTime is non-serializable, but its 'value' is a unicode str, so...
        """
        if isinstance(obj, xmlrpcDateTime):
            return obj.value
        return simplejson.JSONEncoder.default(self, obj)
        
# --------------------------------------------------------------------------------- #

def dumpJSON(obj, outputfile, indent = 2, verbose = False, customenc = DateTimeEncoder):
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
    except IOError, E:
        if verbose:
            print "Could not open file %s for writing. Check permissions"
            print E.strerror
        return False
        
# --------------------------------------------------------------------------------- #

def loadJSON(inputfile, verbose = False):
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
        except:
            print "could not read in data from %s" % inputfile
    except IOError, E:
        if verbose:
            print "could not open file %s for reading. Check permissions?" % inputfile
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
    ans = raw_input('Really %s [%s]? ' %(action, default))
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
    try:
        # attempt to open the output file for writing
        try:
            fd = open(outputfile, 'wb')
        except:
            fd = outputfile

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
            fd.close()
        except:
            pass
        return True

    except Exception, E:
        raise E
        return False


