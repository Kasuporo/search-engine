from flask import Flask, render_template, request, redirect

import feedparser
import random
import os
from app import search
from app import app

@app.route('/')
def home():
    feedURL = "https://www.nasa.gov/rss/dyn/image_of_the_day.rss"
    feed = feedparser.parse(feedURL)
    background = feed.entries[7]['links'][1]['href']
    # Gets url of NASA image of the day
    return render_template('index.html',
                            background = background)

@app.route('/results', methods=['GET', 'POST'])
def page_results():
    if request.method == 'POST':

        external = False
        if request.form.get('external'):
            external = True

        seed, depth = request.form['seed'], request.form['depth']
        query = request.form['query']

        web = search.web(query, seed, depth, external)
        pageInfo, pageRanks = web.search()

        # Hotlinking images is bad, don't ever do this
        backgrounds = ['http://i.imgur.com/HSEvn6M.jpg', 'http://i.imgur.com/wYekTr5.jpg',
                       'http://i.imgur.com/AdlyZgO.jpg', 'http://i.imgur.com/I0zYjsT.jpg',
                       'http://i.imgur.com/I0zYjsT.jpg', 'http://i.imgur.com/mj2QAev.jpg']

        number = random.randint(0,5)
        background = backgrounds[number]
        #Sets random background from list

        return render_template('results.html',
                                background = background,
                                query = query,
                                pageInfo = pageInfo,
                                pageRanks = pageRanks)
