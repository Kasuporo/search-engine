from flask import Flask, render_template, request, redirect, g
from urllib import urlopen, urlretrieve

import feedparser
import re
from app import search
from app import app

@app.route('/')
def home():
	feedURL = "https://www.nasa.gov/rss/dyn/image_of_the_day.rss"
	feed = feedparser.parse(feedURL)
	backhround = feed.entries[0]['links'][1]['href']
	return render_template('index.html',
							background = background)

@app.route('/web', methods=['GET', 'POST'])
def web_search():
	if request.method == 'POST':
		if request.form.get('external'):
			external = True
		else:
			external = False
		query, seed, depth = request.form['query'], request.form['seed'], request.form['depth']
		# webSearch = web(query, seed, depth, external)
		# results = webSearch.web_query()
		return render_template('results.html',
								results = results,
								title = "Results")
	else:
		return render_template('web_search.html')

@app.route('/text', methods=['GET', 'POST'])
def text_search():
	if request.method == 'POST':
		query = request.form['search']
		docs = request.form['docs']
		# textSearch = text(query, docs)
		# results = textSearch.text_query()
		return render_template('results.html',
								results = results)
	else:
		return render_template('text_search.html')

feedURL = "http://apod.nasa.gov.apod"
def get_image():
	xml = urlopen(feedURL).read()
	m = re.search(r"a href\"(image/.*?)\"", xml)
	firstImg = feedURL + m.group(1)
