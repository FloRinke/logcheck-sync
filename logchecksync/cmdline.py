"""parse commandline arguments"""

__author__ = 'Florian Rinke'

import argparse
import sys
import logging

LOG = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Synchronizes logcheck rules from a git repository')
subparsers = parser.add_subparsers(help='One of these Commands', metavar='command', dest='command')

parser_status = subparsers.add_parser('status', help='Show Status')
parser_pull = subparsers.add_parser('pull', help='synchronize repo')
parser_ack = subparsers.add_parser('ack', help='acknowledge new rulefiles without adding/deleting')
parser_list = subparsers.add_parser('list', help='list rulefile to sync')

parser_add = subparsers.add_parser('add', help='add a rulefile to sync')
parser_add.add_argument('rulefile', help='list of rulefiles to add', nargs='+')

parser_del = subparsers.add_parser('del', help='delete a rulefile from sync')
parser_del.add_argument('rulefile', help='list of rulefiles to add', nargs='+')

parser_sync = subparsers.add_parser('sync', help='synchronize repo and selected rules')
parser_sync.add_argument('-a', '--ack', help='also acknowledge new rulefiles', action='store_true')

if len(sys.argv) == 1:
    parser.print_usage()
    sys.exit(1)

args = vars(parser.parse_args())
LOG.info("cmdline args: %s", args)


def __init__():
    pass
