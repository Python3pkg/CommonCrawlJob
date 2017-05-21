

import boto

from gzip import GzipFile
from boto.s3.key import Key
from io import BytesIO
from builtins import ( # noqa
    bytes, str, open, super, range,
    zip, round, input, int, pow, object
)

__all__ = [
    'S3Remote',
]


class S3Remote(object):

    def __init__(self, bucket='aws-publicdatasets'):
        self.s3 = boto.connect_s3(anon=True, is_secure=False)
        self.bucket = self.s3.get_bucket(bucket)

    def __repr__(self):
        return '<{!s} {!r}>'.format(
            self.__class__.__name__,
            self.bucket.name
        )

    @property
    def valid_segments(self):
        kfile = Key(self.bucket, '/common-crawl/parse-output/valid_segments.txt')
        return [i.strip() for i in kfile.read().splitlines()]

    @property
    def prefixes(self):
        """
        By default get's the latest crawl prefix.

        Example:
        --------
        Get the latest crawl from 2014:

        .. code:: python

            >>> self.get_crawl(crawl_date='2014')

        :param crawl_date: str
            Crawl Date Prefix: EG. 2015-48

        :return: crawl_prefix
        :rtype: str
        """
        crawl_bucket = self.bucket.list('common-crawl/crawl-data/', '/')
        return [
            key.name.encode('utf-8')
            for key in crawl_bucket if 'CC-MAIN' in key.name
        ]

    def select_crawl(self, crawl_date=''):
        """
        Fuzzy match a common crawl crawl prefix from available s3 buckets.
        Always selects the latest crawl date matched.

        :param crawl_date: str
            Crawl date specifier

        :return: Selected crawl date
        :rtype: str

        """
        return max([i for i in self.prefixes if crawl_date in i])

    def get_index(self, prefix):
        """
        :param prefix: str
            Prefix to S3 bucket

        :return: Uncompressed warc index
        :rtype: str
        """
        crawl = self.select_crawl(prefix)
        botokey = Key(self.bucket, crawl + 'warc.paths.gz')
        return [i.strip() for i in GzipFile(fileobj=BytesIO(botokey.read()))]

    def print_buckets(self):
        """
        Helper function to print out list of available buckets

        :return: Nothing is returned
        :rtype: None
        """
        for prefix in self.prefixes:
            print(prefix.split('/')[-2].lstrip('CC-MAIN-'))
