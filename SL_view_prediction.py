import pandas as pd
import numpy as np
import streamlit as st
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import matplotlib.pyplot as plt

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

    # Remove outliers using the IQR method
    Q1 = data['y'].quantile(0.25)
    Q3 = data['y'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data = data[(data['y'] >= lower_bound) & (data['y'] <= upper_bound)]

    st.write("Outliers removed using IQR method.")
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

# Model training and prediction
model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
try:
    model.fit(data[['ds', 'y']])
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

# Cross-validation and performance metrics
st.subheader("Model Performance Metrics")
try:
    df_cv = cross_validation(model, initial='730 days', period='180 days', horizon='365 days')
    df_p = performance_metrics(df_cv)
    st.write(df_p)

    st.write("**Insights from Performance Metrics:**")
    st.write("- MAE (Mean Absolute Error) gives the average magnitude of errors in the predictions.")
    st.write("- RMSE (Root Mean Squared Error) is more sensitive to larger errors due to squaring.")
    st.write("- Use these metrics to evaluate and improve the model.")
except Exception as e:
    st.error(f"Error during cross-validation: {e}")

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
