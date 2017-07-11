import re
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

        # Defaults
        phrase = False

        external = True if request.form.get('external') else False
        seed, depth = request.form['seed'], request.form['depth']
        query = request.form['query']

        # Test for phrase searching
        regexp = r'\"(.+?)\"' # Regex for finding text in quotes
        m = re.search(regexp, query)
        try:
            query  = m.group()
            query  = query[1:-1] # Remove quotes
            phrase = True
        except:
            pass

        # Checks spelling
        queryCheck = query.split()
        for i in range(len(queryCheck)):
            spell = spellcheck.check(queryCheck[i])
            corrected = spell.correct(queryCheck[i])
            queryCheck[i] = corrected
        queryCheck = " ".join(queryCheck)

        # Do the search
        web = search.web(query, seed, depth, external, phrase)
        pages = web.run()

        if query == queryCheck: # If there is not a spelling mistake
            queryCheck = False
            return render_template('results.html',
                                    query = query,
                                    pages = pages,
                                    queryCheck = queryCheck,
                                    phrase = phrase)
        else:
            return render_template('results.html',
                                    query = query,
                                    pages = pages,
                                    queryCheck = queryCheck,
                                    phrase = phrase)


