import httplib2
import lxml.html
import threading

from urllib.parse import urlparse
from lxml import html
from bs4 import BeautifulSoup

class web:

    def __init__(self, query, seed, depth, external):
        self.query = str(query)
        self.seed = str(seed)
        self.depth = depth
        self.external = external
        threading.Thread.__init__(self)

    def find_all_links(self, page, crawled):
        http = httplib2.Http()
        status, response = http.request(link)
        page = html.fromstring(response)

	# Finds every link on a webpage
        if page not in crawled:
            if not self.external:
                url = [link for link in page.xpath('//a/@href') if link.startswith('http')]
                # Ignores relative links becuause they are bad
            else:
                parsedUri = urlparse(link)
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsedUri)
                url = [link for link in page.xpath('//a/@href') if link.startswith(domain)]
        return url

    def get_info(self, link):
        http = httplib2.Http()
        status, response = http.request(link)
        soup = BeautifulSoup(response, 'lxml')

        # Gets title and all text in a <p> tag
        title = soup.title.name
        pTexts = [p.get_text() for p in soup.find_all('p')]
        pTexts = "".join(pTexts)
        return title, pTexts

    def page_rank(self, urls):
        # Return as: {URL : [Title, Text]}
        title, text = [get_info(url) for url in urls]
        # TO-DO: Index on text

    def web_crawl(self, seed):
        toCrawl = [seed]
        crawled = []
        nextDepth = []
        atDepth = 0
        while toCrawl and atDepth <= self.depth:
            page = toCrawl.pop()
            if page not in crawled:
                nextDepth += find_all_links(page)
                crawled.append(page)
                # index here
            if not toCrawl:
                toCrawl, nextDepth = nextDepth, []
                atDepth += 1
        return crawled

    def index(self):
        urls = web_crawl(self.seed)
        with Pool(10) as p:
            index = p.map(page_rank, urls)
        return index

class text:

    def __init__(self, query, docs):
        self.query = query
        self.docs = docs
