import sqlite3


class Sqlite(object):

    def __init__(self):
        self.conn = False

    def connect(self, database):
        self.conn = sqlite3.connect(database)

    def execute(self, sql, obj):
        cur = self.conn.cursor()
        cur.execute(sql, obj)
        return cur

    def fecth_one(self, cursor):
        return cursor.fetchone()

    def commit(self):
        self.conn.commit()
