'''Functions interacting with the backend that will be used in app.py.

Written Spring 2019
Chloe Moon, Catherine Chen
'''

'''multiple search criteria: caluses = [] and then '   '.join(clauses)'''
'''select * from table where (title = % or '')''' # title='' returns an empty string
'''construct a view file'''
'''lock for threads'''
from flask import Flask, flash, send_from_directory
from werkzeug import secure_filename
import os, sys
import MySQLdb
import functions, random, math
from threading import Lock

app = Flask(__name__)
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
app.config['UPLOADS'] = 'uploads'
lock = Lock()

def getConn(db):
    '''Connects to local host'''
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db)
    conn.autocommit(True) 
    return conn

# Getters for Profile page
def getAllNetworks(conn):
    '''Returns all the networks in the database, for the dropdown menu in the home page'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    # curs.execute('select name from networks group by networks.name')
    curs.execute('select name from networks')
    return curs.fetchall()
    
def getAllWarnings(conn):
    '''Returns all the content warnings in the database, for the dropdown menu in the home page'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    # curs.execute('select name from networks group by networks.name')
    curs.execute('select name from contentwarnings')
    return curs.fetchall()
    
def getCreators(conn,sid):
    '''Returns all creators of the show'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select creators.name from creators, shows, showsCreators '
                    +'where showsCreators.sid=shows.sid'+
                    ' and showsCreators.cid=creators.cid and shows.sid=%s', (sid,))
    return curs.fetchall()
    
def getGenres(conn,sid):
    '''Returns all genres of the show'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select genres.name from genres, shows, showsGenres '
                +'where showsGenres.sid=shows.sid'+
                ' and showsGenres.gid=genres.gid and shows.sid=%s', (sid,))
    return curs.fetchall()
    
def getScript(conn, sid):
    ''' Given a show ID, return the URL for the script and whether the URL is
        for a script that is stored locally or externally. Context: A script 
        can be stored one of two ways: either as a URL for an external website 
        (external) or as a  filepath that leads to a document that was uploaded 
        to the filesystem (local). '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    numrows = curs.execute('select script from shows where sid=%s', (sid,))
    row =  curs.fetchone()
    print(row)
    if "http" in row['script']:
        return row['script'], "external"
    else:
        val = send_from_directory(app.config['UPLOADS'],
                                  row['script'])
        return val, "local"

def getShow(conn,sid):
    '''Returns show with network name given sid'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select networks.name as network, shows.* from shows inner join networks on '+
                    'networks.nid = shows.nid where sid = %s', (sid,))
    return curs.fetchone()
    
def getTags(conn,sid):
    '''Returns all tags associated with a given show'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select name, val from tags where sid=%s', (sid,))
    return curs.fetchall()
    
def getWarnings(conn,sid):
    '''Returns all contentwarnings of the show'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select contentwarnings.name from contentwarnings, shows, showsCWs '
                    +'where showsCWs.sid=shows.sid'+
                    ' and showsCWs.cwid=contentwarnings.cwid and shows.sid=%s', (sid,))
    return curs.fetchall()

# By Search Terms
def getResultsByContentWarning(conn,term):
    '''Returns all shows based on the search term using network'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from shows, showsCWs, contentwarnings '
                +'where showsCWs.sid=shows.sid and contentwarnings.cwid=showsCWs.cwid '
                +'and contentwarnings.name=%s', (term,))
    return curs.fetchall()
    
def getResultsByCreator(conn,term):
    '''Returns all shows based on the search term using creator'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    term = '%' + term + '%'
    curs.execute('select * from shows, showsCreators, creators '
                +'where showsCreators.sid=shows.sid and creators.cid=showsCreators.cid '
                +'and creators.name like %s group by shows.title', (term,))
    return curs.fetchall()
    
def getResultsByGenre(conn,term):
    '''Returns all shows based on the search term using genre'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    term = '%' + term + '%'
    curs.execute('select * from shows, showsGenres, genres '
                +'where showsGenres.sid=shows.sid and genres.gid=showsGenres.gid '
                +'and genres.name like %s group by shows.title', (term,))
    return curs.fetchall()
    
def getResultsByNetwork(conn,term):
    '''Returns all shows based on the search term using network'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select networks.name as network, shows.* from shows '+
                'inner join networks on networks.nid=shows.nid where networks.name= %s', (term,))
    return curs.fetchall()
    
def getResultsByTags(conn, tag_names, tag_vals):
    ''' Returns all shows based on the search term using tags. Expects an input
        of a tuple of pairs (tag_val, tag_name) '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    tags = tuple(zip(tag_vals, tag_names))
    curs.execute('''select * from shows where sid in
                    (select sid from tags where (val, name) in %s)''', (tags,))
    return curs.fetchall()
    
def getResultsByTitle(conn,term):
    '''Returns all shows based on the search term using title'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    term = '%' + term + '%'
    curs.execute('select * from shows where title like %s', (term,))
    return curs.fetchall()

# ID Getters
def getNid(conn,networkName):
    '''Returns nid based on network name'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select nid from networks where name = %s',[networkName])
    res = curs.fetchone()
    if res:
        return res['nid']
    else:
        return None
    
def getCWid(conn,cw):
    '''Returns cwid based on contentwarning'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select cwid from contentwarnings where name = %s',[cw])
    res = curs.fetchone()
    if res:
        return res['cwid']
    else:
        return None
    
def getSid(conn,showTitle):
    '''Returns sid based on show name'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select sid from shows where title = %s',[showTitle])
    return curs.fetchone()['sid']

def getCid(conn,creatorName):
    '''Returns cid based on creator name'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select cid from creators where name = %s',[creatorName])
    res = curs.fetchone()
    if res:
        return res['cid']
    else:
        return None

def getGid(conn,genre):
    '''Returns cid based on creator name'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select gid from genres where name = %s',[genre])
    res = curs.fetchone()
    if res:
        return res['gid']
    else:
        return None
        
# Insert functions
def insertContentwarnings(conn,sid,cwList):
    ''' Inserts each creator's id first if not already in the database. 
        Also inserts the relationship (e.g. showsCWs). '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    for cw in cwList:
        lock.acquire()
        if getCWid(conn,cw) is None:
            curs.execute('insert into contentwarnings (name) values(%s)', [cw])
        cwid=getCWid(conn,cw)
        curs.execute('insert into showsCWs (sid,cwid) values (%s, %s)',[sid,cwid])
        lock.release()
        

def insertCreators(conn,sid,creatorList):
    ''' Inserts each cw's id first if not already in the database. 
        Also inserts the relationship. '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    for creator in creatorList:
        lock.acquire()
        if getCid(conn,creator) is None:
            curs.execute('insert into creators (name) values(%s)', [creator])
        cid = getCid(conn,creator)
        curs.execute('insert into showsCreators (sid,cid) values(%s, %s)',[sid,cid])
        lock.release()

def insertGenres(conn,sid,genreList):
    ''' Inserts each cw's id first if not already in the database. 
        Also inserts the relationship. '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    for genre in genreList:
        lock.acquire()
        if getGid(conn,genre) is None:
            curs.execute('insert into genres (name) values(%s)', [genre])
        gid = getGid(conn,genre)
        curs.execute('insert into showsGenres (sid,gid) values(%s, %s)',[sid,gid])
        lock.release()
        
def insertTags(conn, sid, tag_names, tag_vals):
    ''' Given a show's ID and lists of tag names and values, inserts the 
        information into the tags table. '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    for i in range(len(tag_names)):
        name = tag_names[i]
        val = tag_vals[i]
        curs.execute('insert into tags (sid, name, val) values(%s, %s, %s)', 
                    [sid, name, val])
        
def insertShows(conn, title, year, cwList, genreList, script, description, 
                creatorList, network, tag_names, tag_vals):
    ''' Inserts show, creator, show&creator relationship etc. to the database, 
        given form values '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    # check if network exists and, if not, inserts the network in the networks table
    lock.acquire()
    if getNid(conn,network) is None:
        curs.execute('insert into networks (name) values(%s)', [network])
    nid = getNid(conn,network)
    curs.execute('insert into shows (title, nid, year, script, description) values(%s, %s, %s, %s, %s)', [title, nid, year, script, description])
    sid = getSid(conn,title)
    insertContentwarnings(conn,sid,cwList)
    insertCreators(conn,sid,creatorList)
    insertGenres(conn,sid, genreList)
    if tag_names and tag_vals: # If tags info exists, insert into database
        insertTags(conn, sid, tag_names, tag_vals)
    lock.release()

def updateWarnings(conn,sid,newwarnings):
    '''Given a list of new warnings, compares it with old warnings and updates'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    lock.acquire()
    oldwarnings = [w['name'] for w in getWarnings(conn,sid)]
    #because the number of new list is not necessarily the same as the old list,
    #decided to delete and insert the differences rather than updating
    toDelete = [w for w in oldwarnings if w not in newwarnings]
    toAdd = [w for w in newwarnings if w not in oldwarnings]
    # use set
    for w in toDelete:
        cwid = getCWid(conn,w)
        curs.execute('delete from showsCWs where sid=%s and cwid=%s',[sid,cwid])
        if len(getResultsByContentWarning(conn,w))==0:
            curs.execute('delete from contentwarnings where name=%s', [w])
    for w in toAdd:
        if getCWid(conn,w) is None:
            curs.execute('insert into contentwarnings (name) values(%s)', [w])
        cwid = getCWid(conn,w)  
        curs.execute('insert into showsCWs (sid,cwid) values (%s,%s)',[sid,cwid])
    lock.release() 
        
# Helper function for script upload
def isValidScriptType(script_file, title):
    ''' Given a document from a file upload, check to see if it is a valid 
        type (.doc, .docx, .pdf). If it is, save the document to the 
        filesystem and return the filename. Otherwise flash an error message
        and return false. '''
    mimetype = script_file.content_type.split('/')[1]
    if mimetype.lower() not in ['doc','docx','pdf']:
        msg = 'ERROR: File type not a DOC, DOCX or PDF: {}'.format(mimetype)
        flash(msg)
        return False
    # If valid file type, then continue with file upload
    filename = secure_filename('{}.{}'.format(title,mimetype))
    pathname = os.path.join(app.config['UPLOADS'],filename)
    script_file.save(pathname)
    return filename 

# Update functions for Edit page
def updateCreators(conn,sid,newCreators):
    ''''Given a list of new creators, compares it with old creators and updates'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    lock.acquire()
    oldCreators = [c['name'] for c in getCreators(conn,sid)]
    toDelete = [c for c in oldCreators if c not in newCreators]
    toAdd = [c for c in newCreators if c not in oldCreators]
    for c in toDelete:
        cid = getCid(conn,c)
        curs.execute('delete from showsCreators where sid=%s and cid=%s',[sid,cid])
        if len(getResultsByCreator(conn,c))==0:
            curs.execute('delete from creators where name=%s', [c])
    for c in toAdd:
        if getCid(conn,c) is None:
            curs.execute('insert into creators (name) values(%s)', [c])
        cid = getCid(conn,c)  
        curs.execute('insert into showsCreators (sid,cid) values (%s,%s)',[sid,cid])
    lock.release()

def updateGenres(conn,sid,newGenres):
    ''''Given a list of new genres, compares it with old genres and updates'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    lock.acquire()
    oldGenres = [g['name'] for g in getGenres(conn,sid)]
    toDelete = [g for g in oldGenres if g not in newGenres]
    toAdd = [g for g in newGenres if g not in oldGenres]
    for g in toDelete:
        gid = getGid(conn,g)
        curs.execute('delete from showsGenres where sid=%s and gid=%s',[sid,gid])
        if len(getResultsByGenre(conn,g))==0:
            curs.execute('delete from genres where name=%s', [g])
    for g in toAdd:
        if getGid(conn,g) is None:
            curs.execute('insert into genres (name) values(%s)', [g])
        gid = getGid(conn,g)  
        curs.execute('insert into showsGenres (sid,gid) values (%s,%s)',[sid,gid])
    lock.release()
        
def updateTags(conn, sid, tag_names, tag_vals):
    ''' Given lists of tag names and values, update the database with new 
        tags if they do not already exist. '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    oldTags = [(tag['name'], tag['val']) for tag in getTags(conn, sid)]
    newTags = zip(tag_names, tag_vals)
    print("Old tags:", oldTags)
    toDelete = [tag for tag in oldTags if tag not in newTags]
    toAdd = [tag for tag in newTags if tag not in oldTags]
    print("Deleting:", toDelete)
    for tag in toDelete:
        curs.execute('''delete from tags where sid=%s 
                        and name=%s and val=%s''', (sid, tag[0], tag[1]))
    print("Adding:", toAdd)
    for tag in toAdd:
        curs.execute('''insert into tags (sid, name, val) 
                        values (%s, %s, %s)''', (sid, tag[0], tag[1]))
        
def updateWarnings(conn,sid,newwarnings):
    '''Given a list of new warnings, compares it with old warnings and updates'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    oldwarnings = [w['name'] for w in getWarnings(conn,sid)]
    #because the number of new list is not necessarily the same as the old list,
    #decided to delete and insert the differences rather than updating
    toDelete = [w for w in oldwarnings if w not in newwarnings]
    toAdd = [w for w in newwarnings if w not in oldwarnings]
    # use set
    for w in toDelete:
        cwid = getCWid(conn,w)
        curs.execute('delete from showsCWs where sid=%s and cwid=%s',[sid,cwid])
        if len(getResultsByContentWarning(conn,w))==0:
            curs.execute('delete from contentwarnings where name=%s', [w])
    for w in toAdd:
        if getCWid(conn,w) is None:
            curs.execute('insert into contentwarnings (name) values(%s)', [w])
        cwid = getCWid(conn,w)  
        curs.execute('insert into showsCWs (sid,cwid) values (%s,%s)',[sid,cwid])
        
# would there be the case where we want to change the sid? -- not really?
def update(conn, sid, title, year, network, genreList, cwList, script, 
           description, creators, tag_names, tag_vals):
    ''''Updates the show'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    lock.acquire()
    # old show information
    oldshow = getShow(conn,sid) #returns network name, sid, nid, title, etc.
    # Update intermediate tables first
    updateWarnings(conn,sid,cwList)
    updateCreators(conn,sid,creators)
    updateGenres(conn,sid,genreList)
    updateTags(conn, sid, tag_names, tag_vals)

    #insert if values don't exist already
    if getNid(conn,network) is None:
        curs.execute('insert into networks (name) values(%s)', [network])
    nid = getNid(conn,network)
    
    curs.execute('''update shows set title=%s, year=%s, script=%s, 
                    description=%s, nid=%s where sid=%s''', 
                    [title, year, script, description, nid, sid]) 
    # curs.execute('update tags set name=%s, val=%s where sid=%s', 
    #               (tag_name, tag_val, sid))
                    
    #delete values if none of the left shows has them
    if len(getResultsByNetwork(conn,oldshow['network']))==0:
        curs.execute('delete from networks where name=%s', [oldshow['network']])
    lock.release()

#username & joins

def checkUsername(conn, username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select username from userpass where username=%s''', [username])
    return curs.fetchone()
    
def insertUser(conn,username,hashed):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('insert into userpass(username,hashed) values (%s,%s)',[username,hashed])

def checkPW(conn,username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select hashed from userpass where username=%s',[username])
    return curs.fetchone()

if __name__ == '__main__':
    conn = getConn('final_project')