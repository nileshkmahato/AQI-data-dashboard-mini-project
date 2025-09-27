from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///aqi_data.db')

def store_data(df):
    df.to_sql('aqi', engine, if_exists='append', index=False)
    print("Data Stored in Database. \n")

def load_data():
    print('Here is the query result of Database: \n')
    return pd.read_sql('SELECT * FROM aqi ORDER BY datetime DESC', engine)
