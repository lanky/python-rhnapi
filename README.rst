======
README
======

Introduction
------------
This directory contains a number of python scripts that together make up an
(almost) complete abstraction of the RHN (Hosted and Satellite) XMLRPC API and by extension, that of the Spacewalk project.

Due to the divergence of the 2 codebases, there are no guarantees that this
will work at all for RHN Hosted without a little TLC in some places.

This is under fairly heavy development and is currently being updated to
work with RHN satellite 5.4 (which added a huge number of new API calls)

The module is designed around a single class and lots of submodules, essentially one per major namespace of the API

There is a companion repository to this one that contains a lot of scripts to automate manual tasks (or those missing from the RHN Satellite web gui or API)
You'll find that in the *spw-api-scripts* repository

License
-------
All of the module is released under the terms of the GNU General Public License (GPL) v.2 or greater. Should any files be missing this information.

Design
------

The API module is split into multiple files (see module contents below).
The main RHN API session class (rhnapi.rhnSession) is in the __init__.py file.
An instance of this is used by all the other methods defined in the various files.
see the USAGE part later


Module Contents
---------------

* __init__.py
  The main rhnSession class defnition with helper functions
  from the parent directory of this one,
  pydoc rhnapi
  should give you the lowdown.

Each of the following files provides one of the major namespaces in the API.
Where possible I have collapsed the namespaces as they were extremely (and to my mind overly) complicated.
i.e. channel includes channel.software etc.

Doing this has naturally involved renaming a few calls as otherwise the names would clash.

Some of the namespaces also include custom methods which are not part of the normal API.

* activationkey.py
* api.py
* channel.py
* configchannel.py
* distchannel.py
* errata.py
* kickstart.py
* packages.py
* preferences.py
* proxy.py
* satellite.py
* systemconfig.py
* systemgroup.py
* system.py
* user.py


* utils.py
  The utils submodule was intended to allow me to add custom functionality to the module

Usage 
-----

How to use the module in your own scripts.

1. Make sure it is on your PYTHONPATH.
    - accomplish this in one of 2 ways:
    a) put it in /usr/lib(64)/python$VERSION/site-packages
    b) put it in another directory (e.g. /usr/local/lib/python/site-packages) and add that to your search path in your scripts, like this:
    #!/usr/bin/env/python
    import sys
    sys.path.append('/usr/local/lib/python/site-packages')

2. Before you can do anything, you'll need to import the module
    import rhnapi

3. to ease typing, the module supports the use of a config file in .ini format, defaulting to '~/.rhninfo'
this should look like this (you can include sections for different satellites if you wish. Each [] section should contain only one hostname.
No regex or protocol bits or any other funny business.

sample ~/.rhninfo::

  [DEFAULTS]
  
  login=None
  
  password=None
  
  [your.satellite.hostname]
  
  login=xxxxx
  
  password=xxxx

if you miss the password=xxxxx bit (or leave it set to None), you'll be prompted for it.

4. create an instance of the rhnSession class:
    RHN = rhnapi.rhnSession(server, config='~/.rhninfo')

5. Import the other bits you want
    e.g.
    from rhnapi import system

6. Each of the different methods requires an rhnSession to be given to it (made it easier to split everything up)

    so:
        system.listSystems(RHN)

    should do what it says on the tin


Happy Scripting
