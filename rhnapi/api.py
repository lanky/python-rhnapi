#!/usr/bin/env python
# -*- coding: utf-8 -*-
# api.py
# an abstraction of the 'api' namespace from the RHN satellite XMLRPC API (5.4+)
# all of these require an authenticated RHN session from rhnapi.rhnSession
#    * getApiCallList
#    * getApiNamespaceCallList
#    * getApiNamespaces
#    * getVersion
#    * systemVersion

def getApiCallList(rhn):
    """
    Lists all available api calls grouped by namespace

    returns: list (dict)

    params:
    rhn               - authenticated rhnapi.rhnSession
    """
    try:
        return rhn.session.api.getApiCallList(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'unable to retrieve API call list')

def getApiNamespaceCallList(rhn, namespace):        
    """
    Lists all available api calls for the given namespace

    returns: list (dict)

    params:
    rhn               - authenticated rhnapi.rhnSession
    """
    try:
        return rhn.session.api.getApiNamespaceCallList(rhn.key, namespace)
    except Exception, E:
        return rhn.fail(E, 'get api calls for namespace %s' % namespace)

def getApiNamespaces(rhn):
    """
    Lists all available api namespaces

    returns: list (dict)

    params:
    rhn               - authenticated rhnapi.rhnSession
    """
    try:
        return rhn.session.api.getApiNamespaces(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'get api namespace list')

def getVersion(rhn):
    """
    returns the api version
    """
    return rhn.session.api.getVersion()


def systemVersion(rhn):
    """
    returns the server version
    """
    return rhn.session.api.systemVersion()


