import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from datetime import datetime

# File upload section
st.title("Audience Engagement Predictor")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Read the dataset
    data = pd.read_csv(uploaded_file)
    
    # Display raw data
    st.subheader("Raw Data")
    st.write(data.head())

    # Data preprocessing
    st.subheader("Data Preprocessing")
    try:
        # Renaming columns to match Prophet requirements
        data.rename(columns={"Video publish time": "ds", "Views": "y"}, inplace=True)
        
        # Convert 'ds' column to datetime
        data['ds'] = pd.to_datetime(data['ds'], errors='coerce')
        
        # Drop rows with missing 'ds' or 'y'
        data = data.dropna(subset=['ds', 'y'])
        
        # Ensure 'y' is numeric
        data['y'] = pd.to_numeric(data['y'], errors='coerce')
        
        # Drop rows where 'y' is still NaN
        data = data.dropna(subset=['y'])
        
        st.write("Processed Data")
        st.write(data.head())
    except KeyError as e:
        st.error(f"Key error: {e}. Please ensure your dataset contains the required columns.")

    # Sidebar for prediction period
    st.sidebar.subheader("Prediction Settings")
    prediction_period = st.sidebar.number_input("Prediction period (days)", min_value=1, max_value=365, value=30)

    # Prophet model setup
    st.subheader("Prophet Model")
    model = Prophet(yearly_seasonality=True, daily_seasonality=False)
    
    try:
        # Fit the model
        model.fit(data[['ds', 'y']])
        
        # Create a future dataframe
        future = model.make_future_dataframe(periods=prediction_period)
        
        # Make predictions
        forecast = model.predict(future)
        
        # Display forecast data
        st.subheader("Forecast Data")
        st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        
        # Plot the forecast
        st.subheader("Forecast Plot")
        fig1 = model.plot(forecast)
        st.pyplot(fig1)
        
        # Plot components
        st.subheader("Forecast Components")
        fig2 = model.plot_components(forecast)
        st.pyplot(fig2)
    except Exception as e:
        st.error(f"Error in forecasting: {e}")
else:
    st.info("Please upload a CSV file to start.")
