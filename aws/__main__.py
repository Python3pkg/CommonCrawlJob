

import sys

from argparse import ArgumentParser
from . import S3Remote


def command_line(remote):

    prog = 'crawl_index'
    description = 'Helper tool to run MapReduce jobs over Common Crawl'

    crawl_list = ArgumentParser(add_help=False)
    crawl_list.add_argument(
        '-l', '--list',
        action='store_true',
        help='Enumerate all possible crawl dates',
    )

    # Preparse Date Codes
    crawl, _ = crawl_list.parse_known_args()
    if crawl.list:
        remote.print_buckets()
        exit(0)

    parser = ArgumentParser(
        parents=[crawl_list],
        prog=prog,
        description=description,
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version="%s v0.1.0" % prog
    )
    parser.add_argument(
        '-d', '--date',
        nargs='?',
        default='latest',
        help='Specify crawl date',
        metavar='d',
    )
    parser.add_argument(
        '-f', '--file',
        nargs='?',
        metavar='f',
        default=None,
        help='Output to a file'
    )
    return parser.parse_args()


def main():
    remote = S3Remote()
    args = command_line(remote)
    crawl = remote.select_crawl() if args.date == 'latest' else remote.select_crawl(args.date)
    fp = open(args.file, 'wt') if args.file else sys.stdout
    idx = remote.get_index(crawl)
    for i in idx:
        print(i, file=fp)

if __name__ == '__main__':
    sys.exit(main())
