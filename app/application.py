import json
import pymysql
from flask import Flask, redirect, url_for, request, render_template
from controller import keyword_search
# Serve the file over http to allow for cross origin requests


app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    print (keyword) 
    paper_data = keyword_search.keyword_search(keyword)
    print (paper_data)
    return render_template('search.html', data=paper_data)

@app.route('/')
def index():
    return render_template('index.html')
#@app.route('/<path:path>')
#def static_proxy(path):
#    return app.send_static_file(path)

print('\nGo to http://localhost:8000/graph.html to see the example\n')
app.run(host='0.0.0.0', port=8000)
