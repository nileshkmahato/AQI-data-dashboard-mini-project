import os
from dotenv import load_dotenv
import streamlit as st
from database import load_data, store_data
from etl import fetch_aqi

load_dotenv()   # Load environment variables from .env file
YOUR_API_KEY = os.getenv("YOUR_API_KEY")
YOUR_LOCATION = os.getenv("YOUR_LOCATION")

st.title("🌫️ Dhanbad AQI Dashboard")

# API data by Run ETL
data=fetch_aqi(YOUR_API_KEY,YOUR_LOCATION)
# print(f"Here is data what we got: \n {data}") 


store_data(data)    # FIRST store data

# Load & Display
df = load_data()    # THEN load data
print(df)
st.line_chart(df.set_index('datetime')['aqi'])
st.dataframe(df)