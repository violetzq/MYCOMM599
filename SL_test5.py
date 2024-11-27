import pandas as pd
import numpy as np
import streamlit as st
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime

# Title and Description
st.title("Audience Engagement Predictor with Model Evaluation")
st.markdown("Use historical data to predict future audience engagement and evaluate model accuracy.")

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
    data['y'] = pd.to_numeric(data['y'], errors='coerce')  # Ensure Views is numeric
    data = data.dropna(subset=['ds', 'y'])

    # Handle duplicate timestamps by aggregating with the mean
    data = data.groupby('ds', as_index=False).agg({'y': 'mean'})
except Exception as e:
    st.error(f"Error processing data: {e}")
    st.stop()

# Split data into train and test sets
split_date = st.sidebar.date_input("Select Train/Test Split Date", datetime(2023, 1, 1))
train_data = data[data['ds'] < pd.Timestamp(split_date)]
test_data = data[data['ds'] >= pd.Timestamp(split_date)]

if train_data.empty or test_data.empty:
    st.error("Train or test dataset is empty. Adjust the split date.")
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

# Model training and prediction
model = Prophet(yearly_seasonality=True, daily_seasonality=False, changepoint_prior_scale=0.5)
model.add_country_holidays(country_name='US')  # Add holiday effects

try:
    model.fit(train_data[['ds', 'y']])
    future = model.make_future_dataframe(periods=periods_input, freq='D')
    forecast = model.predict(future)
    
    # Align test_forecast with test_data
    test_forecast = forecast[forecast['ds'].isin(test_data['ds'])].set_index('ds')
    aligned_test_data = test_data.set_index('ds').reindex(test_forecast.index)

    # Calculate evaluation metrics
    mae = mean_absolute_error(aligned_test_data['y'], test_forecast['yhat'])
    mse = mean_squared_error(aligned_test_data['y'], test_forecast['yhat'])
    rmse = np.sqrt(mse)

    st.subheader("Model Performance on Test Set")
    st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
    st.write(f"Mean Squared Error (MSE): {mse:.2f}")
    st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

    st.write(f"Future DataFrame start: {future['ds'].min()}, Future DataFrame end: {future['ds'].max()}")
    st.subheader("Forecasted Data")
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
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
