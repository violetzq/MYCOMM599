import pandas as pd
import streamlit as st
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

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
    st.stop()

# Data preprocessing
try:
    if "Video publish time" not in data.columns or "Views" not in data.columns:
        st.error("Required columns are missing from the dataset.")
        st.stop()

    data.rename(columns={"Video publish time": "ds", "Views": "y"}, inplace=True)
    data['ds'] = pd.to_datetime(data['ds'], errors='coerce')
    data['y'] = pd.to_numeric(data['y'], errors='coerce')
    data = data.dropna(subset=['ds', 'y'])
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
if not data.empty:
    st.write(data.head())
    st.subheader("Historical Views Over Time")
    try:
        st.line_chart(data.set_index('ds')['y'])
    except Exception as e:
        st.error(f"Error plotting historical data: {e}")
else:
    st.error("No historical data available to display.")
    st.stop()

# Train-test split
split_date = st.sidebar.date_input(
    "Select a test set split date:",
    value=data['ds'].iloc[-int(len(data) * 0.2)],
    min_value=data['ds'].min(),
    max_value=data['ds'].max()
)
train_data = data[data['ds'] < pd.Timestamp(split_date)]
test_data = data[data['ds'] >= pd.Timestamp(split_date)]

# Model training and prediction
model = Prophet(yearly_seasonality=True, daily_seasonality=False)
try:
    model.fit(train_data[['ds', 'y']])
    future = model.make_future_dataframe(periods=periods_input, freq='D')
    forecast = model.predict(future)
    st.write(f"Future DataFrame start: {future['ds'].min()}, Future DataFrame end: {future['ds'].max()}")
    st.subheader("Forecasted Data")
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
except Exception as e:
    st.error(f"Error during future prediction: {e}")
    st.stop()

# Clamp negative predictions to zero
forecast['yhat'] = forecast['yhat'].apply(lambda x: max(x, 0))

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

# Model evaluation
st.subheader("Model Evaluation")
try:
    # Align test data and forecast
    test_forecast = forecast[forecast['ds'].isin(test_data['ds'])]
    aligned_test_data = test_data[test_data['ds'].isin(test_forecast['ds'])].reset_index(drop=True)
    test_forecast = test_forecast.reset_index(drop=True)

    # Ensure alignment
    if len(aligned_test_data['y']) == len(test_forecast['yhat']):
        mae = mean_absolute_error(aligned_test_data['y'], test_forecast['yhat'])
        mse = mean_squared_error(aligned_test_data['y'], test_forecast['yhat'])
        rmse = np.sqrt(mse)

        st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
        st.write(f"Mean Squared Error (MSE): {mse:.2f}")
        st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    else:
        st.warning("Mismatch in data lengths between test data and forecast.")
except Exception as e:
    st.error(f"Error evaluating model: {e}")

# Insights from forecast
st.subheader("Insights from Future Forecast")
try:
    today = datetime.today()
    future_forecast = forecast[forecast['ds'] > pd.Timestamp(today.date())]

    if future_forecast.empty:
        st.warning("No future predictions found. Ensure sufficient future periods are defined in the prediction settings.")
        st.write(f"Forecast available from: {forecast['ds'].min()} to {forecast['ds'].max()}.")
    else:
        min_views_date = future_forecast.loc[future_forecast['yhat'].idxmin()]['ds']
        min_views = future_forecast['yhat'].min()
        max_views_date = future_forecast.loc[future_forecast['yhat'].idxmax()]['ds']
        max_views = future_forecast['yhat'].max()

        st.write(f"The lowest predicted views are {min_views:.2f}, expected on {min_views_date.date()}.")
        st.write(f"The highest predicted views are {max_views:.2f}, expected on {max_views_date.date()}.")
except Exception as e:
    st.error(f"Error generating future insights: {e}")
