from flask import Flask, render_template, request, redirect

import feedparser
import re
import random
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

@app.route('/results', methods=['GET', 'POST'])
def web_search():
	if request.method == 'POST':
		if request.form.get('external'):
			external = True
		else:
			external = False

		# seed, depth = request.form['seed'], request.form['depth']
		# Gets stuff for web search
		# docs = request.form['docs']
		# Gets stuff for text search
		query = request.form['query']

		# textSearch = text(query, docs)
		# webSearch = web(query, seed, depth, external)

		#TO-DO: Merge text and web search into one big search

		backgrounds = ['http://i.imgur.com/HSEvn6M.jpg', 'http://i.imgur.com/wYekTr5.jpg', 'http://i.imgur.com/AdlyZgO.jpg',
					   'http://i.imgur.com/I0zYjsT.jpg', 'http://i.imgur.com/I0zYjsT.jpg', 'http://i.imgur.com/mj2QAev.jpg']

		number = random.randint(0,5)
		background = backgrounds[number]

		return render_template('results.html',
								background = background,
								query = query,
								#results = results,
								#title = "Results"
								)
	else:
		return redirect("/", code=302)
