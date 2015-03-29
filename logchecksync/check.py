"""Various checks for other modules"""

__author__ = 'Florian Rinke'

import os
import logging

from logchecksync.config import get_system


LOG = logging.getLogger(__name__)


def check_pull():
    """check preconditions for action git pull"""
    if not os.path.isdir(get_system('data_dir')):
        os.makedirs(get_system('data_dir'))
    return True


def check_ack(output=True):
    """check preconditions for acknowledging rules as known"""
    retval = True
    if not check_pull():
        retval = False
    if not os.path.isdir(os.path.join(get_system('repo_dir'), '.git')):
        if output:
            LOG.error("no repo, sync first")
            print("no repo, sync first")
        retval = False
    return retval


def check_add(output=True):
    """check preconditions for adding subscriptions"""
    retval = True
    if not check_ack(output):
        retval = False
    if not os.path.isfile(os.path.join(get_system('data_dir'), get_system('known_file'))):
        if output:
            LOG.error("no rulefiles known, ack first")
            print("no rulefiles known, ack first")
        retval = False
    return retval


def check_del(output=True):
    """check preconditions for deleting subscriptions"""
    return check_add(output)


def check_list(output=True):
    """check preconditions for listing subscriptions"""
    return check_add(output)


def check_sync(output=True):
    """check preconditions for syncing subscribed files"""
    retval = True
    if not check_add(output):
        retval = False
    if not os.path.isfile(os.path.join(get_system('data_dir'), get_system('used_file'))):
        if output:
            LOG.error("no rulefiles selected, add some first")
            print("no rulefiles selected, add some first")
        retval = False
    return retval
