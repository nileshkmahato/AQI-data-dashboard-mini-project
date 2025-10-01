import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import plotly.express as px
from database import load_data, store_data
from etl import fetch_aqi

# Load environment variables
load_dotenv()
YOUR_API_KEY = os.getenv("YOUR_API_KEY")

# Define AQI categories with emoji
def categorize_aqi(aqi):
    if aqi <= 50: return "🟢 Good"
    elif aqi <= 100: return "🟡 Moderate"
    elif aqi <= 150: return "🟠 Unhealthy for Sensitive Groups"
    elif aqi <= 200: return "🔴 Unhealthy"
    elif aqi <= 300: return "🟣 Very Unhealthy"
    else: return "⚫ Hazardous"

# Sidebar - Select a city

cities = ['Tata Stadium, Jorapokhar, India', "Major Dhyan Chand National Stadium, Delhi, Delhi, India", "Kurla, Mumbai, India", "Ballygunge, Kolkata, India", "Hombegowda Nagar, Bengaluru, India"]
st.title("📍 Select Location")
selected_city = st.selectbox("Choose a city", cities)

# Page title
st.title("🌫️ Dhanbad AQI Dashboard")

# ETL: Fetch latest data from API and store
fetched_data = fetch_aqi(YOUR_API_KEY, selected_city)
store_data(fetched_data)

# Load data from database
df = load_data()
print(df)
# Filter by selected city only
filtered_df = df[df["location"] == selected_city]

if not filtered_df.empty:
    # Convert datetime
    filtered_df["datetime"] = pd.to_datetime(filtered_df["datetime"])

    # Add AQI category
    filtered_df["AQI Category"] = filtered_df["aqi"].apply(categorize_aqi)

    # Sort by datetime
    filtered_df = filtered_df.sort_values("datetime")

    # Line Chart using Plotly
    fig = px.line(
        filtered_df,
        x="datetime",
        y="aqi",
        markers=True,
        title="📈 Air Quality Index Over Time",
        labels={"datetime": "Date & Time", "aqi": "AQI"},
        color_discrete_sequence=["#00cc96"]
    )
    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"### 🏷️ Latest AQI for `{selected_city}` → **{filtered_df['aqi'].iloc[-1]}** ({filtered_df['AQI Category'].iloc[-1]})")
    # AQI Table
    st.subheader("🗂️ AQI Data Table")
    st.dataframe(filtered_df[["datetime", "aqi", "AQI Category", "location"]])
else:
    st.warning("No data available for the selected location.")
