import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objs as go

# Ensure required libraries are installed
os.system('pip install plotly==5.24.1')

# Set page configuration
st.set_page_config(page_title="Audience Engagement Predictor", layout="wide")

# Load the dataset
data_url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv"
data = pd.read_csv(data_url, encoding="ISO-8859-1")

# Data preprocessing
data.rename(columns={"Publish date": "ds", "Views": "y"}, inplace=True)
data['ds'] = pd.to_datetime(data['ds'], errors='coerce')  # Convert to datetime and handle errors
data = data.dropna(subset=['ds', 'y'])  # Drop rows with NaN in 'ds' or 'y'

# Sidebar options
st.sidebar.header("Prediction Settings")
periods_input = st.sidebar.number_input(
    "Number of days to predict:",
    min_value=30,
    max_value=365,
    value=90,
    step=10
)

# Main title
st.title("Audience Engagement Predictor")
st.markdown("Use historical data to predict future audience engagement metrics.")

# Show historical data
st.subheader("Historical Data")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(data['ds'], data['y'], label='Views')
ax.set_title("Historical Views Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Views")
ax.legend()
st.pyplot(fig)

# Prophet model fitting
st.subheader("Prophet Model and Forecasting")
with st.spinner("Training the model..."):
    model = Prophet(yearly_seasonality=True, daily_seasonality=False)
    model.fit(data[['ds', 'y']])

# Forecast future values
future = model.make_future_dataframe(periods=int(periods_input))
forecast = model.predict(future)

# Replace negative predictions with zero
forecast['yhat'] = forecast['yhat'].clip(lower=0)

# Display forecast data
st.subheader("Forecast Results")
st.write(f"Predictions for the next {periods_input} days:")
st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods_input))

# Plot forecast
st.subheader("Forecasted Views Over Time")
fig1 = plot_plotly(model, forecast)
st.plotly_chart(fig1, use_container_width=True)

# Key insights
st.subheader("Key Insights")
lowest_pred = forecast.loc[forecast['yhat'].idxmin()]
highest_pred = forecast.loc[forecast['yhat'].idxmax()]

st.markdown(f"- The **lowest predicted views** are **{lowest_pred['yhat']:.0f}** on **{lowest_pred['ds'].date()}**.")
st.markdown(f"- The **highest predicted views** are **{highest_pred['yhat']:.0f}** on **{highest_pred['ds'].date()}**.")

# Highlight trends
st.subheader("Future Trends")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Predicted Views'
))
fig2.update_layout(
    title="Predicted Views Over Time",
    xaxis_title="Date",
    yaxis_title="Views",
    showlegend=True
)
st.plotly_chart(fig2, use_container_width=True)
