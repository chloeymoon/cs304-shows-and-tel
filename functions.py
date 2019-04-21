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
    
def getResultsByTitle(conn,term):
    '''Returns all shows based on the search term using title'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    term = '%' + term + '%'
    curs.execute('select * from shows where title like %s', (term,))
    return curs.fetchall()
    
def getResultsByNetwork(conn,term):
    '''Returns all shows based on the search term using title'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    # term = '%' + term + '%'
    curs.execute('select networks.name as network, shows.* from shows inner join networks on networks.nid=shows.nid where networks.name= %s', (term,))
    return curs.fetchall()

def getResultsByCreator(conn,term):
    '''Returns all shows based on the search term using title'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    term = '%' + term + '%'
    curs.execute('select shows.* from shows, showsCreators, creators where showsCreators.sid=shows.sid and creators.cid=showsCreators.cid and creators.name like %s', (term,))
    return curs.fetchall()
    
def getShow(conn,sid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    #curs.execute('select * from shows where sid = %s', (sid,))
    curs.execute('select networks.name as network, shows.* from shows inner join networks on '+
                    'networks.nid = shows.nid where sid = %s', (sid,))
    return curs.fetchone()
    
def getAllNetworks(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select name from networks')
    return curs.fetchall()
    
# def updateAvgRating(conn,tt):
#     '''Updates the average rating in the movie table'''
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('update movie set rating = (select avg(rating) from ratings '+
#                                         'where tt = %s) where tt = %s',(tt,tt))
#     conn.commit()
#     curs.execute('select * from movie where tt = %s',(tt,))
#     return curs.fetchone()

if __name__ == '__main__':
    conn = getConn('c9')

   