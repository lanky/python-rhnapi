======
README
======

Introduction
------------
This directory contains a number of python scripts that together make up an (almost) complete abstraction of the RHN (Hosted and Satellite) XMLRPC API and by extension, that of the Spacewalk project.

Due to the divergence of the 2 codebases, there are no guarantees that this will work at all for RHN Hosted without a little TLC in some places.

This is under fairly heavy development but is more or less up to date with the published API for RHN Satellite 5.4.1

The module is designed around a single class and lots of submodules, essentially one per major namespace of the API

There is a companion repository to this one that contains a lot of scripts to automate manual tasks (or those missing from the RHN Satellite web gui or API)
You'll find that in the *spw-api-scripts* repository, also on my github.

License
-------
All of the module is released under the terms of the GNU General Public License (GPL) v.2 or greater (should any files be missing this information).

Design
------
The API module is split into multiple files (see module contents below). 

The main RHN API session class (rhnapi.rhnSession) is in the __init__.py file.

An instance of this is used by all the other methods defined in the various files. See the *USAGE* part later

Building RPMs
-------------
The repository contains configuration that uses the internal python *distutils* module to build RPMs. These will deploy the API to your python site-packages directory, so it's instantly available to python scripts, if wanted.

The RPM building process is thus:

1. Edit the ``setup.cfg`` file to update the RPM release tag (or simply pass ``--release RELEASENUMBER`` in the next command)
2. ``python setup.py bdist_rpm``
3. Find your newly build RPM in the ``dist`` directory.


Module Contents
---------------

* __init__.py

The main rhnSession class defnition with helper functions from the parent directory of this one.
``pydoc rhnapi`` should show its internal documentation.

Each of the following files provides one of the major namespaces in the API.
Where possible I have collapsed the namespaces as they were extremely (and to my mind overly) complicated.
i.e. channel includes channel.software etc.

Doing this has naturally involved renaming a few calls as otherwise the names would clash. All the calls are documented  - *pydoc modulename* is your friend here. Or a good old text editor, of course.

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

The *utils* submodule contains additional functions that are used in the scripts, to avoid too much repetition

Usage 
-----

How to use the module in your own scripts.

#. Make sure it is on your PYTHONPATH.
   This can be accomplished in one of 2 ways:

   i. Build the module into am RPM package (see *Building RPMS* above) and install that, which should put everything into the right place for you.

   ii. put the contained *rhnapi* directory in /usr/lib/python<VERSION>/site-packages.

   iii. put it in another directory (e.g. /usr/local/lib/python/site-packages) and add that to your search path in your scripts, like this:

::

  #!/usr/bin/env/python
  import sys
  sys.path.append('/usr/local/lib/python/site-packages')

or ::

  export PYTHONPATH=/usr/local/lib/python/site-packages


#. Before you can do anything, you'll need to import the module

::

  import rhnapi

#. To ease typing, the module supports the use of a config file in .ini format, defaulting to '~/.rhninfo'.
This should look like the example below (you can include sections for different satellites if you wish. Each [] section should contain only one hostname.
No regexes, URLS, protocols or any other funny business are supported. Just hostnames. Although I may add some of that in the end, if I get around to it. (Who *really* has so many satellite/spacewalk servers that they can't handle one section each?)

sample ~/.rhninfo::

  [DEFAULTS]
  login=None
  password=None
  
  [your.satellite.hostname]
  login=xxxxx
  password=xxxx

If you miss out the password=xxxxx bit (or leave it set to None), you'll be prompted for it.

4. create an instance of the rhnSession class

::

  RHN = rhnapi.rhnSession(server, config='~/.rhninfo')

5. Import the other bits you want

::

   from rhnapi import system

6. Each of the different methods requires an rhnSession to be given to it (made it easier to split everything up), so

::

  system.listSystems(RHN)

Should do what it says on the tin.


Happy Scripting
