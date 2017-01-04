#!/usr/bin/env python2.7
import httplib2
import lxml.html
import re
from urlparse import urlparse
from lxml import html
from bs4 import BeautifulSoup

class web():

	def __init__(self, query, seed, depth, external):
		self.query = query
		self.seed = seed
		self.depth = depth
		self.external = external

	# Gets all links from a page and puts it into a list
	def find_all_links(self, link, external):
		http = httplib2.Http()
		status, response = http.request(link)
		page = html.fromstring(response)
		if external:
			url = [link for link in page.xpath('//a/@href') if link.startswith('http')]
			# Ignores relative links becuause they are bad
		else:
			parsedUri = urlparse(link)
			domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsedUri)
			url = [link for link in page.xpath('//a/@href') if link.startswith(domain)]
		return url


	# Gets all text in a <p> tag from a html page
	def get_text(self, link):
		http = httplib2.Http()
		status, response = http.request(link)
		soup = BeautifulSoup(response, 'lxml')
		pTexts = [p.get_text() for p in soup.find_all('p')]
		pTexts = " ".join(pTexts)
		return pTexts

	# Web crawler finds ALL the links from the web up to a set depth
	def web_crawl(self, seed, maxDepth):
		toCrawl = [seed]
		crawled = []
		nextDepth = []
		depth = 0
		while toCrawl and depth <= maxDepth:
			page = toCrawl.pop()
			if page not in crawled:
				nextDepth += find_all_links(page)
				crawled.append(page)
			if not toCrawl:
				toCrawl, nextDepth = nextDepth, []
				depth += 1
		return crawled

class text():

	def __init__(self, query, docs):
		self.query = query
		self.docs = docs

	# To-Do: Everything
