import astral.mixins
import datetime
import sqlite3
import os

class PBackend(astral.mixins.odbc, astral.mixins.auth):

    def __init__(self):
        super().__init__()
        self.path = f'.{os.sep}peak{os.sep}peak.db'
        self.cx = sqlite3.connect(self.path)
        self.cx = self.get_dict_connection(self.cx)
        #        self.autocommit()
        self.user_table = 'users'
        self.visit_table = 'visits'
        self.client_table = 'clients'

    def insert_checkin(self, memberid):
        self.execute(f'insert into [peak].user_tracking (member_id, datetime, timezone) values ({memberid}, {datetime.datetime.utcnow().isoformat()}')

    def get_client(self, memberid):
        return self.fetchall(f'select * from [peak].clients where memberid = {memberid}')

    def get_user(self, username):
        return self.fetchall(f'select * from {self.user_table}')
