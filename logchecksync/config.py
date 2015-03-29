"""Configuration used all over the code"""
__author__ = 'Florian Rinke'

import os

# global defaults

CONFIG_DATADIR = '~/logcheck-sync'
CONFIG_REPODIR = 'repo'
CONFIG_LOGCHECKDIR = '~/logcheck-sync-root/logcheck/'

#do not edit below here unless you know what you are doing

SYSTEM = dict()
SYSTEM['repo_remote'] = "https://github.com/Lemelisk/logcheck-rules.git"

SYSTEM['data_dir'] = os.path.expanduser(CONFIG_DATADIR)
SYSTEM['repo_dir'] = os.path.expanduser(os.path.join(CONFIG_DATADIR, CONFIG_REPODIR))
SYSTEM['logcheck_dir'] = os.path.expanduser(CONFIG_LOGCHECKDIR)
SYSTEM['logcheck_manageprefix'] = 'repo-'

SYSTEM['known_file'] = 'known'
SYSTEM['used_file'] = 'used'


def load_config():
    """load configuration from local system"""
    pass


def get(name):
    """get datum from config"""
    if name in SYSTEM:
        return get_system(name)


def get_system(name):
    """get datum from system config"""
    if name in SYSTEM:
        return SYSTEM[name]
    else:
        return None
