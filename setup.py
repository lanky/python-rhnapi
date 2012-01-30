#!/usr/bin/env python
# -*- coding: utf-8 -*-
# setup script for packaging the rhnapi module
from distutils.core import setup
setup(name = 'python-rhnapi',
      version = '5.4.1',
      description = 'Python abstraction of the RHN Satellite XMLRPC API',
      long_description = 'A Python abstraction of the RHN Satellite XMLRPC API, written to assist with accessing the API from python scripts. Much of the API has been collapsed into simple namespaces. This is under heavy development and some functionality may be limited.',
      author = 'Stuart Sears',
      author_email = 'sjs@redhat.com',
      packages = [ 'rhnapi' ],
      license = 'GPL v2+'
      )


