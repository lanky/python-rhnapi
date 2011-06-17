#!/usr/bin/env python
# -*- coding: utf-8 -*-
# schedule.py
# Author: Stuart Sears <sjs@redhat.com>
"""
rhnapi.schedule

An abstraction of the 'schedule' namespace within the RHN Satellite API, 
created for RHN Satellite 5.4
"""

def cancelActions(rhn, action_ids):
    """
    API: schedule.cancelActions

    usage: cancelActions(rhn, action_ids)

    description: 
    Cancel all actions in given list. If an invalid action is provided,
    none of the actions given will canceled.

    returns:
    Bool, or throws exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    action_ids(list/str)     - list of scheduled action id numbers
    """
    try:
        return rhn.session.schedule.cancelActions(rhn.key, action_ids) == 1
    except Exception, E:
        return rhn.fail(E, 'Cancel one or more of the specified scheduled actions')

def listAllActions(rhn):
    """
    API: schedule.listAllActions

    usage: listAllActions(rhn)

    description:
    Lists all scheduled actions. This includes completed, in progress, failed and archived actions. 

    returns:
    list of dict, one per action
        

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.schedule.listAllActions(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list all scheduled actions')

def listArchivedActions(rhn):
    """
    API: schedule.listArchivedActions

    usage: listArchivedActions(rhn)

    description:
    lists all archived scheduled actions

    returns:
    list of dict, one per action
    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.schedule.listArchivedActions(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list archived scheduled actions')

def listCompletedActions(rhn):        
    """
    API: schedule.listCompletedActions

    usage: listCompletedActions(rhn)

    description:
    lists all scheduled actions that have been completed

    returns:
    list of dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.schedule.listCompletedActions(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list completed scheduled actions')

def listCompletedSystems(rhn, action_id):
    """
    API: schedule.listCompletedSystems

    usage: listCompletedSystems(rhn, action_id)

    description:
    lists systems that have completed a specific action

    returns:
    list of dict, one per system

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    action_id(int)           - the scheduled action ID
    """
    try:
        return rhn.session.schedule.listCompletedSystems(rhn.key, action_id)
    except Exception, E:
        return rhn.fail(E, 'list systems that have completed action %d' % action_id)

def listFailedActions(rhn):
    """
    API: schedule.listFailedActions

    usage: listFailedActions(rhn)

    description:
    lists scheduled actions that failed.

    returns:
    list of dict, one per action
    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.schedule.listFailedActions(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list failed actions')

def listFailedSystems(rhn, action_id):
    """
    API: schedule.listFailedSystems

    usage: listFailedSystems(rhn, action_id)

    description:
    lists systems on which the specifed action failed

    returns:
    list of dict, one per system
    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    action_id(int)           - the scheduled action ID
    """
    try:
        return rhn.session.schedule.listFailedSystems(rhn.key, action_id)
    except Exception, E:
        return rhn.fail(E, 'list failed systems for scheduled action %d' % action_id)

def listInProgressActions(rhn):
    """
    API: schedule.listInProgressActions

    usage: listInProgressActions(rhn)

    description:
    lists scheduled actions that are in progress

    returns:
    list of dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    """
    try:
        return rhn.session.schedule.listInProgressActions(rhn.key)
    except Exception, E:
        return rhn.fail(E, 'list scheduled actions currently in progress')

    
def listInProgressSystems(rhn, action_id):
    """
    API: schedule.listInProgressSystems

    usage: listInProgressSystems(rhn)

    description:
    lists systems on which the specified scheduled action is in progress

    returns:
    list of dict

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    action_id(int)           - the scheduled action ID
    """
    try:
        return rhn.session.schedule.listInProgressSystems(rhn.key, action_id)
    except Exception, E:
        return rhn.fail(E, 'list systems on which the schedule actions id %d is currently in progress' % action_id)

def rescheduleActions(rhn, action_ids, only_failed = True):
    """
    API: schedule.rescheduleActions

    usage: rescheduleActions(rhn, action_ids, only_failed)

    description:
    reschedule the given list of actions

    returns:
    Bool, or throws exception

    parameters:
    rhn                      - authenticated rhnapi.rhnSession() object
    action_ids(list/int)     - list of action IDs to reschedule
    only_failed(bool)        - only reschedule failed actions (True)
    """
    try:
        return rhn.session.schedule.rescheduleActions(rhn.key, action_ids, only_failed)
    except Exception, E:
        return rhn.fail(E, 'reschedule actions')
