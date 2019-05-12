'''Enables users to search and add TV shows to the database.

Written Spring 2019
Chloe Moon
'''
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug import secure_filename
import functions, random, math


app = Flask(__name__)


app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

app.config['TRAP_BAD_REQUEST_ERRORS'] = True

#a list of common contentwarnings
#used in add() to allow users to choose from a set of warnings but also add new warnings
commonWarnings = ["Sex & Nudity","Violence & Gore","Profanity","Alcohol, Drugs & Smoking"]
        
@app.route('/')
def index():
    '''Main page'''
    conn = functions.getConn('final_project')
    networks = functions.getAllNetworks(conn)
    contentwarnings = functions.getAllWarnings(conn)
    return render_template('home.html',networks=networks, contentwarnings=contentwarnings)
    
@app.route('/add/', methods=['GET','POST'])
def add():
    '''Allows users to add a show to the database'''
    conn = functions.getConn('final_project')
    if request.method == 'GET':
        contentwarnings = functions.getAllWarnings(conn)
        return render_template('add.html',contentwarnings=contentwarnings, commonWarnings=commonWarnings)
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
        filled = (title and year and genre and script and description and creatorList and network and cwList)
        if not(filled):
            flash("All fields should be completely filled")
            return redirect(request.referrer)
        else:
            databaseTitles = functions.getResultsByTitle(conn, title)
            if(len(databaseTitles)==0):
                functions.insertShows(conn, title, year, genre, cwList, script, description, creatorList, network)
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
        # print show
        return render_template('profile.html', show=show, creators=creators, warnings=warnings)
        
@app.route('/edit/<int:sid>/', methods=['GET','POST'])
def edit(sid):
    '''Edits/updates profile page of the show based on show id (sid)'''
    conn = functions.getConn('final_project')
    if request.method == 'GET':
        show = functions.getShow(conn,sid)
        creators = functions.getCreators(conn,sid)
        warnings = functions.getWarnings(conn,sid)
        return render_template('edit.html', show=show, creators=creators, warnings=warnings)
    if request.method == 'POST':
        oldshow = functions.getShow(conn,sid)
        newtitle = request.form['show-title']
        newnetwork = request.form['show-network']
        newyear = request.form['show-release']
        newdesc = request.form['show-description']
        newscript = request.form['show-script']
        newgenre = request.form['show-genre']
        newcreators = request.form.getlist('show-creators')
        newcwList = request.form.getlist('show-warnings')
        print newcwList
        functions.update(conn, sid, newtitle, newyear,newnetwork, newgenre, newcwList, newscript, newdesc, newcreators)
        return redirect(url_for('edit', sid=sid))

    
@app.route('/search/', methods=['POST'])
def search():
    '''Displays all the user requested search results'''
    if request.method == 'POST':
        conn = functions.getConn('final_project')
        title = request.form['title']
        network = request.form['network']
        creator = request.form['creator']
        contentwarning = request.form['contentwarning']
        tag_names = request.form.getlist('tags')
        tag_vals = request.form.getlist('tag-arg')
        # print(tag_names)
        # print(tag_vals)
        if title:
            shows = functions.getResultsByTitle(conn,title)
        if network:
            shows = functions.getResultsByNetwork(conn,network)
        if creator:
            shows = functions.getResultsByCreator(conn,creator)
        if contentwarning:
            shows = functions.getResultsByContentWarning(conn,contentwarning)
        if title=='' and network=='' and creator=='' and contentwarning=='':
            flash("Search using at least one criteria")
            return redirect(request.referrer)
        # if tag_names and tag_vals:
        #     shows = functions.getResultsByTags(conn, tag_names, tag_vals)
        print shows
        return render_template('results.html', shows=shows)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8082)
