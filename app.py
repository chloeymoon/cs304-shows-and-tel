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

@app.route('/')
def index():
    '''Main page'''
    conn = functions.getConn('final_project')
    networks = functions.getAllNetworks(conn)
    return render_template('home.html',networks=networks)
    
@app.route('/add/', methods=['GET','POST'])
def add():
    '''Allows users to add a show to the database'''
    conn = functions.getConn('final_project')
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        conn = functions.getConn('final_project')
        title = request.form.get('title')
        year = request.form.get('year')
        genre = request.form.get('genre')
        script = request.form.get('script')
        description = request.form.get('description')
        # creator = request.form.get('creator')
        network = request.form.get('network')
        # cw = request.form.get('contentwarning')
        cwList = request.form.getlist('cw')
        creatorList=request.form.getlist('creator')
        # tag_names = request.form.getlist('tags')
        # tag_vals = request.form.getlist('tag-arg')
        tag_name = request.form['tags']
        tag_val = request.form['tag-arg']
        filled = (title and year and genre and script and description 
                    and creatorList[0] and network and cwList[0]
                    and tag_name and tag_val)
        if not(filled):
            flash("All fields should be completely filled")
            return redirect(request.referrer)
        else:
            databaseTitles = functions.getResultsByTitle(conn, title)
            if(len(databaseTitles)==0):
                functions.insertShows(conn, title, year, genre, cwList, script, 
                                        description, creatorList, network, 
                                        tag_names, tag_vals)
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
        tags = functions.getTags(conn,sid)
        print(tags)
        # print show
        return render_template('profile.html', show=show, creators=creators, 
                                warnings=warnings, tags=tags)
        
@app.route('/edit/<int:sid>/', methods=['GET','POST'])
def edit(sid):
    '''Edits/updates profile page of the show based on show id (sid)'''
    conn = functions.getConn('final_project')
    if request.method == 'GET':
        show = functions.getShow(conn,sid)
        creators = functions.getCreators(conn,sid)
        warnings = functions.getWarnings(conn,sid)
        tags = functions.getTags(conn, sid)
        return render_template('edit.html', show=show, creators=creators, 
                                warnings=warnings, tags=tags)
    if request.method == 'POST':
        oldshow = functions.getShow(conn,sid)
        newtitle = request.form['show-title']
        oldnetwork = oldshow['network']
        newnetwork = request.form['show-network']
        newyear = request.form['show-release']
        newdesc = request.form['show-description']
        newscript = request.form['show-script']
        newgenre = request.form['show-genre']
        newcreators = request.form['show-creators']
        oldcwList = functions.getWarnings(conn,sid)
        newcwList = request.form.getlist('show-warning')
        tag_name = request.form['tags']
        tag_val = request.form['tag-vals']
        functions.update(conn, sid, newtitle, newyear, oldnetwork, newnetwork, 
                        newgenre, oldcwList, newcwList, newscript, newdesc,
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
        tag_name = request.form['tags']
        tag_val = request.form['tag-arg']
        print("*************************")
        print(tag_name)
        print(tag_val)
        # tag_names = request.form.getlist('tags')
        # tag_vals = request.form.getlist('tag-arg')
        if title:
            shows = functions.getResultsByTitle(conn,title)
        if network:
            shows = functions.getResultsByNetwork(conn,network)
        if creator:
            shows = functions.getResultsByCreator(conn,creator)
        if (title=='' and network=='' and creator==''
                      and tag_name=='' and tag_val==''):
            flash("Search using at least one criteria")
            return redirect(request.referrer)
        if tag_name and tag_val:
            shows = functions.getResultsByTags(conn, tag_name, tag_val)
        return render_template('results.html', shows=shows)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8082)
