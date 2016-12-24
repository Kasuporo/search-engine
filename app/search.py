#!/usr/bin/env python
import urllib2
import lxml.html
import re
from bs4 import BeautifulSoup

# Gets all links from a page and puts it into a list
def find_all_links(link):
	connection = urllib2.urlopen(link)
	dom = lxml.html.fromstring(connection.read())
	url = [link for link in dom.xpath('//a/@href') if link.startswith('http')]
	# Ignores relative links becuause they are bad
	return url
#print(find_all_links('https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=55260'))

# Web crawler crawls the web with set depth
def web_crawl(seed, maxDepth):
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
#print(web_crawl('http://www.qantas.com/qcatering/quality-safety-environment/index.html', 2))

# Gets all text in a <p> tag from a html page
def get_text(link):
	html = urllib2.urlopen(link)
	soup = BeautifulSoup(html, 'lxml')
	pTexts = [ p.get_text() for p in soup.find_all('p') ]
	pTexts = " ".join(pTexts)
	return pTexts
#print(get_text('http://news.bbc.co.uk/2/hi/health/2284783.stm'))


""" ()()		Indentation bunny says:
    ('.')		variables are mixedCase
    (()()		functions are lower_case_with_underscores
   *(_()() """
