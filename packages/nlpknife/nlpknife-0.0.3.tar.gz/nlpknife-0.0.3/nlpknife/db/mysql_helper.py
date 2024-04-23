'''
Description: MySQL
Version: 0.0.1
Author: aka.zhp
Date: 2024-01-04 11:00:24
LastEditTime: 2024-01-04 11:11:25
'''
import pymysql
import traceback
import pandas as pd

class MysqlHelper:
    def __init__(self, host, port, user, password, database):
        self.db = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            autocommit=True
        )
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

    def read_sql(self, sql=None) -> pd.DataFrame:
        self.db.ping(reconnect=True)
        self.cursor.execute(sql)
        cols = [item[0] for item in self.cursor.description]
        data = self.cursor.fetchall()
        if len(data) != 0:
            data = pd.DataFrame(data)
            data.columns = cols
        else:
            data = pd.DataFrame()
        return data

    def batch_insert_data(self, sql, datas):
        try:
            self.cursor.executemany(sql, datas)
            self.db.commit()
        except Exception as e:
             print(traceback.format_exc())

    def insert_data(self, sql, datas):
        try:
            self.cursor.execute(sql, datas)
            self.db.commit()
        except Exception as e:
            print(traceback.format_exc())