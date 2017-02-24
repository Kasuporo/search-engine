from flask import Flask, render_template, request, redirect, g

import feedparser
import re
from app import search
from app import app

@app.route('/')
def home():
	feedURL = "https://www.nasa.gov/rss/dyn/image_of_the_day.rss"
	feed = feedparser.parse(feedURL)
	background = feed.entries[0]['links'][1]['href']
	# Gets url of NASA image of the day
	return render_template('index.html',
							background = background)

@app.route('/web', methods=['GET', 'POST'])
def web_search():
	if request.method == 'POST':
		if request.form.get('external'):
			external = True
		else:
			external = False
			
		seed, depth = request.form['seed'], request.form['depth']
		# Gets stuff for web search
		docs = request.form['docs']
		# Gets stuff for text search
		query = request.form['query']

		# textSearch = text(query, docs)
		# webSearch = web(query, seed, depth, external)

		#TO-DO: Merge text and web search into one big search
		return render_template('results.html',
								results = results,
								title = "Results")
	else:
		return render_template('web_search.html')
