__author__ = 'Florian Rinke'

import os
import argparse
import glob
import logging

from git import Repo



# TODO move config to extra file (in /etc)

CONFIG_DATADIR = '~/logcheck-sync'
CONFIG_REPODIR = 'repo'

GITREPO = "https://github.com/Lemelisk/logcheck-rules.git"

DATADIR = os.path.expanduser(CONFIG_DATADIR)
REPODIR = os.path.expanduser(os.path.join(CONFIG_DATADIR, CONFIG_REPODIR))

KNOWN_FILE = 'known'
USED_FILE = 'used'

# configurable logging
log = logging.getLogger('main')
logging.addLevelName(15, 'NOTICE')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
formatter = logging.Formatter("%(levelname)s: %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)


def show_status():
    if log.level > logging.INFO:
        log.setLevel(logging.INFO)

    log.info("-- logcheck-sync data status --")
    if not os.path.isdir(DATADIR):
        log.info('datadir missing [{0}]'.format(DATADIR))
    else:
        log.info('datadir existing [{0}]'.format(DATADIR))
        if os.path.isfile(os.path.join(DATADIR, KNOWN_FILE)):
            log.info('  knownfile exists [{0}]'.format(os.path.join(DATADIR, KNOWN_FILE)))
        else:
            log.info('  knownfile missing [{0}]'.format(os.path.join(DATADIR, KNOWN_FILE)))
        if os.path.isfile(os.path.join(DATADIR, USED_FILE)):
            log.info('  usedfile exists [{0}]'.format(os.path.join(DATADIR, USED_FILE)))
        else:
            log.info('  usedfile missing [{0}]'.format(os.path.join(DATADIR, USED_FILE)))
        if not os.path.isdir(REPODIR):
            log.info('  repodir missing [{0}]'.format(DATADIR))
        else:
            log.info('  repodir exists [{0}]'.format(REPODIR))
            if os.path.isdir(os.path.join(REPODIR, '.git')):
                log.info('    containing git repository')
            else:
                log.info('    not containing git repository [{0}]'.format(os.path.join(REPODIR, '.git')))


def check_pull():
    if not os.path.isdir(DATADIR):
        os.makedirs(DATADIR)
    return True


def check_ack(output=True):
    retval = True
    if not check_pull():
        retval = False
    if not os.path.isdir(os.path.join(REPODIR, '.git')):
        if output:
            log.error("no repo, sync first")
        retval = False
    return retval


def check_add(output=True):
    retval = True
    if not check_ack(output):
        retval = False
    if not os.path.isfile(os.path.join(DATADIR, KNOWN_FILE)):
        if output:
            log.error("no rulefiles known, ack first")
        retval = False
    return retval


def check_del(output=True):
    return check_add(output)


def check_list(output=True):
    return check_add(output)


def check_sync(output=True):
    retval = True
    if not check_add(output):
        retval = False
    if not os.path.isfile(os.path.join(DATADIR, USED_FILE)):
        if output:
            log.error("no rulefiles selected, add some first")
        retval = False
    return retval


def repo_pull():
    log.log(15, 'Starting repo synchronisation')
    if not os.path.isdir(REPODIR):
        log.log(15, ' creating repo dir {0}'.format(REPODIR))
        os.makedirs(REPODIR)
    if not os.path.isdir(os.path.join(REPODIR, '.git')):
        log.log(15, ' cloning repo from {0}'.format(GITREPO))
        Repo.clone_from(GITREPO, REPODIR)
        # repo = Repo.clone_from(GITREPO, REPODIR)
    else:
        log.log(15, ' refreshing repo from {0}'.format(GITREPO))
        Repo(REPODIR).remotes.origin.pull()
        # repo.remotes.origin.pull()
    return


def rules_load_file(path):
    rules = set()
    if os.path.isfile(path):
        knownfile = open(path, 'r')
        rules = set(knownfile.read().splitlines())
        knownfile.close()
    return rules


def rules_save_file(rules, path):
    sortrules = list(rules)
    sortrules.sort()
    knownfile = open(path, 'w')
    for rule in sortrules:
        knownfile.write(rule)
        knownfile.write('\n')
    knownfile.close()


def rules_load_repo():
    rules = set()
    for entry in glob.glob(os.path.join(REPODIR, '*', '*')):
        rules.add(os.path.relpath(entry, REPODIR))
    return rules


def rules_diff():
    log.debug('Compare known and existing rules')
    # load known rules
    knownrules = rules_load_file(os.path.join(DATADIR, KNOWN_FILE))
    log.debug('  known rules: {0}'.format(knownrules))

    #load existing rules
    log.debug(' checking for rules in {0}'.format(os.path.join(REPODIR, '*', '*')))
    existingrules = rules_load_repo()
    log.debug('  existing rules: {0}'.format(existingrules))

    #generate diff
    newrules = existingrules - knownrules
    deletedrules = knownrules - existingrules

    if len(newrules) != 0:
        log.warning("There are new rules available:")
        for line in newrules:
            log.warning(" - {0}".format(line))
        log.warning("use --ack to acknowledge the change")

    if len(deletedrules) != 0:
        log.warning("Some rules were deleted:")
        for line in deletedrules:
            log.warning(" - {0}".format(line))
        log.warning("use --ack to acknowledge the change")


def rules_ack():
    log.info('Saving new knownfile to {0}'.format(os.path.join(DATADIR, KNOWN_FILE)))
    existingrules = rules_load_repo()
    rules_save_file(existingrules, os.path.join(DATADIR, KNOWN_FILE))


def rules_list():
    rules = rules_load_file(os.path.join(DATADIR, USED_FILE))
    if len(rules) == 0:
        print("No rules are currently selected")
    else:
        print("These rules are currently configured for updating:")
        for rule in rules:
            print(rule)


def rules_verify(rules):
    verifiedrules = set()
    knownrules = rules_load_file(os.path.join(DATADIR, KNOWN_FILE))
    for rule in rules:
        if rule in knownrules:
            verifiedrules.add(rule)
    return verifiedrules


def rules_add(addrules):
    log.info('Add rules')
    currentrules = rules_load_file(os.path.join(DATADIR, USED_FILE))
    if addrules == ['all']:
        addrules = rules_load_repo()
    newrules = currentrules | addrules
    rules_save_file(newrules, os.path.join(DATADIR, USED_FILE))


def rules_del(delrules):
    log.info('Delete rules')
    currentrules = rules_load_file(os.path.join(DATADIR, USED_FILE))
    newrules = set()
    if delrules != ['all']:
        newrules = currentrules - delrules
    rules_save_file(newrules, os.path.join(DATADIR, USED_FILE))


def logcheck_sync():
    pass
    # TODO implement management of actual logcheck rules


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronizes logcheck rules from a git repository')
    subparsers = parser.add_subparsers(help='One of these Commands', metavar='command', dest='command')
    parser_status = subparsers.add_parser('status', help='Show Status')
    parser_sync = subparsers.add_parser('pull', help='synchronize repo')
    parser_ack = subparsers.add_parser('ack', help='acknowledge new rulefiles without adding/deleting')
    parser_list = subparsers.add_parser('list', help='list rulefile to sync')
    parser_add = subparsers.add_parser('add', help='add a rulefile to sync')
    parser_add.add_argument('rulefile', help='list of rulefiles to add', nargs='+')
    parser_del = subparsers.add_parser('del', help='delete a rulefile from sync')
    parser_del.add_argument('rulefile', help='list of rulefiles to add', nargs='+')
    parser_sync = subparsers.add_parser('sync', help='synchronize repo and selected rules')
    parser_sync.add_argument('-a', '--ack', help='also acknowledge new rulefiles', action='store_true')
    args = vars(parser.parse_args())

    log.info(args)

    if args['command'] == 'status':
        show_status()
        check_sync()

    elif args['command'] == 'pull':
        check_pull()
        repo_pull()
        rules_diff()

    elif args['command'] == 'ack':
        if not check_ack():
            exit(1)
        rules_ack()

    elif args['command'] == 'list':
        check_list()
        rules_list()

    elif args['command'] == 'add':
        check_add()
        print(args)
        rules_add(args['rulefile'])

    elif args['command'] == 'del':
        check_del()
        print(args)
        # rules_del(args['rulefile'])

    elif args['command'] == 'sync':
        if not check_pull():
            exit(1)
        repo_pull()
        if args['ack']:
            rules_ack()
        if not check_sync():
            exit(1)
        logcheck_sync()

    exit(0)