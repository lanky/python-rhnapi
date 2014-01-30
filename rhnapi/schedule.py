#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RHN/Spacewalk API Module abstracting the 'schedule' namespace
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
rhnapi.schedule

An abstraction of the 'schedule' namespace within the RHN Satellite API, 
created for RHN Satellite 5.4
"""
__author__ = "Stuart Sears"

# ---------------------------------------------------------------------------- #

def cancelActions(rhn, actionids):
    """
    API:
    schedule.cancelActions

    usage:
    cancelActions(rhn, actionids)

    description: 
    Cancel all actions in given list. If an invalid action is provided,
    none of the actions given will canceled.

    returns:
    Bool, or throws exception

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
    actionids(list/str)     - list of scheduled action id numbers
    """
    try:
        return rhn.session.schedule.cancelActions(rhn.key, actionids) == 1
    except Exception, E:
        return rhn.fail(E, 'Cancel one or more of the specified scheduled actions')

# ---------------------------------------------------------------------------- #

def listAllActions(rhn):
    """
    API:
    schedule.listAllActions

    usage:
    listAllActions(rhn)

    description:
    Lists all scheduled actions. This includes completed, in progress, failed and archived actions. 

    returns:
    list of dict, one per action
        {
          'id'(int)                 : action ID,
          'name'(str)               : action name,
          'scheduler'(str)          : user who scheduled the action,
          'earliest'(dateTime)      : earliest date for execution,
          'completedSystems' (int)  : number of systems that completed,
          'failedSystems'(int)      : number of systems that failed,
          'inProgressSystems'(int)  : number of systems still in progress,
        }
        

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.schedule.listAllActions(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list all scheduled actions')

# ---------------------------------------------------------------------------- #

def listArchivedActions(rhn):
    """
    API:
    schedule.listArchivedActions

    usage:
    listArchivedActions(rhn)

    description:
    lists all archived scheduled actions

    returns:
    list of dict, one per action
        {
          'id'(int)                 : action ID,
          'name'(str)               : action name,
          'scheduler'(str)          : user who scheduled the action,
          'earliest'(dateTime)      : earliest date for execution,
          'completedSystems' (int)  : number of systems that completed,
          'failedSystems'(int)      : number of systems that failed,
          'inProgressSystems'(int)  : number of systems still in progress,
        }

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.schedule.listArchivedActions(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list archived scheduled actions')

# ---------------------------------------------------------------------------- #

def listCompletedActions(rhn):        
    """
    API:
    schedule.listCompletedActions

    usage:
    listCompletedActions(rhn)

    description:
    lists all scheduled actions that have been completed

    returns:
    list of dict, one per action
        {
          'id'(int)                 : action ID,
          'name'(str)               : action name,
          'scheduler'(str)          : user who scheduled the action,
          'earliest'(dateTime)      : earliest date for execution,
          'completedSystems' (int)  : number of systems that completed,
          'failedSystems'(int)      : number of systems that failed,
          'inProgressSystems'(int)  : number of systems still in progress,
        }

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.schedule.listCompletedActions(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list completed scheduled actions')

# ---------------------------------------------------------------------------- #

def listCompletedSystems(rhn, actionid):
    """
    API:
    schedule.listCompletedSystems

    usage:
    listCompletedSystems(rhn, actionid)

    description:
    lists systems that have completed a specific action

    returns:
    list of dict, one per system
        {
          'server_id' (int)     : server ID,
          'server_name' (str)   : server name,
          'base_channel' (str)  : base software channel,
          'timestamp' (dateTime): time action completed
          'message' (str)       : (optional) message generated by action (stdout/stderr)
        }

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
    actionid(int)           - the scheduled action ID
    """
    try:
        return rhn.session.schedule.listCompletedSystems(rhn.key, actionid)
    except Exception, E:
        return rhn.fail(E, 'list systems that have completed action %d' % actionid)

# ---------------------------------------------------------------------------- #

def listFailedActions(rhn):
    """
    API:
    schedule.listFailedActions

    usage:
    listFailedActions(rhn)

    description:
    lists scheduled actions that failed.

    returns:
    list of dict, one per action
        {
          'id'(int)                 : action ID,
          'name'(str)               : action name,
          'scheduler'(str)          : user who scheduled the action,
          'earliest'(dateTime)      : earliest date for execution,
          'completedSystems' (int)  : number of systems that completed,
          'failedSystems'(int)      : number of systems that failed,
          'inProgressSystems'(int)  : number of systems still in progress,
        }

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.schedule.listFailedActions(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list failed actions')

def listFailedSystems(rhn, actionid):
    """
    API:
    schedule.listFailedSystems

    usage:
    listFailedSystems(rhn, actionid)

    description:
    lists systems on which the specifed action failed

    returns:
    list of dict, one per system
        {
          'server_id' (int)     : server ID,
          'server_name' (str)   : server name,
          'base_channel' (str)  : base software channel,
          'timestamp' (dateTime): time action completed
          'message' (str)       : (optional) message generated by action (stdout/stderr)
        }

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
    actionid(int)           - the scheduled action ID
    """
    try:
        return rhn.session.schedule.listFailedSystems(rhn.key, actionid)
    except Exception, E:
        return rhn.fail(E, 'list failed systems for scheduled action %d' % actionid)

# ---------------------------------------------------------------------------- #

def listInProgressActions(rhn):
    """
    API:
    schedule.listInProgressActions

    usage:
    listInProgressActions(rhn)

    description:
    lists scheduled actions that are in progress

    returns:
    list of dict, one per action
        {
          'id'(int)                 : action ID,
          'name'(str)               : action name,
          'scheduler'(str)          : user who scheduled the action,
          'earliest'(dateTime)      : earliest date for execution,
          'completedSystems' (int)  : number of systems that completed,
          'failedSystems'(int)      : number of systems that failed,
          'inProgressSystems'(int)  : number of systems still in progress,
        }

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.schedule.listInProgressActions(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list scheduled actions currently in progress')

    
# ---------------------------------------------------------------------------- #

def listInProgressSystems(rhn, actionid):
    """
    API:
    schedule.listInProgressSystems

    usage:
    listInProgressSystems(rhn)

    description:
    lists systems on which the specified scheduled action is in progress

    returns:
    list of dict, one per system
        {
          'server_id' (int)     : server ID,
          'server_name' (str)   : server name,
          'base_channel' (str)  : base software channel,
          'timestamp' (dateTime): time action completed
          'message' (str)       : (optional) message generated by action (stdout/stderr)
        }

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
    actionid(int)           - the scheduled action ID
    """
    try:
        return rhn.session.schedule.listInProgressSystems(rhn.key, actionid)
    except Exception, E:
        return rhn.fail(E, 'list systems on which the schedule actions id %d is currently in progress' % actionid)

# ---------------------------------------------------------------------------- #

def rescheduleActions(rhn, actionids, failedonly = True):
    """
    API:
    schedule.rescheduleActions

    usage:
    rescheduleActions(rhn, actionids, failedonly)

    description:
    reschedule the given list of actions

    returns:
    Bool, or throws exception

    parameters:
    rhn                     - authenticated rhnapi.rhnSession() object
    actionids(list/int)     - list of action IDs to reschedule
    failedonly(bool)        - only reschedule failed actions (True)
    """
    try:
        return rhn.session.schedule.rescheduleActions(rhn.key, actionids, failedonly) == 1
    except Exception, E:
        return rhn.fail(E, 'reschedule actions')

# footer - do not edit below here
# vim: set et ai smartindent ts=4 sts=4 sw=4 ft=python:
