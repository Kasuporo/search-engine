#!\usr\env\python
import urllib2
import lxml.html
import re
from bs4 import BeautifulSoup

#Gets all links from a page and puts it into a list
def findAllLinks(link):
	url = []
	connection = urllib2.urlopen(link)
	dom =  lxml.html.fromstring(connection.read())
	for link in dom.xpath('//a/@href'):
		if not link.startswith('http'):  					# Ignores relative links
			continue										# because I don't want to deal with them
		url.append(link)
	return url

#Web crawler crawls the web with set depth
def webCrawl(seed, maxDepth):
	toCrawl = [seed]
	crawled = []
	nextDepth = []
	depth = 0
	while toCrawl and depth <= maxDepth:
		page = toCrawl.pop()
		if page not in crawled:
			nextDepth += findAllLinks(page)
			crawled.append(page)
		if not toCrawl:
			toCrawl, nextDepth = nextDepth, []
			depth += 1
	return crawled

#Gets all text in a <p> tag from a html page
def getText(link):
	html = urllib2.urlopen(link)
	soup = BeautifulSoup(html, 'lxml')
	p_texts = [ p.get_text() for p in soup.find_all('p') ]
	p_texts = " ".join(p_texts)
	return p_texts


#--For Testing--#
#print(getText('http://news.bbc.co.uk/2/hi/health/2284783.stm'))
#print(webCrawl('http://www.qantas.com/qcatering/quality-safety-environment/index.html', 2))
#print(findAllLinks('https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=55260'))


""" ()()		Cute Bunny
    ('.')		Makes up for
    (()()		Ugly code
   *(_()() """
