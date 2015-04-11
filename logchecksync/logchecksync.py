"""run program"""

__author__ = 'Florian Rinke'

from logchecksync import check
from logchecksync import rules
from logchecksync import repo


def run(args):
    """Run the correct functionality for the chosen module"""

    if args['command'] == 'status':
        rules.show_status()
        check.check_sync()

    elif args['command'] == 'pull':
        check.check_pull()
        repo.repo_pull()
        rules.rules_diff()

    elif args['command'] == 'ack':
        if not check.check_ack():
            exit(1)
        rules.rules_ack()

    elif args['command'] == 'list':
        check.check_list()
        rules.rules_list()

    elif args['command'] == 'add':
        check.check_add()
        # print(args)
        rules.rules_add(args['rulefile'])

    elif args['command'] == 'del':
        check.check_del()
        # print(args)
        # rules_del(args['rulefile'])

    elif args['command'] == 'sync':
        if not check.check_pull():
            exit(1)
        repo.repo_pull()
        if args['ack']:
            rules.rules_ack()
        if not check.check_sync():
            exit(1)
        rules.logcheck_sync()
