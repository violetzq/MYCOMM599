import pandas as pd
import streamlit as st
from prophet import Prophet
from prophet.plot import plot_components_plotly
import matplotlib.pyplot as plt
from io import BytesIO

# Title and Description
st.title("Audience Engagement Predictor")
st.markdown("Use historical data to predict future audience engagement.")

# Load Dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv"
    return pd.read_csv(url)

try:
    data = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")

# Data preprocessing
try:
    data.rename(columns={"Video publish time": "ds", "Views": "y"}, inplace=True)
    data['ds'] = pd.to_datetime(data['ds'], errors='coerce')  # Convert to datetime
    data = data.dropna(subset=['ds', 'y'])  # Drop rows with NaN in 'ds' or 'y'
    data['y'] = pd.to_numeric(data['y'], errors='coerce')  # Ensure 'y' is numeric
    data = data.dropna(subset=['y'])  # Drop rows with NaN in 'y'
except KeyError as e:
    st.error(f"Column missing in dataset: {e}")

# Sidebar options
st.sidebar.subheader("Prediction Settings")
periods_input = st.sidebar.number_input(
    "How many future days would you like to predict?", min_value=1, max_value=365, value=30
)

# Display historical data
st.subheader("Historical Data")
st.write(data.head())

# Plot historical data
st.line_chart(data.set_index('ds')['y'])

# Model training and prediction
model = Prophet(yearly_seasonality=True, daily_seasonality=False)
try:
    model.fit(data[['ds', 'y']])
    future = model.make_future_dataframe(periods=periods_input)
    forecast = model.predict(future)
    st.subheader("Forecasted Data")
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
except Exception as e:
    st.error(f"Error during modeling: {e}")

# Forecast plot
st.subheader("Forecasted Views Over Time")
try:
    fig1 = model.plot(forecast)
    st.pyplot(fig1)
except Exception as e:
    st.error(f"Error generating forecast plot: {e}")

# Components plot
st.subheader("Forecast Components")
try:
    fig2 = model.plot_components(forecast)
    st.pyplot(fig2)
except Exception as e:
    st.error(f"Error generating components plot: {e}")

# Debugging: Display changepoint trends without `add_changepoints_to_plot`
st.subheader("Changepoint Analysis")
try:
    fig3 = model.plot(forecast)
    st.pyplot(fig3)
except Exception as e:
    st.error(f"Error generating changepoint analysis: {e}")

# Insights from forecast
st.subheader("Insights from Forecast")
try:
    min_views_date = forecast.loc[forecast['yhat'].idxmin()]['ds']
    min_views = forecast['yhat'].min()
    max_views_date = forecast.loc[forecast['yhat'].idxmax()]['ds']
    max_views = forecast['yhat'].max()

    st.write(f"The lowest predicted views are {min_views:.2f}, expected on {min_views_date.date()}.")
    st.write(f"The highest predicted views are {max_views:.2f}, expected on {max_views_date.date()}.")
except Exception as e:
    st.error(f"Error generating insights: {e}")

# Debugging forecast DataFrame
st.subheader("Debugging Data")
if st.checkbox("Show Forecast Data"):
    st.write(forecast.head())
