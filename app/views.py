#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, g

from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		query = request.form['search']
		return render_template('results.html',
								query = query,
								title = "Results")
	else:
		return render_template('queryindex.html')
