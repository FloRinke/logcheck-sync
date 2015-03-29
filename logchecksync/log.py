"""logging utilities and definitions"""

__author__ = 'Florian Rinke'

import logging
import sys

LOG = logging.getLogger(__name__)


def configure_general():
    """configure logger"""
    logging.addLevelName(15, 'NOTICE')
    LOG.setLevel(logging.DEBUG)

    chan = logging.StreamHandler(sys.stderr)
    chan.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # formatter = logging.Formatter("%(levelname)s: %(message)s")
    chan.setFormatter(formatter)

    LOG.addHandler(chan)


configure_general()
# LOG.debug('debug message')
#LOG.info('info message')
#LOG.warn('warn message')
#LOG.error('error message')
#LOG.critical('critical message')
