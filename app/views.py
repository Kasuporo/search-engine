#!/usr/bin/python
from flask import Flask, render_template, request, redirect
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		query = request.form['search']
		return render_template('results.html', query = query)
	else:
		return render_template('queryindex.html')
