"""Configuration used all over the code"""
__author__ = 'Florian Rinke'

import configparser
import logging
import os
import sys

SYSTEM = dict()

LOG = logging.getLogger(__name__)


def load_config(debug=False):
    """load configuration from local system"""
    config = configparser.ConfigParser()
    result = config.read('/etc/logcheck-sync/logcheck-sync.conf')
    LOG.info("Parsed config file: %s", result)
    print("Parsed config file: {0}".format(result))

    if not result:
        print("Cannot load config file")
        sys.exit(1)

    # config_section = None

    if debug:
        config_section = config['debug']
    else:
        config_section = config['DEFAULT']

    SYSTEM['repo_remote'] = config_section.get('repo_remote', 'https://github.com/Lemelisk/logcheck-rules.git')
    SYSTEM['data_dir'] = os.path.expanduser(config_section.get('data_dir', '~/logcheck-sync'))
    SYSTEM['repo_dir'] = os.path.expanduser(os.path.join(SYSTEM['data_dir'],
                                                         config_section.get('repo_dir', 'repo')))
    SYSTEM['logcheck_dir'] = os.path.expanduser(config_section.get('logcheck_dir', '~/logcheck-sync-root/logcheck/'))
    SYSTEM['logcheck_manageprefix'] = config_section.get('logcheck_manageprefix', 'repo-')

    SYSTEM['known_file'] = config_section.get('known', 'known')
    SYSTEM['used_file'] = config_section.get('used', 'used')


def get(name):
    """get datum from config"""
    if name in SYSTEM:
        return SYSTEM[name]
    else:
        return None

# def get_system(name):
#    """get datum from system config"""
#    if name in SYSTEM:
#        return SYSTEM[name]
#    else:
#        return None
