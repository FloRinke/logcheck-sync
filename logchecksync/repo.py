"""Access to git repository"""
__author__ = 'Florian Rinke'

import os
import logging

from git import Repo

from logchecksync.config import get_system

LOG = logging.getLogger(__name__)


def repo_pull():
    """refresh local repo from remote"""
    LOG.log(15, 'Starting repo synchronisation')
    print('Starting repo synchronisation')
    if not os.path.isdir(get_system('repo_dir')):
        LOG.log(15, ' creating repo dir [%s]', get_system('repo_dir'))
        print(' creating repo dir [{0}]'.format(get_system('repo_dir')))
        os.makedirs(get_system('repo_dir'))
    if not os.path.isdir(os.path.join(get_system('repo_dir'), '.git')):
        LOG.log(15, ' cloning repo from %s', get_system('repo_remote'))
        print(' cloning repo from {0}'.format(get_system('repo_remote')))
        Repo.clone_from(get_system('repo_remote'), get_system('repo_dir'))
        # repo = Repo.clone_from(GITREPO, REPODIR)
    else:
        LOG.log(15, ' refreshing repo from %s', get_system('repo_remote'))
        print(' refreshing repo from {0}'.format(get_system('repo_remote')))
        Repo(get_system('repo_dir')).remotes.origin.pull()
        # repo.remotes.origin.pull()
    return
