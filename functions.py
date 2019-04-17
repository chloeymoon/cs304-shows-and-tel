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

# def getAllMovies(conn):
#     '''Returns a list of rows as dictionaries. selects all movies in  database'''
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('select person.name as director, movie.tt, movie.title, ' +
#              'movie.release, movie.addedby, movie.rating from person right join '
#              + 'movie on person.nm = movie.director')
#     return curs.fetchall()
    
def getResults(conn,term):
    '''Returns all shows based on the search term using title'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    term = '%' + term + '%'
    # curs.execute('select person.name as director, movie.tt, movie.title, '+
    #             'movie.release, movie.rating from person right join movie '+
    #             'on person.nm = movie.director where title like %s',(term,))
    curs.execute('select * from shows where title like %s', (term,))
    return curs.fetchall()

def getShow(conn,sid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from shows where tt = %s', (sid,))
    return curs.fetchone()

# def addUserRating(conn,tt,rating,uid):
#     '''Adds to the ratings table the tt, uid, and rating'''
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('insert into ratings (tt, uid, rating) values (%s, %s, %s) '+
#                 'on duplicate key update rating = %s',(tt,uid,rating,rating))
#     conn.commit()
#     return updateAvgRating(conn,tt) # add rating, update avrating, return dic
    
# def updateAvgRating(conn,tt):
#     '''Updates the average rating in the movie table'''
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('update movie set rating = (select avg(rating) from ratings '+
#                                         'where tt = %s) where tt = %s',(tt,tt))
#     conn.commit()
#     curs.execute('select * from movie where tt = %s',(tt,))
#     return curs.fetchone()

if __name__ == '__main__':
    conn = getConn('wmdb')

   