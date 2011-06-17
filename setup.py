#!/usr/bin/env python
# -*- coding: utf-8 -*-
# setup script for packaging the rhnapi module
from distutils.core import setup
setup(name = 'python-rhnapi',
      version = '5.4',
      description = 'Python abstraction of the RHN Satellite XMLRPC API',
      author = 'Stuart Sears',
      author_email = 'sjs@redhat.com',
      packages = [ 'rhnapi' ],
      )


