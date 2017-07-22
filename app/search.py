import httplib2
import lxml.html
import operator
import re
import codecs

from urllib.parse import urlparse
from lxml import html
from bs4 import BeautifulSoup

class web:

    def __init__(self, query, seed, depth, external, phrase):
        self.query = query
        self.seed = seed
        self.depth = depth
        self.external = external
        self.phrase = phrase

    def check_url(self, link, domain):
        """ 
        Checks a link to see if it is suitable for futher crawling, 
        and adds the domain name to a relative link if not external 
        """

        ignore = ['.jpg', '.png', '.gif', '.pdf']
        for ext in ignore:
            if ext in link:
                return False

        if not link.startswith(domain):
            link = domain + link[1:]

        p = re.compile('.+?\/(ttps|ttp):\/\/')
        try:
            l = p.split(link)
            link = h + l[1] + '://' + l[2]
        except:
            pass

        return link

    def find_all_links(self, link, crawled):
        http = httplib2.Http(disable_ssl_certificate_validation=True)
        status, response = http.request(link)
        page = html.fromstring(response)

        parsedUri = urlparse(link)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsedUri)
        # Finds every link on a webpage
        urls = []
        if page not in crawled:
            for link in page.xpath('//a/@href'):
                if self.external:
                    urls.append(self.check_url(link, domain))
                else:
                    if link.startswith(domain):
                        urls.append(self.check_url(link, domain))

        for link in urls[:]:
            if link is False:
                urls.remove(link)

        print('Found %s links from: %s' % (len(urls), link))
        return urls

    def strip_escape(self, string):
        """
        Removes all unwanted escape seqences: '\\n', '\\x0b' etc.
        from the input string for better ranking
        """

        ESCAPE_SEQUENCE_RE = re.compile(r'''
            ( \\U........      # 8-digit hex escapes
            | \\u....          # 4-digit hex escapes
            | \\x..            # 2-digit hex escapes
            | \\[0-7]{1-3}     # Octal escapes
            | \\N\{[^]}+\}     # Unicode characters by name
            | \\[\\'"abfnrtv]  # Single-character escapes
            )''', re.UNICODE | re.VERBOSE)

        def decode_match(match):
            return codecs.decode(match.group(0), 'unicode-escape')

        return ESCAPE_SEQUENCE_RE.sub(decode_match, string)


    def get_info(self, link):
        http = httplib2.Http(disable_ssl_certificate_validation=True)
        status, response = http.request(link)
        soup = BeautifulSoup(response, 'lxml')
        print('Getting text from: %s' % (link))

        try:
            title    = soup.find('title').get_text()
            text     = self.strip_escape(soup.get_text())
            pTexts   = "".join([p.get_text() for p in soup.find_all('p')])
            pageInfo = [title, text, pTexts]
            return pageInfo
        except:
            return 1 # Last resort to catch 'non-sites'

    # Get ready for the worst page ranker you have ever seen
    def page_rank(self, pageInfo, urls):
        words = self.query.lower().split()
        with open('app/stopwords.txt', 'r') as stopwords: # Remove unnecessary words from search
            for word in words:
                if word in stopwords:
                    words.remove(word)

        pageRanks = {}
        for url in urls:
            rank = 0
            text = pageInfo[url][1].lower().split()
            #if len(text) > 0:
            for w in words:
                for t in text:
                    rank += 1 if w == t else 0
            rankRel = len(words) / len(text)
            rank /= rankRel * 100
            pageRanks[url] = rank
            print('Ranked %s as %f' % (url,rank))

        # Sorts based on the values of pageRanks
        sortedRanks = sorted(pageRanks.items(), key=operator.itemgetter(1), reverse=True)
        return sortedRanks # Returns as: [(url, rank), ...] in descending order

    def phrase_rank(self, pageInfo, urls):
        pageRanks = {}
        phrase = self.query.lower()

        for url in urls:
            rank = 0
            text = pageInfo[url][1].lower()
            reall = re.findall(phrase, text) # Regex is fun, regex is good
            rank += len(reall)
            pageRanks[url] = rank
            print('Ranked %s as %f' % (url,rank))

        sortedRanks = sorted(pageRanks.items(), key=operator.itemgetter(1), reverse=True)
        return sortedRanks

    # Get ready for the slowest web crawler you have ever seen
    def web_crawl(self):
        toCrawl   = [self.seed]
        crawled   = []
        nextDepth = []
        atDepth   = 1

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
            if self.get_info(page) != 1:
                pageInfo[page] = self.get_info(page)
        return pageInfo, crawled # Returns as {url: [title, text, pTexts]}, [crawled]

    def run(self):
        pageInfo, crawled = self.web_crawl()
        print('\n Starting page ranking \n')

        if self.phrase:
            ranks = self.phrase_rank(pageInfo, crawled)
        else:
            ranks = self.page_rank(pageInfo, crawled)

        pages = []
        num = 10 if len(ranks) >= 10 else len(ranks) # Limits to 10
        for i in range(0, num):
            temp          = {'url': 'url', 'title': 'title', 'body': 'body'}
            link          = ranks[i][0]
            temp['url']   = ranks[i][0]
            temp['title'] = pageInfo[link][0]
            char          = pageInfo[link][2] # Limits charcters to 240
            temp['body']  = char[:240]+'...' if len(char) > 240 else char
            pages.append(temp)
        #print(pages)
        return pages
