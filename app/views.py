#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, g

from app import app
from search import web, text

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/web', methods=['GET', 'POST'])
def web_search():
	if request.method == 'POST':
		query = request.form['search']
		# Put query here
		# webSearch = web(query, seed, depth)
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
		# Here too
		# textSearch = text(query, docs)
		# results = textSearch.text_query()
		return render_template('results.html',
								results = results,
								title = 'Results')
	else:
		return render_template('text_search.html')
