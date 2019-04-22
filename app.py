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
    conn = functions.getConn('c9')
    networks = functions.getAllNetworks(conn)
    return render_template('home.html',networks=networks)
    
@app.route('/add', methods=['GET','POST'])
def add():
    '''Allows users to add a show to the database'''
    conn = functions.getConn('c9')
    curs = conn.cursor()

    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        conn = functions.getConn('c9')
        title = request.form.get('title')
        year = request.form.get('year')
        genre = request.form.get('genre')
        script = request.form.get('script')
        description = request.form.get('description')
        creator = request.form.get('creator')
        network = request.form.get('network')

        if title == "":
            flash("Title must be nonempty")
            return render_template('add.html')
            
        elif script == "":
            flash("Script must be nonempty")
            return render_template('add.html')
            
        else:
            curs.execute('select title from shows where title=%s', [title])
            databaseTitles = curs.fetchone()
            if(databaseTitles == None):
                curs.execute('insert into shows (title, year, genre, script, description) values(%s, %s, %s, %s, %s)', [title, year, genre, script, description])
                curs.execute('insert into creators (name) values(%s)', [creator])
                curs.execute('insert into networks (name) values(%s)', [network])
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
    '''Displays all the user requested search results'''
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
            print creator
            shows = functions.getResultsByCreator(conn,creator)
        return render_template('results.html', shows=shows)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8082)