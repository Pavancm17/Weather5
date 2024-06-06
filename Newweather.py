import os
import requests
import streamlit as st
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

st.markdown(
    """
    <style>
    .stApp {
        background: url("https://img.freepik.com/free-vector/sky-background-video-conferencing_23-2148623068.jpg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# OpenWeatherMap API key
API_KEY = 'afbd94da602d9d0fbd99467976150946'

# Streamlit app title and instructions
st.title("5 Days Weather Forecast")

# User inputs
place = st.text_input("NAME OF THE CITY:", "")
unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))
g_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

# Helper function to fetch weather data
def fetch_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if response.status_code != 200:
        raise Exception(data.get("message", "Error fetching data"))
    return data

# Check if city is provided
if place:
    try:
        # Fetch the 5-day forecast data
        data = fetch_weather_data(place, API_KEY)

        # Extract data from forecast and filter for the next 5 days including today
        now = datetime.utcnow()
        end_date = now + timedelta(days=5)
        dates = []
        temps = []

        for entry in data['list']:
            date = datetime.utcfromtimestamp(entry['dt'])
            if now <= date < end_date:
                dates.append(date)
                temp_kelvin = entry['main']['temp']
                temp = temp_kelvin - 273.15 if unit == 'Celsius' else (temp_kelvin - 273.15) * 9/5 + 32
                temps.append(temp)

        # Fetch current weather for additional information
        current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}"
        current_weather_response = requests.get(current_weather_url)
        current_weather_data = current_weather_response.json()
        current_weather = current_weather_data['main']

        # Plot the data
        def plot_line_chart(dates, temps):
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(dates, temps, label='Temperature', color='blue')
            ax.fill_between(dates, temps, color='lightblue', alpha=0.4)
            ax.set_xlabel('Date')
            ax.set_ylabel(f'Temperature ({unit})')
            ax.set_title('5 Day Weather Forecast')
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

        def plot_bar_chart(dates, temps):
            fig, ax = plt.subplots(figsize=(10, 5))
            width = timedelta(hours=2)  # width of the bars
            ax.bar(dates, temps, width=width, label='Temperature', color='blue', alpha=0.6)
            ax.set_xlabel('Date')
            ax.set_ylabel(f'Temperature ({unit})')
            ax.set_title('5 Days Weather Forecast')
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Choose the graph type and plot
        if g_type == 'Line Graph':
            plot_line_chart(dates, temps)
        elif g_type == 'Bar Graph':
            plot_bar_chart(dates, temps)

        # Additional weather information from current weather
        sunrise = datetime.utcfromtimestamp(current_weather_data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
        sunset = datetime.utcfromtimestamp(current_weather_data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')
        wind_speed = current_weather_data['wind']['speed']  # Wind speed in m/s
        wind_speed_kmh = wind_speed * 3.6  # Convert m/s to km/h
        humidity = current_weather['humidity']

        st.write(f"The current humidity is {humidity}%")
        st.write(f"Sunrise at: {sunrise}")
        st.write(f"Sunset at: {sunset}")
        st.write("Add 2 hours, as local time to Sunrise and Sunset")
        st.write(f"Wind speed: {wind_speed_kmh:.2f} km/h")

    except Exception as e:
        st.error(f"Error fetching data: {e}")
else:
    st.write("Input a CITY!")
