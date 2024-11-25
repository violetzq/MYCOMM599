import pandas as pd
import streamlit as st
from prophet import Prophet
import matplotlib.pyplot as plt

# Title and Description
st.title("Audience Engagement Predictor")
st.markdown("Analyze historical data and predict audience engagement.")

# Load Dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv"
    return pd.read_csv(url)

try:
    data = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Data preprocessing
try:
    # Ensure required columns are present
    required_columns = ["Video publish time", "Views", "Average view duration"]
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        st.stop()

    # Rename columns for compatibility with Prophet
    data.rename(columns={"Video publish time": "ds", "Views": "y"}, inplace=True)
    data['ds'] = pd.to_datetime(data['ds'], errors='coerce')  # Convert to datetime
    data['y'] = pd.to_numeric(data['y'], errors='coerce')  # Ensure 'y' is numeric
    data = data.dropna(subset=['ds', 'y'])  # Drop rows with NaN in 'ds' or 'y'

    # Ensure 'Average view duration' is numeric
    data["Average view duration"] = pd.to_numeric(data["Average view duration"], errors='coerce')
    data = data.dropna(subset=["Average view duration"])  # Drop rows with invalid values
except Exception as e:
    st.error(f"Error processing data: {e}")
    st.stop()

# Sidebar options
st.sidebar.subheader("Prediction Settings")
periods_input = st.sidebar.number_input(
    "How many future days would you like to predict?", min_value=1, max_value=730, value=365
)

# Display historical data
st.subheader("Historical Data")
st.write(data.head())

# Plot historical views over time
st.subheader("Historical Views Over Time")
try:
    st.line_chart(data.set_index('ds')['y'])
except Exception as e:
    st.error(f"Error plotting historical data: {e}")

# Model training and prediction
model = Prophet(yearly_seasonality=True, daily_seasonality=False)
try:
    model.fit(data[['ds', 'y']])
    future = model.make_future_dataframe(periods=periods_input, freq='D')
    forecast = model.predict(future)

    # Clamp negative predictions to zero
    forecast['yhat'] = forecast['yhat'].apply(lambda x: max(x, 0))

    st.subheader("Forecasted Data")
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
except Exception as e:
    st.error(f"Error during modeling: {e}")
    st.stop()

# Forecast plot
st.subheader("Forecasted Views Over Time")
try:
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    model.plot(forecast, ax=ax1)
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

# Insights from forecast
from datetime import datetime

st.subheader("Insights from Future Forecast")
try:
    # Get today's date
    today = datetime.today()

    # Filter forecast for future dates only
    future_forecast = forecast[forecast['ds'] >= pd.Timestamp(today.date())]

    if future_forecast.empty:
        st.write("No future predictions found. Check the date range in the forecast data.")
        st.write(f"Forecast start: {forecast['ds'].min()}, Forecast end: {forecast['ds'].max()}")
    else:
        # Get the lowest and highest predicted views for future dates
        min_views_date = future_forecast.loc[future_forecast['yhat'].idxmin()]['ds']
        min_views = future_forecast['yhat'].min()
        max_views_date = future_forecast.loc[future_forecast['yhat'].idxmax()]['ds']
        max_views = future_forecast['yhat'].max()

        st.write(f"The lowest predicted views are {min_views:.2f}, expected on {min_views_date.date()}.")
        st.write(f"The highest predicted views are {max_views:.2f}, expected on {max_views_date.date()}.")
except Exception as e:
    st.error(f"Error generating future insights: {e}")

# Content Length Analysis
st.subheader("Content Length Analysis")
try:
    content_length_analysis = data.groupby(data['ds'].dt.date)["Average view duration"].mean()
    st.line_chart(content_length_analysis)
    st.write("This chart shows the average view duration over time.")
except Exception as e:
    st.error(f"Error during content length analysis: {e}")
