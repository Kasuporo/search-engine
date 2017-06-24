from flask import Flask, render_template, request, redirect

from app import search
from app import spellcheck
from app import app

@app.route('/')
def home():
   return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def page_results():
    if request.method == 'POST':

        external = False
        if request.form.get('external'):
            external = True

        seed, depth = request.form['seed'], request.form['depth']
        query = request.form['query']

        # Checks spelling
        queryCheck = query.split()
        for i in range(len(queryCheck)):
            spell = spellcheck.check(queryCheck[i])
            corrected = spell.correct(queryCheck[i])
            queryCheck[i] = corrected
        queryCheck = " ".join(queryCheck)

        web = search.web(query, seed, depth, external)
        pages = web.search()

        if query == queryCheck: # If there is not a spelling mistake
            queryCheck = False
            return render_template('results.html',
                                    query = query,
                                    pages = pages,
                                    queryCheck = queryCheck)
        else:
            return render_template('results.html',
                                    query = query,
                                    pages = pages,
                                    queryCheck = queryCheck)


