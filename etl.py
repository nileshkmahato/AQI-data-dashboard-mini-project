import os
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import datetime

load_dotenv()   # Load environment variables from .env file
YOUR_API_KEY = os.getenv("YOUR_API_KEY")
YOUR_LOCATION = os.getenv("YOUR_LOCATION")

def fetch_aqi(key,location):
    url = f"https://api.waqi.info/feed/{location}/?token={key}"
    response = requests.get(url).json()
    aqi = response['data']['aqi']
    time = response['data']['time']['s']
    location=response['data']['city']['name']
    return pd.DataFrame([{'datetime': time, 'aqi': aqi , 'location':location}])

data = fetch_aqi(YOUR_API_KEY,YOUR_LOCATION)

print(data)
