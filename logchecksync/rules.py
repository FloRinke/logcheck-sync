"""Manage local rules and subscriptions"""
__author__ = 'Florian Rinke'

import glob
import logging
import logging.config
import os
import shutil

from logchecksync import config

LOG = logging.getLogger(__name__)


def show_status():
    """show initialization status of local configuration"""
    init_complete = False

    LOG.info("-- logchecksync data status --")
    if not os.path.isdir(config.get('data_dir')):
        LOG.info('[x] datadir missing [%s]', config.get('data_dir'))
        print('[x] datadir missing [{0}]'.format(config.get('data_dir')))
    else:
        LOG.info('[x] datadir exists [%s]', config.get('data_dir'))
        print('[x] datadir exists [{0}]'.format(config.get('data_dir')))
        if os.path.isfile(os.path.join(config.get('data_dir'), config.get('known_file'))):
            LOG.info('[x]  knownfile exists [%s]', os.path.join(config.get('data_dir'), config.get('known_file')))
            print('[x]  knownfile exists [{0}]'.format(os.path.join(config.get('data_dir'), config.get('known_file'))))
        else:
            LOG.info('[ ]  knownfile missing [%s]', os.path.join(config.get('data_dir'), config.get('known_file')))
            print('[ ]  knownfile missing [{0}]'.format(os.path.join(config.get('data_dir'), config.get('known_file'))))
        if os.path.isfile(os.path.join(config.get('data_dir'), config.get('used_file'))):
            LOG.info('[x]  usedfile exists [%s]', os.path.join(config.get('data_dir'), config.get('used_file')))
            print('[x]  usedfile exists [{0}]'.format(os.path.join(config.get('data_dir'), config.get('used_file'))))
        else:
            LOG.info('[ ] usedfile missing [%s]', os.path.join(config.get('data_dir'), config.get('used_file')))
            print('[ ] usedfile missing [{0}]'.format(os.path.join(config.get('data_dir'), config.get('used_file'))))
        if not os.path.isdir(config.get('repo_dir')):
            LOG.info('[ ] repodir missing [%s]', config.get('data_dir'))
            print('[ ] repodir missing [{0}]'.format(config.get('data_dir')))
        else:
            LOG.info('[x]  repodir exists [%s]', config.get('repo_dir'))
            print('[x]  repodir exists [{0}]'.format(config.get('repo_dir')))
            if os.path.isdir(os.path.join(config.get('repo_dir'), '.git')):
                LOG.info('[x]   containing git repository')
                print('[x]   containing git repository')
                init_complete = True
                show_used_rules()
            else:
                LOG.info('[ ]    not containing git repository [%s]', os.path.join(config.get('repo_dir'), '.git'))
                print('[ ]    not containing git repository [{0}]'.format(os.path.join(config.get('repo_dir'), '.git')))
    return init_complete


def show_used_rules():
    """show which rules are available, ack'd and in use"""
    LOG.debug('Show known and existing rules')
    print('Show known and existing rules')

    # load existing rules
    LOG.debug(' checking for rules in %s', os.path.join(config.get('repo_dir'), '*', '*'))
    existingrules = rules_load_repo()
    LOG.debug('  existing rules: %s', existingrules)

    # load known rules
    knownrules = rules_load_file(os.path.join(config.get('data_dir'), config.get('known_file')))
    LOG.debug('  known rules: %s', knownrules)

    # load used rules
    usedrules = rules_load_file(os.path.join(config.get('data_dir'), config.get('used_file')))
    LOG.debug('  used rules: %s', knownrules)

    # get system rules
    systemrules = rules_get_system()
    LOG.debug('  system rules: %s', systemrules)

    allrules = existingrules | knownrules | usedrules | systemrules
    LOG.debug('  all rules: %s', allrules)
    allsort = list(allrules)
    allsort.sort()

    maxlen = len(max(allsort, key=len)) + 2
    linespec = "|{:" + str(maxlen) + "}|{:8}|{:8}|{:8}|{:8}|"
    print(linespec.format("Element", "Repo", "known", "used", "system"))
    for item in allsort:
        print(linespec.format(item,
                              "x" if item in existingrules else "",
                              "x" if item in knownrules else "",
                              "x" if item in usedrules else "",
                              "x" if item in systemrules else ""))

    if len(systemrules - usedrules) > 0:
        LOG.warn('Your system uses repo-rules that are not marked as used": %s', systemrules - usedrules)
        print('Warning: Your system uses repo-rules that are not marked as used: {}'.format(systemrules - usedrules))


def rules_get_system():
    os.chdir(config.get('logcheck_dir'))
    rules = set()
    pattern = os.path.join('ignore.d.paranoid', config.get('logcheck_manageprefix') + '*')
    for entry in glob.glob(pattern):
        rules.add(entry)

    pattern = os.path.join('ignore.d.server', config.get('logcheck_manageprefix') + '*')
    for entry in glob.glob(pattern):
        rules.add(entry)

    pattern = os.path.join('ignore.d.workstation', config.get('logcheck_manageprefix') + '*')
    for entry in glob.glob(pattern):
        rules.add(entry)

    return rules


def rules_load_file(path):
    """load list of rules known to local system"""
    rules = set()
    if os.path.isfile(path):
        knownfile = open(path, 'r')
        rules = set(knownfile.read().splitlines())
        knownfile.close()
    return rules


def rules_save_file(rules, path):
    """save list of rules known to local system"""
    sortrules = list(rules)
    sortrules.sort()
    knownfile = open(path, 'w')
    for rule in sortrules:
        knownfile.write(rule)
        knownfile.write('\n')
    knownfile.close()


def rules_load_repo():
    """load list of rules available in local repo"""
    rules = set()
    for entry in glob.glob(os.path.join(config.get('repo_dir'), '*', '*')):
        rules.add(os.path.relpath(entry, config.get('repo_dir')))
    return rules


def rules_diff():
    """evaluate differences between locally known rules and rules available in repo"""
    LOG.debug('Compare known and existing rules')
    print('Compare known and existing rules')
    # load known rules
    knownrules = rules_load_file(os.path.join(config.get('data_dir'), config.get('known_file')))
    LOG.debug('  known rules: %s', knownrules)
    # print('  known rules: {0}'.format(knownrules))

    # load existing rules
    LOG.debug(' checking for rules in %s', os.path.join(config.get('repo_dir'), '*', '*'))
    print(' checking for rules in {0}'.format(os.path.join(config.get('repo_dir'), '*', '*')))
    existingrules = rules_load_repo()
    LOG.debug('  existing rules: %s', existingrules)
    # print('  existing rules: {0}'.format(existingrules))

    # generate diff
    newrules = existingrules - knownrules
    deletedrules = knownrules - existingrules

    if len(newrules) != 0:
        LOG.warning("There are new rules available:")
        print("There are new rules available:")
        for line in newrules:
            LOG.warning(" - %s", line)
            print(" - {0}".format(line))
        LOG.warning('use "ack" or "sync --ack" to acknowledge the change')
        print('use "ack" or "sync --ack" to acknowledge the change')

    if len(deletedrules) != 0:
        LOG.warning("Some rules were deleted:")
        print("Some rules were deleted:")
        for line in deletedrules:
            LOG.warning(" - %s", line)
            print(" - {0}".format(line))
        LOG.warning('use "ack" or "sync --ack" to acknowledge the change')
        print('use "ack" or "sync --ack" to acknowledge the change')

    if len(newrules) == 0 and len(deletedrules) == 0:
        LOG.warning("no pending changes, nothing to do")
        print("no pending changes, nothing to do")


def rules_ack():
    """acknowledge all repo-rules as known to local system"""
    LOG.info('Saving new knownfile to %s', os.path.join(config.get('data_dir'), config.get('known_file')))
    print('Saving new knownfile to {0}'.format(os.path.join(config.get('data_dir'), config.get('known_file'))))
    existingrules = rules_load_repo()
    rules_save_file(existingrules, os.path.join(config.get('data_dir'), config.get('known_file')))


def rules_list():
    """list rules local system has subscribed to"""
    rules = rules_load_file(os.path.join(config.get('data_dir'), config.get('used_file')))
    if len(rules) == 0:
        print("No rules are currently selected")
    else:
        print("These rules are currently configured for updating:")
        for rule in rules:
            print(rule)


def rules_verify(rules):
    """filter list of rules for being known to local system"""
    verifiedrules = set()
    knownrules = rules_load_file(os.path.join(config.get('data_dir'), config.get('known_file')))
    for rule in rules:
        if rule in knownrules:
            verifiedrules.add(rule)
    return verifiedrules


def rules_add(addrules):
    """add rule subscription(s) to local system"""
    LOG.info('Add rules')
    print('Add rules')
    currentrules = rules_load_file(os.path.join(config.get('data_dir'), config.get('used_file')))
    if addrules == ['all']:
        addrules = rules_load_repo()
    newrules = currentrules | rules_verify(addrules)
    rules_save_file(newrules, os.path.join(config.get('data_dir'), config.get('used_file')))


def rules_del(delrules):
    """delete rule subscriptions from local system"""
    LOG.info('Delete rules')
    print('Delete rules')
    currentrules = rules_load_file(os.path.join(config.get('data_dir'), config.get('used_file')))
    newrules = set()
    if delrules != ['all']:
        newrules = currentrules - delrules
    rules_save_file(newrules, os.path.join(config.get('data_dir'), config.get('used_file')))


def files_delete():
    """delete all managed rulefiles from system"""
    path = os.path.join(config.get('logcheck_dir'), 'ignore.d.paranoid', config.get('logcheck_manageprefix') + '*')
    # print("checking {0}".format(path))
    for entry in glob.glob(path):
        # print ("delete paranoid: {0}".format(entry))
        os.remove(entry)

    path = os.path.join(config.get('logcheck_dir'), 'ignore.d.server', config.get('logcheck_manageprefix') + '*')
    # print("checking {0}".format(path))
    for entry in glob.glob(path):
        # print ("delete server: {0}".format(entry))
        os.remove(entry)

    path = os.path.join(config.get('logcheck_dir'), 'ignore.d.workstation', config.get('logcheck_manageprefix') + '*')
    # print("checking {0}".format(path))
    for entry in glob.glob(path):
        # print ("delete workstation: {0}".format(entry))
        os.remove(entry)


def files_copy():
    """copy subscribed files to system"""
    rules = rules_load_file(os.path.join(config.get('data_dir'), config.get('used_file')))
    for entry in rules:
        src = os.path.join(config.get('repo_dir'), entry)
        dst = os.path.join(config.get('logcheck_dir'), entry)
        # print ("copy: {0} to {1}".format(src, dst))
        shutil.copy(src, dst)


def logcheck_sync():
    """sync subscribed rules"""
    print("syncing rules")
    files_delete()
    files_copy()
