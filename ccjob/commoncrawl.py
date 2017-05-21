

import re

from mrjob.job import MRJob
from warc import WARCFile
from six.moves.urllib.request import url2pathname
from s3fs import S3FileSystem

from . structures import CaseInsensitiveDict

__all__ = [
    'CommonCrawl'
]

class CommonCrawl(MRJob):
    """
    Concrete Base class for CommonCrawl MRJob Task.

    Can be inherited from, or used directly by overriding `self.pattern` regular expression
    pattern or through manipulation of the inherited MRJob parent class.

    Usage::

    .. code:: python

        class GoogleAnalytics(CommonCrawl):

            def mapper_init(self):
                self.pattern = re.compile('[\"\']UA-(\d+)-(\d)+[\'\"]')

        if __name__ == '__main__':
            GoogleAnalytics.run()
    """
    s3 = S3FileSystem(anon=True)

    def __repr__(self):
        return '<{clsname}: {stdin}>'.format(
            clsname=self.__class__.__name__,
            stdin=self.stdin,
        )

    def configure_options(self):
        super(CommonCrawl, self).configure_options()
        self.add_passthrough_option(
            '--pattern',
            default='[\"\']UA-(\d+)-(\d)+[\'\"]',
            type=str,
            help='Regex pattern input as a command line argument',
        )
    def mapper_init(self):
        self.pattern = re.compile(self.options.pattern)

    @staticmethod
    def split_headers(head):
        return CaseInsensitiveDict(
            [
                k.strip() for k in i.split(':', 1)
            ] for i in head.splitlines() if ':' in i
        )

    def get_payload(self, record):
        payload = record.payload.read()
        head, _, tail = payload.partition('\r\n\r\n')
        content_type = self.split_headers(head).get('content-type', '').lower()
        if 'latin-1' or 'iso-8859-1' in content_type:
            tail = tail.decode('latin-1').encode('utf-8')
        try:
            return tail.decode('utf-8')
        except UnicodeDecodeError:
            return str()

    def read_warc(self, key):
        keypath = 's3://aws-publicdatasets/{key}'.format(key=key)
        with self.s3.open(keypath, 'rb') as fp:
            warcfile = WARCFile(fileobj=fp, compress='gzip')
            for record in warcfile.reader:
                if record.type == 'response':
                    self.increment_counter(self.__class__.__name__, 'match', 1)
                    yield record

    def mapper(self, key, line):
        for record in self.read_warc(line.strip()):
            payload = self.get_payload(record)
            for value in self.process_record(payload):
                yield ((url2pathname(record.url), value), 1)

    def process_record(self, body):
        for match in self.pattern.finditer(body):
            if match:
                yield match.groups()[0]

    def reducer(self, url, values):
        yield (url[0], url[1])

