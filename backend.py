import sys
import MySQLdb

# ================================================================
# The functions that do most of the work.
# The optional arguments make it easy to play with these in the
# Python REPL
    
def getConn(db):
    '''Returns a connection'''
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db)
    conn.autocommit(True)                       
    return conn



# ================================================================
# Runs when the script is run as a script (e.g. python lookup.py)


if __name__ == '__main__':
    conn = getConn('wmdb')