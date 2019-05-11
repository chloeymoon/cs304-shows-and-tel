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
    conn.autocommit(True) 
    return conn
    
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
    
def getWarnings(conn,sid):
    '''Returns all contentwarnings of the show'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select contentwarnings.name from contentwarnings, shows, showsCWs '
                    +'where showsCWs.sid=shows.sid'+
                    ' and showsCWs.cwid=contentwarnings.cwid and shows.sid=%s', (sid,))
    return curs.fetchall()

def getShow(conn,sid):
    '''Returns show with network name given sid'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
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
    
def getResultsByContentWarning(conn,term):
    '''Returns all shows based on the search term using network'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from shows, showsCWs, contentwarnings '
                +'where showsCWs.sid=shows.sid and contentwarnings.cwid=showsCWs.cwid '
                +'and contentwarnings.name=%s', (term,))
    return curs.fetchall()
    
def getResultsByTags(conn, tag_names, tag_vals):
    '''Returns all shows based on the search term using tags'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from shows''')
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

# helper functions for insertShows
# many-to-many relationships (Contentwarnings, Creators)
# inserts each creator/cw's id first if not already in the database
# also inserts the relationship (e.g. showsCWs)
def insertContentwarnings(conn,sid,cwList):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    for cw in cwList:
        if getCWid(conn,cw) is None:
            curs.execute('insert into contentwarnings (name) values(%s)', [cw])
        cwid=getCWid(conn,cw)
        curs.execute('insert into showsCWs (sid,cwid) values (%s, %s)',[sid,cwid])

def insertCreators(conn,sid,creatorList):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    for creator in creatorList:
        if getCid(conn,creator) is None:
            curs.execute('insert into creators (name) values(%s)', [creator])
        cid = getCid(conn,creator)
        curs.execute('insert into showsCreators (sid,cid) values(%s, %s)',[sid,cid])

def insertShows(conn, title, year, genre, cwList, script, description, creatorList, network):
    '''Inserts show, creator, show&creator relationship etc. to the database, given form values'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    # check if network exists and, if not, inserts the network in the networks table
    if getNid(conn,network) is None:
        curs.execute('insert into networks (name) values(%s)', [network])
    nid = getNid(conn,network)
    curs.execute('insert into shows (title, nid, year, genre, script, description) values(%s, %s, %s, %s, %s, %s)', [title, nid, year, genre, script, description])
    sid = getSid(conn,title)
    insertContentwarnings(conn,sid,cwList)
    insertCreators(conn,sid,creatorList)

# would there be the case where we want to change the sid? -- not really?
def update(conn, sid, title, year, oldnetwork, network, genre, oldcwList, newcwList, script, description, creators):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    if getNid(conn,network) is None:
        curs.execute('insert into networks (name) values(%s)', [network])
    nid = getNid(conn,network)
    curs.execute('''update shows set title=%s, year=%s, genre=%s, script=%s, 
                    description=%s, nid=%s where sid=%s''', 
                    [title, year, genre, script, description, nid, sid]) 
    # if only this show has this network, delete network from networks table or not?
    if len(getResultsByNetwork(conn,oldnetwork))==0:
        curs.execute('delete from networks where name=%s', [oldnetwork])
    # for creator in creators:
    #     if getCid(conn,creator) is None:
    #         curs.execute('insert into creators (name) values(%s)', [creator])
    #     cid = getCid(conn,creator)
    #     # curs.execute('update creators set name=%s where sid=%s', [creator,sid])
    #     curs.execute('update showsCreators set cid=%s where sid=%s',[cid,sid])
    

if __name__ == '__main__':
    conn = getConn('final_project')