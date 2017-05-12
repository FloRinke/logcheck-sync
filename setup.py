#!/usr/bin/env python3
import os

from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(name="logchecksync",
      version="0.2",
      author="Florian Rinke",
      author_email="github+logchecksync@florianrinke.de",
      description="Sync logcheck-rules from git-repository",
      license="",
      keywords="logcheck sync configuration management",
      url="https://github.com/FloRinke/logchecksync",
      packages=['logchecksync'],
      scripts=['bin/logchecksync'],
      data_files=[('/etc/logchecksync', ['logchecksync/logchecksync.conf']),
                  ('/var/lib/logchecksync', ['logchecksync/logging.conf'])
                  ],
      include_package_data=True,
      long_description=read('README.md'),
      classifiers=["Development Status :: 4 - Beta",
                   "Topic :: System :: Systems Administration",
                   "License :: OSI Approved :: BSD License",
                   "Programming Language :: Python :: 3",
                   "Operating System :: POSIX :: Linux",
                   "Intended Audience :: System Administrators",
                   ],
      requires=['nose']
      )
