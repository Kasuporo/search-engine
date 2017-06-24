import httplib2
import lxml.html
import operator

from urllib.parse import urlparse
from lxml import html
from bs4 import BeautifulSoup

class web:

    def __init__(self, query, seed, depth, external):
        self.query = query
        self.seed = seed
        self.depth = depth
        self.external = external

    def find_all_links(self, link, crawled):
        http = httplib2.Http(disable_ssl_certificate_validation=True)
        status, response = http.request(link)
        page = html.fromstring(response)

        # Finds every link on a webpage
        if page not in crawled:
            if self.external:
                # Ignores relative links becuause they are bad
                url = [link for link in page.xpath('//a/@href') if link.startswith('http')]
            else:
                parsedUri = urlparse(link)
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsedUri)
                url = [link for link in page.xpath('//a/@href') if link.startswith(domain)]
        return url

    def get_info(self, link):
        http = httplib2.Http(disable_ssl_certificate_validation=True)
        status, response = http.request(link)
        soup = BeautifulSoup(response, 'lxml')

        # Gets title and all text in a <p> tag
        try:
            title    = soup.find('title').get_text()
            pTexts   = [p.get_text() for p in soup.find_all('p')]
            pTexts   = " ".join(pTexts).replace('\n', '') # Removes all newlines (\n)
            pageInfo = [title, pTexts[:140]+'...'] # Restrics text to 140 characters
            return pageInfo
        except:
            return None # Makes sure it is a page and not a picture

    # Get ready for the worst page ranker you have ever seen
    def page_rank(self, pageInfo, urls):
       words = self.query.lower().split()
        with open('app/stopwords.txt') as stopwords: # Remove unnecessary words from search
            for word in words:
                if word in stopwords:
                    words.remove(word)

        pageRanks = {}
        for url in urls:
            rank = 0
            text = pageInfo[url][1].lower().split()
            #if len(text) > 0:
            with open('app/stopwords.txt', 'r') as stopwords:
                for word in text:
                    if word in stopwords:
                        text.remove(word)
                for w in words:
                    for t in text:
                            if w is t:
                                rank += 1
            rankNum = len(words) / len(text)
            rank /= rankNum * 100
            pageRanks[url] = rank

        # Sorts based on the values of pageRanks
        sortedRanks = sorted(pageRanks.items(), key=operator.itemgetter(1), reverse=True)
        return sortedRanks # Returns as: [(url, rank), ...] in descending order

    # Get ready for the slowest web crawler you have ever seen
    def web_crawl(self):
        toCrawl   = [self.seed]
        crawled   = []
        nextDepth = []
        atDepth   = 0
        depth     = 1 # Defaults to 1 if not given a number

        if self.depth.isnumeric():
            depth = int(self.depth)

        while toCrawl and atDepth <= depth:
            page = toCrawl.pop()
            if page not in crawled:
                nextDepth += self.find_all_links(page, crawled)
                crawled.append(page)
            if not toCrawl:
                toCrawl, nextDepth = nextDepth, []
                atDepth += 1

        pageInfo = {}
        for page in crawled:
            pageInfo[page] = self.get_info(page)
        return pageInfo, crawled # Returns as {url: [title, pTexts], ...}, [crawled, ...]

    def search(self): # Runs all functions
        pageInfo, crawled = self.web_crawl()
        ranks = self.page_rank(pageInfo, crawled)

        pages = []
        for i in range(0,5):
            temp          = {'url': 'url', 'title': 'title', 'body': 'body'}
            temp['url']   = ranks[i][0]
            temp['title'] = pageInfo[temp['url']][0]
            temp['body']  = pageInfo[temp['url']][1]
            pages.append(temp)
        #print(pages)
        return pages


#####----- Tests -----#####
if __name__ == " __main__":
    seed = "https://github.com/apt-helion/Viperidae"
    query = "Github"
    depth = 1
    external = False

    webSearch = web(query, seed, depth, external)
    #print(webSearch.web_crawl())
    #print(webSearch.search())
