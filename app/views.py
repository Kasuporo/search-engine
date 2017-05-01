from flask import Flask, render_template, request, redirect

import feedparser
import random
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
    # Default Variables
    seed = "https://github.com/apt-helion/Viperidae " 
    depth = 1
    external = False

    if request.form.get('external'):
        external = True

    # seed, depth = request.form['seed'], request.form['depth']
    # docs = request.form['docs']
    query = request.form['query']

    # text = search.text(query, docs)
    web = search.web(query, seed, depth, external)
    web.web_crawl()
    # text = text.index()
    # web = web.index()

    backgrounds = ['http://i.imgur.com/HSEvn6M.jpg', 'http://i.imgur.com/wYekTr5.jpg',
                   'http://i.imgur.com/AdlyZgO.jpg', 'http://i.imgur.com/I0zYjsT.jpg',
                   'http://i.imgur.com/I0zYjsT.jpg', 'http://i.imgur.com/mj2QAev.jpg']

    number = random.randint(0,5)
    background = backgrounds[number]
    #Sets random background from list

    return render_template('results.html',
                            background = background,
                            query = query)
 
