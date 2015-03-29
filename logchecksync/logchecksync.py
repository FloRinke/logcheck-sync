"""run program"""

__author__ = 'Florian Rinke'

import logging.config

from logchecksync.cmdline import args
from logchecksync import dispatch


def main():
    """run the module"""
    logging.config.fileConfig('logging.conf')
    dispatch.run(args)
