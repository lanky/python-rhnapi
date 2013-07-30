#!/usr/bin/env python
import sys, os
sys.path.insert(0, os.path.expanduser('~/dev/scripts/python-rhnapi'))

import rhnapi
# from rhnapi import channel
from rhnapi.decorators import logexcptn

@logexcptn
def listErr(rhn, chanlabel, **kwargs):
    """
    An attempt at wrapping the true/false return values and exception handling
    """
    # debuggery
    print kwargs.keys()
    for k in kwargs.keys():
        if not k in [ 'start_date', 'end_date' ]:
            del kwargs[k]
    return rhn.session.channel.software.listErrata(rhn.key, chanlabel, **kwargs)


def main():
    RHN = rhnapi.rhnSession('localhost', logenable=True, loglevel=10, config='~/.rhninfo')
    # this channel exists
    RHN.logInfo("listing errata for 'lgb-4.0-base-x86_64-dev'")
    myerr = listErr(RHN, 'lgb-4.0-base-x86_64-dev')
    # this doesn't
    othererr = listErr(RHN, 'lgb-40-base-x86_64-dev')


if __name__ == '__main__':
    main()
    
