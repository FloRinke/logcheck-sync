"""Access to git repository"""
__author__ = 'Florian Rinke'

import logging
import os

from git import Repo

from logchecksync import config

LOG = logging.getLogger(__name__)


def repo_pull():
    """refresh local repo from remote"""
    LOG.log(15, 'Starting repo synchronisation')
    print('Starting repo synchronisation')
    if not os.path.isdir(config.get('repo_dir')):
        LOG.log(15, ' creating repo dir [%s]', config.get('repo_dir'))
        print(' creating repo dir [{0}]'.format(config.get('repo_dir')))
        os.makedirs(config.get('repo_dir'))
    if not os.path.isdir(os.path.join(config.get('repo_dir'), '.git')):
        LOG.log(15, ' cloning repo from %s', config.get('repo_remote'))
        print(' cloning repo from {0}'.format(config.get('repo_remote')))
        Repo.clone_from(config.get('repo_remote'), config.get('repo_dir'))
        # repo = Repo.clone_from(GITREPO, REPODIR)
    else:
        LOG.log(15, ' refreshing repo from %s', config.get('repo_remote'))
        print(' refreshing repo from {0}'.format(config.get('repo_remote')))
        Repo(config.get('repo_dir')).remotes.origin.pull()
        # repo.remotes.origin.pull()
    return
