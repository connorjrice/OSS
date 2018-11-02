import sqlite3
import tornado

def list_tables(path='peak.db'):
    curs = sqlite3.connect(path).cursor()
    curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return sorted([i[0] for i in curs.fetchall()])

def close_tornado():
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.close()

def dict_connection(sqlite_conn):
    def dict_factory(cursor, row):
        return {str(col[0]): row[idx] for idx, col in enumerate(cursor.description)}
    # Modify sqlite_cx to return dict instead of tuple
    sqlite_conn.row_factory = dict_factory
    return sqlite_conn

def sqlite_from_file(src, dst):
    quer = open(src, 'r').read()
    quer = [q+';' for q in quer.split(';')]
    conn = sqlite3.connect(dst)
    c = conn.cursor()
    [c.execute(q) for q in quer]
    return f'{src}->{dst} ✓'
