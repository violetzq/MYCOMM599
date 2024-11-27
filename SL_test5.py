import pandas as pd
import streamlit as st
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Title and Description
st.title("Audience Engagement Predictor with Validation")
st.markdown("Use historical data to predict future audience engagement and validate model accuracy.")

# Load Dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv"
    return pd.read_csv(url)

try:
    data = load_data()
    data.rename(columns={"Video publish time": "ds", "Views": "y"}, inplace=True)
    data['ds'] = pd.to_datetime(data['ds'], errors='coerce')
    data['y'] = pd.to_numeric(data['y'], errors='coerce')
    data = data.dropna(subset=['ds', 'y'])
except Exception as e:
    st.error(f"Error loading or processing data: {e}")
    st.stop()

# Split the data into training and testing sets
split_date = st.sidebar.date_input("Select Training/Test Split Date", value=data['ds'].iloc[int(len(data) * 0.8)])
train_data = data[data['ds'] <= pd.Timestamp(split_date)]
test_data = data[data['ds'] > pd.Timestamp(split_date)]

# Display split data information
st.subheader("Training and Testing Data Split")
st.write(f"Training Data: {len(train_data)} rows, Testing Data: {len(test_data)} rows")
st.write(f"Training Data Range: {train_data['ds'].min()} to {train_data['ds'].max()}")
st.write(f"Testing Data Range: {test_data['ds'].min()} to {test_data['ds'].max()}")

# Train the model on the training set
model = Prophet(yearly_seasonality=True, daily_seasonality=False)
model.fit(train_data)

# Forecast for the test set dates
future = model.make_future_dataframe(periods=len(test_data), freq='D')
forecast = model.predict(future)

# Filter forecast to test set dates only
test_forecast = forecast[forecast['ds'].isin(test_data['ds'])]

# Calculate accuracy metrics
if not test_forecast.empty:
    mae = mean_absolute_error(test_data['y'], test_forecast['yhat'])
    rmse = np.sqrt(mean_squared_error(test_data['y'], test_forecast['yhat']))
    st.subheader("Validation Metrics")
    st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
    st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

    # Plot Actual vs. Predicted
    st.subheader("Actual vs. Predicted Views (Test Set)")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(test_data['ds'], test_data['y'], label='Actual', marker='o')
    ax.plot(test_forecast['ds'], test_forecast['yhat'], label='Predicted', marker='x')
    ax.set_title("Actual vs. Predicted Views")
    ax.set_xlabel("Date")
    ax.set_ylabel("Views")
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("No predictions available for the test set.")

# Insights from future forecast
st.subheader("Future Forecast Insights")
future_forecast = forecast[forecast['ds'] > datetime.today()]
if not future_forecast.empty:
    min_views_date = future_forecast.loc[future_forecast['yhat'].idxmin()]['ds']
    min_views = future_forecast['yhat'].min()
    max_views_date = future_forecast.loc[future_forecast['yhat'].idxmax()]['ds']
    max_views = future_forecast['yhat'].max()
    st.write(f"The lowest predicted views are {min_views:.2f}, expected on {min_views_date.date()}.")
    st.write(f"The highest predicted views are {max_views:.2f}, expected on {max_views_date.date()}.")
else:
    st.warning("No future predictions available.")
