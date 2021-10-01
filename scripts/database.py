import pandas as pd
import os
from sqlalchemy import create_engine
import pymysql

class DataBase:
    
    def __init__(self):
        self.get_engine = pymysql.connect(host='oege.ie.hva.nl',user='polletk', password=os.getenv('DATABASE_PASSWORD'), database='zpolletk', cursorclass=pymysql.cursors.DictCursor)
        self.put_engine = create_engine(os.getenv('DATABASE_URL'))

    def get_unhcr(self):
        return pd.read_sql_query("CALL allDataUn()", con=self.get_engine)

    def get_tweets(self):
        return pd.read_sql_query("CALL allDataTweets()", con=self.get_engine)

    def upload_data(self, df, name, error='fail'):
        try:
            df.to_sql(name=name,con=self.put_engine,if_exists=error,index=False,chunksize=1000) 
            print('succesful uloaded data')
        except Exception as e:
            print('something went wrong:', e)
        