from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug import secure_filename
import random, math
app = Flask(__name__)

import functions

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    '''Main page'''
    conn = functions.getConn('c9')
    networks = functions.getAllNetworks(conn)
    return render_template('home.html',networks=networks)
    
@app.route('/add/', methods=['GET','POST'])
def add():
    '''Allows users to add a show to the database'''
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        conn = functions.getConn('c9')
        # insert data to database
        # and flash a message saying it's successful
        return render_template('add.html')
    
@app.route('/displayAll/', methods=['GET'])
def displayAll():
    '''Displays all shows in the database'''
    if request.method == 'GET': # return all results
        conn = functions.getConn('c9')
        shows = functions.getResultsByTitle(conn,"")
        return render_template('results.html', shows=shows)
    
@app.route('/profile/<int:sid>/', methods=['GET', 'POST'])
def profile(sid):
    '''Displays profile page of the show based on show id (sid)'''
    if request.method == 'GET':
        conn = functions.getConn('c9')
        show = functions.getShow(conn,sid)
        creators = functions.getCreators(conn,sid)
        return render_template('profile.html', show=show, creators=creators)
    

# @app.route('/results/', methods=['GET', 'POST'])
# def results():
#     if request.method == 'GET':
#         return render_template('results.html')

    
@app.route('/search/', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        conn = functions.getConn('c9')
        title = request.form['title']
        network = request.form['network']
        creator = request.form['creator']
        if title:
            shows = functions.getResultsByTitle(conn,title)
        if network:
            shows = functions.getResultsByNetwork(conn,network)
        if creator:
            shows = functions.getResultsByCreator(conn,creator)
        return render_template('results.html', shows=shows)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8082)