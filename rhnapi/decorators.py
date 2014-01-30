#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module containing decorators, used by other modules
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
import xmlrpclib

def logexcptn(fn):
    # this expects a given fn to be provided with an 'rhn' argument
    def wrapper(*args, **kwargs):
        # the RHN session object is our default first argument.
        # we want to use it here, too
        rhn = args[0]
        try:
            fn(*args, **kwargs)
        except xmlrpclib.Fault, F:
            rhn.logError("%s (%s)" %(F.faultString, str(F.faultCode)))
            return False
        except Exception, E:
            rhn.logError("Non-XMLRPC Error: %s" % E.msg)
            return False

    return wrapper

            


# footer - do not edit below this line
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
