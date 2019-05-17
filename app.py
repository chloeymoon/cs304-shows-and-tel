'''Enables users to search and add TV shows to the database.

Written Spring 2019
Chloe Moon, Catherine Chen, Alice Zhou
'''
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug import secure_filename
import functions, random, math

import os
import bcrypt
import MySQLdb


app = Flask(__name__)


app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

app.config['TRAP_BAD_REQUEST_ERRORS'] = True

#a list of common contentwarnings
#used in add() to allow users to choose from a set of warnings but also add new warnings
commonWarnings = ["Sex & Nudity","Violence & Gore","Profanity","Frightening & Intense Scenes"]
        
@app.route('/')
def index():
    '''Main page'''
    conn = functions.getConn('final_project')
    networks = functions.getAllNetworks(conn)
    contentwarnings = functions.getAllWarnings(conn)
    return render_template('home.html', networks=networks, 
                                        contentwarnings=contentwarnings)
    
@app.route('/add/', methods=['GET','POST'])
def add():
    '''Allows users to add a show to the database'''
    conn = functions.getConn('final_project')
    if request.method == 'GET':
        contentwarnings = functions.getAllWarnings(conn)
        return render_template('add.html',contentwarnings=contentwarnings, 
                                commonWarnings=commonWarnings)
    if request.method == 'POST':
        conn = functions.getConn('final_project')
        title = request.form.get('title')
        year = request.form.get('year')
        genre = request.form.get('genre')
        script = request.form.get('script')
        description = request.form.get('description')
        network = request.form.get('network')
        cwList = request.form.getlist('cw')
        creatorList=request.form.getlist('creator')
        genreList=request.form.getlist('genre')
        tag_name = request.form['tags'] #.getlist('tags')
        tag_val = request.form['tag-arg'] #.getlist('tag-arg')
        filled = (title and year and genre and script and description
                and creatorList and network and cwList and tag_name and tag_val)
        if not(filled):
            flash("All fields should be completely filled")
            return redirect(request.referrer)
        else:
            databaseTitles = functions.getResultsByTitle(conn, title)
            if(len(databaseTitles)==0):
                functions.insertShows(conn, title, year, cwList, genreList, script, 
                                        description, creatorList, network, 
                                        tag_name, tag_val)
                flash("TV show: " + title + " successfully inserted")
                return render_template('add.html')
            else: 
                flash("TV Show already exists in database")
                return render_template('add.html')
        return render_template('add.html')

    
@app.route('/displayAll/', methods=['GET'])
def displayAll():
    '''Displays all shows in the database'''
    if request.method == 'GET': # return all results
        conn = functions.getConn('final_project')
        shows = functions.getResultsByTitle(conn,"")
        return render_template('results.html', shows=shows)

@app.route('/profile/<int:sid>/', methods=['GET'])
def profile(sid):
    '''Displays profile page of the show based on show id (sid)'''
    if request.method == 'GET':
        conn = functions.getConn('final_project')
        show = functions.getShow(conn,sid)
        creators = functions.getCreators(conn,sid)
        warnings = functions.getWarnings(conn,sid)
        genres = functions.getGenres(conn,sid)
        tags = functions.getTags(conn,sid)
        return render_template('profile.html', show=show, creators=creators, 
                                warnings=warnings, tags=tags, genres=genres)
        
@app.route('/edit/<int:sid>/', methods=['GET','POST'])
def edit(sid):
    '''Edits/updates profile page of the show based on show id (sid)'''
    conn = functions.getConn('final_project')
    if request.method == 'GET':
        show = functions.getShow(conn,sid)
        creators = functions.getCreators(conn,sid)
        warnings = functions.getWarnings(conn,sid)
        genres = functions.getGenres(conn,sid)
        tags = functions.getTags(conn, sid)
        return render_template('edit.html', show=show, creators=creators, 
                                warnings=warnings, tags=tags, genres=genres)
    if request.method == 'POST':
        newtitle = request.form['show-title']
        newnetwork = request.form['show-network']
        newyear = request.form['show-release']
        newdesc = request.form['show-description']
        newscript = request.form['show-script']
        newgenrelist = request.form.getlist('show-genres')
        newcreators = request.form.getlist('show-creators')
        newcwList = request.form.getlist('show-warnings')
        tag_name = request.form['tags']
        tag_val = request.form['tag-vals']
        functions.update(conn, sid, newtitle, newyear, newnetwork, 
                        newgenrelist, newcwList, newscript, newdesc,
                        newcreators, tag_name, tag_val)
        return redirect(url_for('profile', sid=sid))

@app.route('/search/', methods=['POST'])
def search():
    '''Displays all the user requested search results'''
    if request.method == 'POST':
        conn = functions.getConn('final_project')
        title = request.form['title']
        network = request.form['network']
        creator = request.form['creator']
        genre = request.form['genre']
        contentwarning = request.form['contentwarning']
        tag_name = request.form['tags'] #.getlist('tags')
        tag_val = request.form['tag-arg'] #.getlist('tag-arg')

        if (title=='' and network=='' and creator=='' and contentwarning==''
                      and tag_name=='' and tag_val=='' and genre==''):
            flash("Search using at least one criteria")
            return redirect(request.referrer)
            
        if title:
            shows = functions.getResultsByTitle(conn,title)
        if network:
            shows = functions.getResultsByNetwork(conn,network)
        if creator:
            shows = functions.getResultsByCreator(conn,creator)
        if genre:
            shows = functions.getResultsByGenre(conn,genre)
        if tag_name and tag_val:
            shows = functions.getResultsByTags(conn, tag_name, tag_val)
        if contentwarning:
            shows = functions.getResultsByContentWarning(conn,contentwarning)
            
        return render_template('results.html', shows=shows)
        
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    '''lets a user to sign up/join'''
    if request.method=='GET':
        return render_template('signup.html')
    if request.method=='POST':
        try:
            username = request.form['username']
            passwd1 = request.form['password1']
            passwd2 = request.form['password2']
            if passwd1 != passwd2:
                flash('passwords do not match')
                return redirect( url_for('signup'))
            hashed = bcrypt.hashpw(passwd1.encode('utf-8'), bcrypt.gensalt())
            conn = functions.getConn('final_project')
            userRow = functions.checkUsername(conn,username)
            if userRow is not None: #check if username exists in the database
                flash('That username is taken')
                return redirect( url_for('signup') )
            functions.insertUser(conn,username,hashed)
            session['username'] = username
            session['logged_in'] = True
            ###### decide and change this later ########
            return redirect(url_for('login', username=username))
        except Exception as err:
            flash('form submission error '+str(err))
            return redirect( url_for('signup') )
        
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        try:
            username = request.form['username']
            passwd = request.form['password']
            conn = functions.getConn('final_project')
            userRow = functions.checkPW(conn,username)
            if userRow is None:
                flash('login incorrect (app.py 201). Try again or join')
                return redirect(url_for('login'))
            hashed = userRow['hashed']
            #strings always come out as unicode, so have to encode
            if bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8')) == hashed:
                flash('successfully logged in as '+username)
                session['username'] = username
                session['logged_in'] = True
                #### change this later
                return redirect(url_for('login'))
            else:
                flash('login incorrect. Try again or join')
                return redirect(url_for('login'))
        except Exception as err:
            flash('form submission error '+str(err))
            return redirect( url_for('login') )
            
            
@app.route('/logout/', methods=['POST','GET'])
def logout():
    try:
        if 'username' in session:
            print session
            username = session['username']
            session.pop('username')
            session.pop('logged_in')
            flash('You are logged out')
            print session
            return redirect(url_for('index'))
        else:
            flash('you are not logged in. Please login or join')
            return redirect( url_for('login') )
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect( url_for('index') )

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)
