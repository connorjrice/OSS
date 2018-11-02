import sqlite3
import os
import random
import datetime
import pandas
 
from faker import Faker
from peak.backend import PBackend

class populate_db(object):

    def __init__(self):
        self.backend = PBackend()
        self.src = f'{os.sep}user.sql'
        self.fake = Faker()
        self.dst = self.backend.path

        self.start_date = datetime.date(2012,1,1)
        self.end_date = datetime.datetime.today().date()
        #self.fake_users = 1000 # 2011 m-cpu
        self.fake_users = 2000 # 2017 CPU

        self.max_fake_visits = self.fake_users // 10        

    def build_local(self):
        util.build_sqlite_from_file(self.src, self.dst)

    def get_random_date(self):
        year = random.randint(self.start_date.year, self.end_date.year+1)
        month = random.randint(1, 12)
        end_date = 31
        day = random.randint(1, end_date)
        while True:
            day = random.randint(1, end_date)
            try:
                date = datetime.datetime(year, month, random.randint(1, end_date))
                return date
            except ValueError:
                end_date -= 1
                continue

    def get_end_date(self, date):
        return date + datetime.timedelta(days=365)

    def populate_fake(self):
        self.populate_fake_users()
        self.populate_fake_times()
        self.populate_fake_login()

    async def await_faker(self, method):
        await self.fake.method()

    def populate_fake_users(self):
        start_time = datetime.datetime.utcnow()        
        cols = ['name', 'username', 'number', 'address', 'email', 'total_income', 'memberid',
                'start_date', 'end_date']
        rows = [['Connor Rice', 'crice', '6126665555', 'Kappa St', 'admin@peak.ninja', '350',
                 '101743', datetime.datetime(2017,9,1), datetime.datetime(2050,9,1)]]
        for i in range(0, self.fake_users):
            name = self.fake.name()
            username = f"{name.split(' ')[0][0]}{name.split(' ')[1]}".lower()
            number = self.fake.phone_number()
            address = self.fake.address()
            email = self.fake.email()
            total_income = random.randint(0, 100000)
            memberid = random.randint(101744, 10000000)            
            start_date = self.get_random_date()
            end_date = self.get_end_date(start_date)
            rows.append([name, username, number, address, email, total_income, memberid, start_date, end_date])
            
        print(f"fake users: {self.fake_users}, {datetime.datetime.utcnow() - start_time} time")
        df = pandas.DataFrame(rows, columns=cols)
        df.to_sql(self.backend.client_table, self.backend.cx, if_exists='replace', index=False)

    def populate_fake_times(self):
        start_time = datetime.datetime.utcnow()
        date_format = '%Y-%m-%d %H:%M:%S'
        user_df = pandas.read_sql(f"select * from {self.backend.client_table}", self.backend.cx)
        cols = ['member_id', 'date']
        rows = []

        for tup in user_df.itertuples():
            for rnd in range(1, random.randint(0, self.max_fake_visits+1)):
                rows.append([tup.memberid, self.fake.date_time_between_dates(
                    datetime.datetime.strptime(tup.start_date, date_format),
                    datetime.datetime.strptime(tup.start_date, date_format) + datetime.timedelta(days=400)
                )])

        print(f"fake_visits: {len(rows)} records, {datetime.datetime.utcnow() - start_time} time")
        df = pandas.DataFrame(rows, columns=cols)
        df.to_sql(self.backend.visit_table, self.backend.cx, if_exists='replace', index=False)

    def populate_fake_login(self):
        cols = ['username', 'bhash']
        df = pandas.DataFrame([], columns=cols)
        df.to_sql(self.backend.user_table, self.backend.cx, if_exists='replace', index=False)
        self.backend.create_user('admin@peak', 'kappa')
        print('admin user added')
        print(self.backend.fetchall(f"select * from {self.backend.user_table}"))


if __name__ == '__main__':
    populate_db().populate_fake()
    populate_db().populate_fake_login()
