import pandas as pd
import os
from sqlalchemy import create_engine
import pymysql

class DataBase:
    
    def __init__(self, table):
        print('Creating database connection...')
        self.get_engine = pymysql.connect(host='oege.ie.hva.nl',user='polletk', password=os.getenv('DATABASE_PASSWORD'), database='zpolletk', cursorclass=pymysql.cursors.DictCursor, ssl={"fake_flag_to_enable_tls":True})
        self.put_engine = create_engine(os.getenv('DATABASE_URL'))
        self.table = table

    def __get(self, table):
        print('\nGetting data from database...')
        return pd.read_sql_query(f"CALL allData('{table}')", con=self.get_engine)

    def get_unhcr(self):
        return self.__get('unhcr')

    def get_tweets(self):
        return self.__get(self.table)

    def get_new_id(self):
        return pd.read_sql_query(f"CALL mostRecent('{self.table}')", con=self.get_engine)

    def get_old_id(self):
        return pd.read_sql_query(f"CALL mostOld('{self.table}')", con=self.get_engine)

    def upload_data(self, df, name, error='fail'):
        try:
            df.to_sql(name=name,con=self.put_engine,if_exists=error,index=False,chunksize=1000) 
            print('succesful uloaded data')
        except Exception as e:
            print('something went wrong uploading data:', e)
        