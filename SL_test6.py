# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Uckx2V4CZbWO_AiW1AEJJjX3MdaGEykL
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from prophet.plot import plot_plotly
import numpy as np

# Set Streamlit page configuration
st.set_page_config(page_title="Audience Engagement Predictor", layout="wide")

# Load dataset from GitHub
data_url = 'https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv'
data = pd.read_csv(data_url, encoding='ISO-8859-1')

# Preprocess data
data['Video publish time'] = pd.to_datetime(data['Video publish time'])
data = data.rename(columns={'Video publish time': 'ds', 'Views': 'y'})

# Handle missing or negative values in 'y'
data = data.dropna(subset=['y'])
data = data[data['y'] >= 0]  # Keep only non-negative values

# Train Prophet model
st.title("Audience Engagement Predictor")
st.markdown("Use historical data to predict future audience engagement metrics.")
model = Prophet(yearly_seasonality=True, daily_seasonality=False)
model.fit(data[['ds', 'y']])

# Forecast future values
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

# Clamp negative predictions to zero
forecast['yhat'] = forecast['yhat'].clip(lower=0)
forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0)
forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=0)

# Plot predictions
st.subheader("Forecasted Views Over Time")
fig1 = plot_plotly(model, forecast)
st.plotly_chart(fig1, use_container_width=True)

# Key Insights
st.subheader("Key Insights")
highest_prediction = forecast[['ds', 'yhat']].sort_values(by='yhat', ascending=False).iloc[0]
lowest_prediction = forecast[['ds', 'yhat']].sort_values(by='yhat', ascending=True).iloc[0]

st.markdown(f"- The **highest predicted Views** is **{highest_prediction['yhat']:.2f}**, expected on **{highest_prediction['ds'].strftime('%Y-%m-%d')}**.")
st.markdown(f"- The **lowest predicted Views** is **{lowest_prediction['yhat']:.2f}**, expected on **{lowest_prediction['ds'].strftime('%Y-%m-%d')}**.")

# Visualize trends
st.subheader("Components of the Forecast")
fig2 = model.plot_components(forecast)
st.pyplot(fig2)

# Optional: Show raw data
st.subheader("Raw Forecast Data")
if st.checkbox("Show Forecast Data"):
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
