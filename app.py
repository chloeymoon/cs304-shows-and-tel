from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug import secure_filename
app = Flask(__name__)

# import sys,os,random
import functions

app.secret_key = 'asdflsgflawiewurhe'

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    '''Main page'''
    # uid= session.get('uid','')
    return render_template('home.html')
    
@app.route('/results/', methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        return render_template('results.html')
    
@app.route('/search/', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        # searchterm = request.form['searchterm']
        # return all relevant dictionaries and display results
        # conn = functions.getConn('wmdb')
        # shows = functions.getResults(conn,searchterm)
        return render_template('results.html') #, shows=shows)
    
@app.route('/login/', methods=['POST'])
def login():
    return render_template('search.html')

# how are we connecting search result and each movie profile?
# link on each title? or separate section in the result page (maybe table)?
@app.route('/profile/<sid>/', methods=['GET', 'POST'])
def profile(sid):
    if request.method == 'GET':
        conn = functions.getConn('wmdb')
        show = functions.getShow(conn,sid)
        return render_template('profile.html', show=show)


if __name__ == '__main__':
    
    
    app.debug = True
    app.run('0.0.0.0',8082)

