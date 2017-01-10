import httplib2
import lxml.html
from urllib.parse import urlparse
from lxml import html
from bs4 import BeautifulSoup

class web:

	def __init__(self, query, seed, depth, external):
		self.query = query
		self.seed = seed
		self.depth = depth
		self.external = external

	def find_all_links(self):
		http = httplib2.Http()
		status, response = http.request(link)
		page = html.fromstring(response)
		if self.external:
			url = [link for link in page.xpath('//a/@href') if link.startswith('http')]
			# Ignores relative links becuause they are bad
		else:
			parsedUri = urlparse(link)
			domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsedUri)
			url = [link for link in page.xpath('//a/@href') if link.startswith(domain)]
		return url

	def get_text(self):
		http = httplib2.Http()
		status, response = http.request(link)
		soup = BeautifulSoup(response, 'lxml')
		pTexts = [p.get_text() for p in soup.find_all('p')]
		pTexts = " ".join(pTexts)
		return pTexts

	def web_crawl(self):
		toCrawl = [self.seed]
		crawled = []
		nextDepth = []
		atDepth = 0
		while toCrawl and atDepth <= self.depth:
			page = toCrawl.pop()
			if page not in crawled:
				nextDepth += find_all_links(page)
				crawled.append(page)
			if not toCrawl:
				toCrawl, nextDepth = nextDepth, []
				atDepth += 1
		return crawled

class text:

	def __init__(self, query, docs):
		self.query = query
		self.docs = docs

	# To-Do: Everything
