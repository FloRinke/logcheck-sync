#!/usr/bin/env python
"""lochchecksync startup wrapper"""
__author__ = 'Florian Rinke'

import sys

import logchecksync


if __name__ == '__main__':
    sys.exit(logchecksync.main())
