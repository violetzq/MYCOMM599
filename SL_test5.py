import pandas as pd
import streamlit as st
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Title and Description
st.title("Refined Audience Engagement Predictor")
st.markdown("Predict YouTube views and analyze errors for better programming insights.")

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

    # Rename and clean data
    data.rename(columns={"Video publish time": "ds", "Views": "y"}, inplace=True)
    data['ds'] = pd.to_datetime(data['ds'], errors='coerce')
    data['y'] = pd.to_numeric(data['y'], errors='coerce')
    data = data.dropna(subset=['ds', 'y'])

    # Outlier detection (remove points with extremely high views)
    upper_limit = data['y'].quantile(0.99)  # 99th percentile
    data = data[data['y'] <= upper_limit]
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

st.subheader("Historical Views Over Time")
st.line_chart(data.set_index('ds')['y'])

# Split into train and test
train_data = data[data['ds'] < '2023-01-01']  # Train on data before 2023
test_data = data[data['ds'] >= '2023-01-01']  # Test on data from 2023 onwards

# Prophet Model
model = Prophet(yearly_seasonality=True, daily_seasonality=False, changepoint_prior_scale=0.5)
model.add_country_holidays(country_name='US')  # Add holiday effects

try:
    model.fit(train_data[['ds', 'y']])
    future = model.make_future_dataframe(periods=periods_input, freq='D')
    forecast = model.predict(future)

    # Evaluate predictions on test set
    test_forecast = forecast[forecast['ds'].isin(test_data['ds'])]
    mae = mean_absolute_error(test_data['y'], test_forecast['yhat'])
    mse = mean_squared_error(test_data['y'], test_forecast['yhat'])
    rmse = np.sqrt(mse)

    st.subheader("Model Performance on Test Set")
    st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
    st.write(f"Mean Squared Error (MSE): {mse:.2f}")
    st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
except Exception as e:
    st.error(f"Error during modeling or evaluation: {e}")
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

# Residual Analysis
st.subheader("Residual Analysis")
try:
    residuals = test_data['y'].values - test_forecast['yhat'].values
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.hist(residuals, bins=30, edgecolor='k')
    ax3.set_title("Residuals Distribution")
    ax3.set_xlabel("Residuals (Actual - Predicted)")
    ax3.set_ylabel("Frequency")
    st.pyplot(fig3)

    st.write("Insights from Residuals:")
    st.write("- Check if residuals are centered around zero.")
    st.write("- Look for patterns in errors (e.g., underprediction during certain periods).")
except Exception as e:
    st.error(f"Error during residual analysis: {e}")

# Insights from forecast
st.subheader("Insights from Future Forecast")
try:
    today = datetime.today()
    future_forecast = forecast[forecast['ds'] > pd.Timestamp(today.date())]

    if future_forecast.empty:
        st.warning("No future predictions found. Ensure sufficient future periods are defined in the prediction settings.")
    else:
        min_views_date = future_forecast.loc[future_forecast['yhat'].idxmin()]['ds']
        min_views = future_forecast['yhat'].min()
        max_views_date = future_forecast.loc[future_forecast['yhat'].idxmax()]['ds']
        max_views = future_forecast['yhat'].max()

        st.write(f"The lowest predicted views are {min_views:.2f}, expected on {min_views_date.date()}.")
        st.write(f"The highest predicted views are {max_views:.2f}, expected on {max_views_date.date()}.")
except Exception as e:
    st.error(f"Error generating future insights: {e}")
