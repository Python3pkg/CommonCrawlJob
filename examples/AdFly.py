

from bs4 import BeautifulSoup
from ccjob import CommonCrawl

class AdFly(CommonCrawl):

    def process_record(self, body):
        soup = BeautifulSoup(body, 'lxml')
        for record in soup.find_all('a'):
            link = record.attrs.get('href', '')
            if 'adf.ly' in link:
                yield link

if __name__ == '__main__':
    AdFly.run()
