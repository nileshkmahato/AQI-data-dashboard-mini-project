import requests
import pandas as pd

def fetch_aqi(key,location):
    url = f"https://api.waqi.info/feed/{location}/?token={key}"
    response = requests.get(url).json()
    aqi = response['data']['aqi']
    time = response['data']['time']['s']
    location=response['data']['city']['name']
    return pd.DataFrame([{'datetime': time, 'aqi': aqi , 'location':location}])

# # To test data
# data = fetch_aqi(YOUR_API_KEY,YOUR_LOCATION)
# print(f"Here is data what we got: \n {data}")
