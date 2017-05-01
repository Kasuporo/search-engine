import httplib2
import lxml.html

from urllib.parse import urlparse
from lxml import html
from bs4 import BeautifulSoup
from multiprocessing import Pool

class web:

    def __init__(self, query, seed, depth, external):
        self.query = query
        self.seed = seed
        self.depth = depth
        self.external = external

    def find_all_links(self, link, crawled):
        http = httplib2.Http()
        status, response = http.request(link)
        page = html.fromstring(response)

	# Finds every link on a webpage
        if page not in crawled: # Ignores duplicates
            if not self.external:
                url = [link for link in page.xpath('//a/@href') if link.startswith('http')]
                # Ignores relative links becuause they are bad
            else:
                parsedUri = urlparse(link)
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsedUri)
                url = [link for link in page.xpath('//a/@href') if link.startswith(domain)]
        else:
            return
        return url

    def get_info(self, link):
        http = httplib2.Http()
        status, response = http.request(link)
        soup = BeautifulSoup(response, 'lxml')

	# Gets title and all text in a <p> tag
        title = soup.title.name
        pTexts = [p.get_text() for p in soup.find_all('p')]
        pTexts = "".join(pTexts)
        pageInfo = [title, pTexts]
        return pageInfo

    def page_rank(self, urls):
        # Return as: {URL : [Title, Text]}
        with Pool(5) as p:
            titles, texts = [p.map(self.get_info, urls)]
        # TO-DO: Index on text

    def web_crawl(self):
        toCrawl = [self.seed]
        crawled = []
        nextDepth = []
        atDepth = 0
        pageInfo = {}
        while toCrawl and atDepth <= self.depth:
            page = toCrawl.pop()
            if page not in crawled:
                nextDepth += self.find_all_links(page, crawled)
                crawled.append(page)
                pageInfo[page] = self.get_info(page)
            if not toCrawl:
                toCrawl, nextDepth = nextDepth, []
                atDepth += 1
        print(crawled)
        print(pageInfo)
        return crawled

    def index(self):
        urls = self.web_crawl(self.seed)
        with Pool(10) as p:
            index = p.map(self.page_rank, urls)
        return index

class text:

    def __init__(self, query, docs):
        self.query = query
        self.docs = docs
