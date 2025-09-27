import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import etl as data
from datetime import datetime

load_dotenv()   # Load environment variables from .env file
YOUR_API_KEY = os.getenv("YOUR_API_KEY")
YOUR_LOCATION = os.getenv("YOUR_LOCATION")

# API data
data=data.fetch_aqi(YOUR_API_KEY,YOUR_LOCATION)
# print(f"Here is data what we got: \n {data}") 

engine = create_engine('sqlite:///aqi_data.db')

def store_data(df):
    df.to_sql('aqi', engine, if_exists='append', index=False)
    print("Data Stored in Database. \n")

def load_data():
    print('Here is the query result of Database: \n')
    return pd.read_sql('SELECT * FROM aqi ORDER BY datetime DESC', engine)

# FIRST store data
store_data(data)

# THEN load data
print(load_data())
