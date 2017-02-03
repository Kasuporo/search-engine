from flask import Flask, render_template, request, redirect, g

from app import search
from app import app

@app.route('/')
def home():
	return render_template('home.html')

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
								results = results,
								title = 'Results')
	else:
		return render_template('text_search.html')
