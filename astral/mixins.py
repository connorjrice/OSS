import sqlite3
import bcrypt
from astral.util import dict_connection

"""Given functional dependencies, I'm not convinced this is the best approach.

However, the ability to separate functionality is appealing to me.
"""

class odbc(object):

    def get_dict_connection(self, cx):
        return dict_connection(cx)

    def execute(self, query):
        return self.cx.cursor().execute(query)

    def commit(self, query):
        self.cx.cursor().execute(query)
        self.cx.commit()

    def fetchall(self, query):
        return self.execute(query).fetchall()

    def fetchone(self, query):
        return self.execute(query).fetchone()

    def get_user_by_name(self, name):
        return self.fetchone(f"select * from {self.user_table} where user_name = '{name.decode('utf-8')}'")

class auth(object):
    """Has a functional dependency to odbc"""

    @staticmethod
    def hash_pw(raw_password, salt=None):
        if salt:
            try:
                salt = salt.encode('utf-8')
            except AttributeError:
                salt = salt
        else:
            salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        
        return hashed.decode('utf-8')

    def create_user(self, username, raw_password):
        quer = f"insert into {self.user_table} ([username], [bhash]) values ('{username}', '{self.hash_pw(raw_password)}')"
        print(quer)
        return self.commit(quer)

    def auth_check(self, username, password):
        quer = f"select * from {self.user_table} where username = '{username}'"
        print(quer)
        user = self.fetchone(quer)
        print(user)
        if user:
            if self.hash_pw(password, user['bhash'].encode('utf-8')) == user['bhash']:
                return user

class path(object):
    ...
