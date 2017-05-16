from flask import Flask, render_template, request, redirect

import feedparser
import random
from app import search
from app import spellcheck
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

        # Checks spelling and FORCES YOU TO USE IT
        queryCheck = query.split()
        for i in queryCheck:
            spell = spellcheck.check(queryCheck[i])
            corrected = spell.correct(queryCheck[i])
            queryCheck[i] = corrected
        query = " ".join(queryCheck)

        web = search.web(query, seed, depth, external)
        pages = web.search()

        return render_template('results.html',
                                query = query,
                                pages = pages)
