import os
import pytz
import pyowm
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

# Initialize the OpenWeatherMap API with your API key
owm = pyowm.OWM('afbd94da602d9d0fbd99467976150946')
mgr = owm.weather_manager()

# Streamlit app title and instructions
st.title("5 Days Weather Forecast")

# User inputs
place = st.text_input("NAME OF THE CITY:", "")
unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))
g_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

# Check if city is provided
if place:
    try:
        # Fetch the 5-day forecast data with 3-hour intervals
        forecaster = mgr.forecast_at_place(place, '3h')
        forecast = forecaster.forecast

        # Fetch current weather for additional information
        current_weather = mgr.weather_at_place(place).weather

        # Extract data from forecast and filter for the next 5 days including today
        now = datetime.utcnow()
        end_date = now + timedelta(days=5)
        dates = []
        temps = []

        for weather in forecast:
            date = datetime.utcfromtimestamp(weather.reference_time())
            if now <= date < end_date:
                dates.append(date)
                temps.append(weather.temperature(unit='celsius' if unit == 'Celsius' else 'fahrenheit')['temp'])

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
        sunrise = current_weather.sunrise_time(timeformat='iso')
        sunset = current_weather.sunset_time(timeformat='iso')
        wind_speed = current_weather.wind()['speed']  # Wind speed in m/s
        wind_speed_kmh = wind_speed * 3.6  # Convert m/s to km/h
        humidity = current_weather.humidity

        st.write(f"The current humidity is {humidity}%")
        st.write(f"Sunrise at: {sunrise}")
        st.write(f"Sunset at: {sunset}")
        st.write("Add 2 hours, as local time to Sunrise and Sunset")
        st.write(f"Wind speed: {wind_speed_kmh:.2f} km/h")

    except Exception as e:
        st.error(f"Error fetching data: {e}")
else:
    st.write("Input a CITY!")
