#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module
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



# a top-level init file for the RHN API namespaces

__doc__ = """
Contains the core RHN class, with the 'api' namespace subsumed into it.
Plus additional methods for URL munging, login/password prompting
and reading writing ini-style config files for saved credentials

All the classes and methods below have docstrings, so help(item) should
work for further documentation

Classes
* proxiedTransport
  The core proxied transport class for accessing an RHN server over an HTTP proxy
* rhnSession
  The main class, handles authentication and session for RHN
  This class is then used as a parameter to practically all of
  the methods in the other submodules

Non-class Methods:
* getHostname(url)
  extract just the hostname part from an passed http(s) URL
* rhnifyURL(url)
  convert an https URL or hostname into the appropriate form for RHN/Satellite
* promptUser
  prompt for and return a username
* promptPass(user)
  primpt for and return a password, without echoing.
* fetchCreds(configfile, servername)
  read in credentials from an ini-style config file
* saveCreds(configfile, servername)
  save credentials to an ini-style config file, without trashing existing files.

TODO
* better handling of XMLRPC errors - at the moment we just print out the error message.
I'm sure there's a better way to manage this. Raise a proper exception, I suppose.
"""

__author__ = "Stuart Sears"

# the following controls what is imported when you do a 'from rhnapi import *'
__all__ =     [
            'activationkey',
            'api',
            'channel',
            'configchannel',
            'distchannel',
            'errata',
            'kickstart',
            'org',
            'packages',
            'preferences',
            'proxy',
            'satellite',
            'schedule',
            'system',
            'systemgroup',
            'user',
            'utils',
            ]

import xmlrpclib
import httplib
import sys
import re
import os
from ConfigParser import SafeConfigParser
import time
import logging

# these methods could all be part of the main class, but don't need to be:
# besides, who knows if I'll need them somewhere else in the future?

# ---------------------------------------------------------------------------- #

def getHostname(url):
    """
    returns a sanitised URL for RHN connection - deals with those that
    add protocols or paths to their hostnames!
    """
    urlpattern = re.compile(r'(http[s]?://)?([\w.]+)([/\w]*)')
    # strip away all but the hostname...
    hostname = urlpattern.search(url).groups()[1]

    # add  the correct start and end bits:
    return hostname

# ---------------------------------------------------------------------------- #

def rhnifyURL(url):
    """
    returns a sanitised URL for RHN connection - deals with those that
    add protocols or paths to their hostnames!
    """
    urlpattern = re.compile(r'(http[s]?://)?([\w.]+)([/\w]*)')
    # strip away all but the hostname...
    hostname = urlpattern.search(url).groups()[1]

    # add  the correct start and end bits:
    return 'https://%s/rpc/api' % hostname

# ---------------------------------------------------------------------------- #

def promptUser():
    """
    prompts for username.
    """
    rhnuser = str(raw_input('Please enter your RHN username: ')).strip()
    return rhnuser

# ---------------------------------------------------------------------------- #

def promptPass(username):
    """
    prompts for a password for an existing user
    """
    # we only need the getpass stuff if prompting for passwords.
    # This only happens on session init.
    from getpass import getpass
    rhnpass = getpass('Please enter the RHN password for user %s: ' % username)
    return rhnpass.strip()

# ---------------------------------------------------------------------------- #

def fetchCreds(filename, servername, logger=None, debug=False):
    """
    usage:
    fetchCreds(filename, servername, logger, debug=False)

    description:
    An updated method to parse a config file (originally ~/.rhninfo)
    for login and password, if present.

    uses an INI format, like this:
    [servername]
    login = LOGIN
    password = PASSWORD

    Values picked up from [DEFAULTS] if missing from a section

    returns:
    tuple: (username, password)

    parameters:
    filename(str)           - configuration file path
    servername(str)         - RHN hostname (section header)
    logger(logging.Logger)  - logger for output messages
    debug(bool)             - whether to log debug messages
    """
    # set initial values
    mylogin = None
    mypass = None

    # harmless, so just for sanity:
    srcfile = os.path.expanduser(filename)

    if logger:
        logger.debug("attempting to load credentials from %s", srcfile)

    confparse = SafeConfigParser()
    # does the file exist, if so, read from it...
    if os.path.isfile(srcfile):
        confparse.read(srcfile)
        if confparse.has_section(servername):
            if logger:
               logger.debug("found section for server %s", servername)
            mylogin = confparse.get(servername, 'login')
            mypass  = confparse.get(servername, 'password')
        else:
            if logger:
                logger.info("No section found for server %s, using defaults", servername)
    if debug and logger:
        logger.debug("using username %s from config file", mylogin)

    return str(mylogin).strip(), str(mypass).strip()

# ---------------------------------------------------------------------------- #

def saveCreds(filename, servername, logger = None, login = None, password = None):
    """
    description:
    Attempts to save login and password information to the given configfile
    could be extended for other stuff later.
    The file uses an INI format, like this:
    [servername]
    login = LOGIN
    password = PASSWORD

    Values picked up from [DEFAULTS] if missing from a section
    (most values in DEFAULTS will be 'None')

    returns:
    Bool, or throws exception

    parameters:
    filename(str)           - destination file for credential info
    servername(str)         - RHN Server hostname (section header in file)
    logger(logging.Logger)  - logger instance for error messages etc
    login(str)              - RHN login name to save [None]
    password(str)           - RHN password for login name [None]
    debug(bool)             - Enable debug logging
    """
    # handle being given '~/' as part of a filename
    dstfile = os.path.expanduser(filename)
    if logger:
        logger.debug("saving credentials to %s", dstfile) 

    # existing defaults will replace these, but just in case we're setting
    # up a new config file from scratch...
    confparse = SafeConfigParser({'login' : None, 'password' : None})

    # if the file already exists, read its contents into a configparser object:

    if os.path.isfile(dstfile):
        confparse.read(dstfile)

    # otherwise the file doesn't exist, so we can create it from scratch
    try:
        fd = open(dstfile, 'w')
    except IOError:
        if logger:
            logger.exception("unable to open file %s for writing", dstfile)
        
    # add a section for our hostname, if missing
    if not confparse.has_section(servername):
        if logger:
            logger.debug("Adding section for %s", servername)
        confparse.add_section(servername)

    # now make settings as appropriate. Existing settings will be replaced
    if login is not None:
        confparse.set(servername, 'login', str(login))
    if password is not None:
        confparse.set(servername, 'password', str(password))
    try:
        # write out our in-memory config to disk
        confparse.write(fd)
        fd.close()
        if logger:
            logger.info("successfully saved credentials to %s", dstfile)
        return True
    except:
        if logger:
            logger.log(logging.ERROR, "Failed to save configuration information", exc_info = 1)
        return False
    
# -------------------------- Class Definitions     --------------------------- #

class proxiedTransport(xmlrpclib.SafeTransport):
    """
    A class representing a custom transport for XMLPRC transactions via a proxy
    totally stolen from the python 2.7 docs at http://docs.python.org/library/xmlrpclib.html
    Adapted to use HTTPS...
    """
    def set_proxy(self, proxy):
        self.proxy = proxy
    # ---------------------------------------------------------------------------- #

    def make_connection(self, host):
        """
        used to use httplib.HTTPS, but the proxy is a plain HTTP connection, I think.
        """
        self.realhost = host
        h = httplib.HTTP(self.proxy)
        return h
    # ---------------------------------------------------------------------------- #

    def send_request(self, connection, handler, request_body):
        """
        replaced the original 'http' with https for RHN.
        I wonder if there's an official 'protocol placeholder
        for the 'connection' type ?

        realhost: hostname (URL?) of remote XMLRPC server
        handler: /rpc/api in this case
        """
        connection.putrequest("POST", 'https://%s%s' % (self.realhost, handler))
    # ---------------------------------------------------------------------------- #

    def send_host(self, connection, host):
        connection.putheader('Host', self.realhost)

# ---------------------------------------------------------------------------- #

class rhnSession(object):

    """
    a base RHN class. You'll need one of the other submodules for it to do anything useful.
    """

    def __init__(self, url='rhn.redhat.com', rhnlogin = None, rhnpassword = None,
                 proxyserver = None, config = None, savecreds=False, debug = False,
                 logenable = True, logfile = None, loglevel = 20, logname = 'RHN API'):
        """
        Initialize a connection to RHN (or a satellite) using the provided information.
        proxy server should be local https proxy, if available. IPaddress/Hostname:port.
        No protocol required for the proxy definition.

        returns rhnSession object

        parameters: (* = optional)
        url(str)            - hostname or ip address of the RHN server
        rhnlogin(str)       - username (prompted if omitted)
        rhnpassword(str)    - password (prompted if omitted)
        *proxyserver(str)   - HTTP proxy betweeen you and the satellite (IP or hostname only)
        *config(str)        - local configuration file, in .ini format for username and password
        *savecreds(bool)    - should we save username and passwords to our ~/.rhninfo file?
        *debug(bool)        - print out lots of horribly (and possibly insecure) information for testing.
        *logenable(bool)    - whether to enable RHN Session logging [True]
        *logfile(str)       - destination for log output [None].
                              if not specified and logging is enabled, uses stderr
        *loglevel(int)      - loglevel to set [20(INFO)]
                              (10 = debug, 20 = info, 30 = warn, 40 = error, 50 = crit/fatal)
        *logname(str)       - name to use in log messages. Defaults to 'RHN API'. Can be any string.                              
                              (for example, your script name)
        """
        # for config passing we require the hostname, let's clean up whatever we've been given:
        self.hostname = getHostname(url)
        self.rhnurl = rhnifyURL(url)
        self.login = rhnlogin
        # passwords are private variables. Cached, but not exposed
        self._password = rhnpassword

        self.debug = debug
        # in case we need it:
        self.configfile = config
        # logdestination

        # logging configuration
        self.logger = None
        self.logenable = logenable
        self.logfile = logfile
        if self.debug:
            self.loglevel = 10
        else:            
            self.loglevel = loglevel

        if self.logenable:
            if self.logfile is not None:
                self.addLogger(logname, self.logfile, self.loglevel)
            else:
                self.addLogger(logname, None, self.loglevel)

        # authentication config (order of precedence)
        # 1. login and password as args
        # 2. login and password from config file
        # 3. prompt for missing information
        # If login and/or password are specified explicitly they override the config file
        if self.login == None and self._password == None and self.configfile != None:
            self.logInfo("looking up config info in %s" % self.configfile)
            self.login, self._password = fetchCreds(self.configfile, self.hostname, self.logger, self.debug)

        # see what we got back and prompt if required:
        if str(self.login) == 'None':
            self.login = promptUser()

        if str(self._password) == 'None':
            self._password = promptPass(self.login)


        try:
            if proxyserver is not None:
                P = proxiedTransport()
                P.set_proxy(proxyserver)

                # basic session initialisation
                self.session = xmlrpclib.Server(self.rhnurl, verbose=0, transport = P)
            else:
                self.session = xmlrpclib.Server(self.rhnurl, verbose=0)

            # now we login
            self.key = self.session.auth.login(self.login, self._password)
            if isinstance(self.key, str):
                self.logDebug("initialised RHN Session, key: %s" % self.key)

            # set some version info for debug, really.
            self.sat_version = self.session.api.systemVersion()
            self.api_version = self.session.api.getVersion()
            # org ID for the currently logged-in user
            self.org_number = self.session.user.getDetails(self.key, self.login).get('org_id', None)

            if savecreds:
                if self.configfile is not None:
                    res = saveCreds(self.configfile, self.hostname, self.logger, self.login, self._password)
                    if res:
                        self.logDebug("saved credentials to %s" % self.configfile)
                    else:
                        self.logWarn("failed to save credentials to %s" % self.configfile)

            


        except xmlrpclib.Fault, E:
            self.fail(E, 'login to RHN server %s' % self.rhnurl )
            raise

# ---------------------------------------------------------------------------- #

    # def addLogger(self, logname, logdest, loglevel, logfmt = '%(asctime)s - %(name)s - %(levelname)-8s - %(message)s'):
    def addLogger(self, logname, logdest, loglevel, 
            logfmt = '%(asctime)s %(name)s[%(process)d]: %(levelname)-8s - %(message)s',
            datefmt = '%b %e %H:%M:%S'):
        """
        Generates self.logger, a logging.Logger instance.

        returns a logging.logger instance, with appropriate configuration
        supports logging to streams (sys.stdout, sys.stderr) and files.

        The assumption here is that if given a filename, we use that, otherwise we use a StreamHandler and log to
        stderr

        parameters:
        logname(str)    - name of log instance (appears in log messages). Your script name is a good choice.
        logdest(str)    - destination for log messages (sys.stdout/err or a filename (NOT filehandle))
        loglevel(int)   - log messages at this priority or higher
                          log levels are numeric, mapping like this:
                          10 -> DEBUG
                          20 -> INFO
                          30 -> WARN
                          40 -> ERROR
                          50 -> CRIT / FATAL
        """
        # set up logging
        # used later...
        broken_log = False

        # initialise a logger with the appropriate name:
        self.logger = logging.getLogger(logname)

        # set logging levels
        self.logger.setLevel(loglevel)

        # configure the format of log messages
        formatter = logging.Formatter(logfmt, datefmt)

        # we should now have a functional logger, so let's configure a destination
        # this is done by adding an appropriate handler:
        # with python 2.4 we have to wrap the try...except block in another
        # block to use the 'finally' statement for cleanup.
        try:
            if logdest is not None:
            # we were actually given a filename or path to log to
            # try and open it
                try:
                    lh = logging.FileHandler(logdest)
                    logerror = False
                except:
                    # if we can't open the file, fall back to stderr
                    lh = logging.StreamHandler()
                    logerror = True
            else:
                lh = logging.StreamHandler()
                logerror = False
        finally:
        # this should run once the outer 'try' block has completed
        # whether an exception was raised or not.
            lh.setFormatter(formatter)
            lh.setLevel(loglevel)
            if len(self.logger.handlers) == 0:
                self.logger.addHandler(lh)
            if logerror:
                self.logErr("unable to open/access log file %s, falling back to stderr" % logdest)
            if self.logger is None:
                raise RuntimeError("failed to instantiate logger")
            self.logger.debug("Logger initiated")
        

    def setLogLevel(self, loglevel = 10):
        """
        sets loglevel for the RHN logger
        """
        if self.logger is not None:
            self.logger.setLevel(loglevel)

    # ---------------------------------------------------------------------------- #

    def logMessage(self, loglevel, message):
        """
        Write a log message

        passes if this fails, as failed logging should not fail everything else.

        parameters
        loglevel(int)       - log priority. Can be logging.INFO (etc) or numeric
        message(str)        - the actual message to send.
        """
        if self.logger is not None:
            self.logger.log(loglevel, message)
    
    def logInfo(self, message):
        """
        logs at INFO priority
        """
        if self.logger is not None:
            self.logger.info(message)

    def logDebug(self, message):
        """
        Shortcut for DEBUG level logging
        """
        if self.logger is not None:
            self.logger.debug(message)

    def logCrit(self, message):
        """
        Shortcut for CRITICAL level logging
        """
        if self.logger is not None:
            self.logger.critical(message)

    def logWarn(self, message):
        """
        logs a message at WARN priority
        """
        if self.logger is not None:
            self.logger.warn(message)

    def logFatal(self, message):
        """
        shortcut to FATAL (emerg-ish) level logging
        """
        if self.logger is not None:
            self.logger.fatal(message)

    def logErr(self, message):
        """
        ERROR level logging
        """
        if self.logger is not None:
            self.logger.error(message)

    def logError(self, message):
        """
        ERROR level logging
        """
        if self.logger is not None:
            self.logger.error(message)

    def fail(self, exptn, message):
        """
        Generic failure handler
        logs and re-raises the exception passed to it
        """
        try:
            self.logErr("Failed to %s" % message)
            raise exptn
        except xmlrpclib.Fault, E:
            self.logErr(str(exptn.faultCode).strip())
            self.logErr(str(exptn.faultString).strip())
        except Exception, E:
            self.logErr(str(E))
        # raise
        return False

    def close(self):
        """
        close an opened RHN session. Arguably not required, but still...
        """
        try:
            self.session.auth.logout(self.key)
        except Exception, E:
            self.fail(E, 'logout user %s' % self.login)

    def getSatelliteVersion(self):
        """
        return the satellite version in use.
        """
        return self.session.api.systemVersion()

    def getRHNUser(self):
        """
        return the user currently logged in via rhnSession
        """
        return self.login

    def getApiVersion(self):
        """
        return the RHN API version in use.
        """
        return self.session.api.getVersion()

    def enableDebug(self):
        """
        enable debug output
        """
        self.debug = True
        if self.logger is not None:
            self.logger.setLevel(logging.DEBUG)

    def disableDebug(self):
        """
        disable debug output
        """
        self.debug = False
        # go back to Info Logging
        if self.logger is not None:
            self.logger.setLevel(logging.WARN)
            
    def enableVerbose(self):
        """
        Verbose Logging
        """
        self.verbose = True
        if self.logger is not None:
            self.logger.setLevel(logging.INFO)
            self.logger.info("loglevel set to INFO")

    def disableVerbose(self):
        """
        disable verbose logging
        """
        self.verbose = False
        if self.logger is not None:
            self.logger.setLevel(logging.WARN)

    def renewSession(self):
        """
        Renews an expired session
        """
        self.key = self.session.auth.login(self.login, self._password)

    def logout(self):
        """
        logout of the session (expires the session key)
        """
        try:
            res = self.session.auth.logout(self.key)
            if res == 1:
                return True
        except Exception, E:
            return self.fail(E, '%s logout failed!' % self.username)

    def encodeDate(self, datestr = None):
        """
        returns an xmlrpclib.DateTime object for all those methods that require one.
        Defaults to current date/time if this is not provided.
        """
        if datestr is not None:
            try:
                time.strptime(datestr, '%Y%m%dT%H:%M:%S')
                return xmlrpclib.DateTime(datestr)
            except ValueError, E:
                return self.fail(E, 'encode date. Error: %s' % E.args[0]) 
        else:
            return xmlrpclib.DateTime()
    
    def decodeDate(self, rpcdate, timefmt = '%Y-%m-%d %H:%M:%S'):
        """
        decode an XMLRPC DateTime object to a string in the appropriate format.
        Time format defaults to YYYY-MM-DD HH:MM:SS

        parameters:
        rpcdate(xmlrpclib.DateTime) object
        timefmt(str)
        """
        tt = time.strptime(rpcdate.value, '%Y%m%dT%H:%M:%S')
        return time.strftime(timefmt, tt)


class rhnException(Exception):
    """
    An attempt to customise the exception handling
    current known codes:
    -1  : no such session (expiry)
    -210: channel does not exist
    2905: username/password fail
    """

    def __init__(self, value, *args, **kwargs):
        """
        initialisation code for our custom exception
        """
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)

# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
