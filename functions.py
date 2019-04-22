'''Functions interacting with the backend that will be used in app.py.
Written Spring 2019
Chloe Moon
'''
import sys
import MySQLdb

def getConn(db):
    '''Connects to local host'''
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db)
    return conn
    
def getAllNetworks(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select name from networks')
    return curs.fetchall()
    
def getCreators(conn,sid): #get creators by show id
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select creators.name from creators, shows, showsCreators '
                    +'where showsCreators.sid=shows.sid'+
                    ' and showsCreators.cid=creators.cid and shows.sid=%s', (sid,))
    return curs.fetchall()

def getShow(conn,sid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    #curs.execute('select * from shows where sid = %s', (sid,))
    curs.execute('select networks.name as network, shows.* from shows inner join networks on '+
                    'networks.nid = shows.nid where sid = %s', (sid,))
    return curs.fetchone()

def getResultsByCreator(conn,term):
    '''Returns all shows based on the search term using creator'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    term = '%' + term + '%'
    curs.execute('select * from shows, showsCreators, creators '
                +'where showsCreators.sid=shows.sid and creators.cid=showsCreators.cid '
                +'and creators.name like %s group by shows.title', (term,))
    return curs.fetchall()
    
def getResultsByNetwork(conn,term):
    '''Returns all shows based on the search term using network'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select networks.name as network, shows.* from shows '+
                'inner join networks on networks.nid=shows.nid where networks.name= %s', (term,))
    return curs.fetchall()
    
def getResultsByTitle(conn,term):
    '''Returns all shows based on the search term using title'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    term = '%' + term + '%'
    curs.execute('select * from shows where title like %s', (term,))
    return curs.fetchall()
    
def insertShows(conn, title, year, genre, script, description, creator, network):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('insert into shows (title, year, genre, script, description) values(%s, %s, %s, %s, %s)', [title, year, genre, script, description])
    curs.execute('insert into creators (name) values(%s)', [creator])
    curs.execute('insert into networks (name) values(%s)', [network])
    

if __name__ == '__main__':
    conn = getConn('c9')