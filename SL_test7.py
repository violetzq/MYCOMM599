import pandas as pd
import streamlit as st
from prophet import Prophet
from prophet.plot import plot_plotly, add_changepoints_to_plot
import matplotlib.pyplot as plt

# Load your data from GitHub
url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/335eecad5c20fd988c8dc65408218972c1201db1/DangerTV_Content.csv"
data = pd.read_csv(url)

# Data preprocessing
data.rename(columns={"Video publish time": "ds", "Views": "y"}, inplace=True)
data['ds'] = pd.to_datetime(data['ds'], errors='coerce')  # Convert to datetime
data = data.dropna(subset=['ds', 'y'])  # Drop rows with NaN in 'ds' or 'y'

# Sidebar options
st.sidebar.header("Prediction Configuration")
forecast_days = st.sidebar.slider("Select forecast period (days):", 30, 365, 90)

# Model training
model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
model.fit(data[['ds', 'y']])

# Forecast future values
future = model.make_future_dataframe(periods=forecast_days)
forecast = model.predict(future)

# Visualize historical data
st.title("Audience Engagement Predictor")
st.subheader("Historical Data")
fig, ax = plt.subplots()
data.plot(x='ds', y='y', ax=ax, title="Historical Views Over Time")
st.pyplot(fig)

# Forecast Visualization
st.subheader("Forecasted Views Over Time")
fig1 = plot_plotly(model, forecast)
st.plotly_chart(fig1)

# Seasonal Components
st.subheader("Seasonality Analysis")
fig2 = model.plot_components(forecast)
st.pyplot(fig2)

# Generate Insights
st.subheader("Key Insights")
# 1. Find the highest and lowest predicted values
highest_prediction = forecast[['ds', 'yhat']].sort_values(by='yhat', ascending=False).iloc[0]
lowest_prediction = forecast[['ds', 'yhat']].sort_values(by='yhat', ascending=True).iloc[0]

st.markdown(f"**Highest Predicted Views:** {highest_prediction['yhat']:.2f} on {highest_prediction['ds'].date()}")
st.markdown(f"**Lowest Predicted Views:** {lowest_prediction['yhat']:.2f} on {lowest_prediction['ds'].date()}")

# 2. Analyze seasonality contributions
weekly_seasonality = forecast[['ds', 'weekly']]
yearly_seasonality = forecast[['ds', 'yearly']]

# Day with the highest weekly seasonality
highest_weekly = weekly_seasonality.sort_values(by='weekly', ascending=False).iloc[0]
lowest_weekly = weekly_seasonality.sort_values(by='weekly', ascending=True).iloc[0]

st.markdown(f"**Day with highest weekly contribution:** {highest_weekly['ds'].date()} ({highest_weekly['weekly']:.2f})")
st.markdown(f"**Day with lowest weekly contribution:** {lowest_weekly['ds'].date()} ({lowest_weekly['weekly']:.2f})")

# Month with the highest yearly contribution
highest_yearly = yearly_seasonality.sort_values(by='yearly', ascending=False).iloc[0]
lowest_yearly = yearly_seasonality.sort_values(by='yearly', ascending=True).iloc[0]

st.markdown(f"**Month with highest yearly contribution:** {highest_yearly['ds'].strftime('%B')} ({highest_yearly['yearly']:.2f})")
st.markdown(f"**Month with lowest yearly contribution:** {lowest_yearly['ds'].strftime('%B')} ({lowest_yearly['yearly']:.2f})")

# 3. General trend
st.markdown("**General Observations:**")
if forecast['yhat'].iloc[-1] > data['y'].mean():
    st.markdown("- Future views are expected to increase compared to historical average.")
else:
    st.markdown("- Future views are expected to decrease compared to historical average.")

# Highlight anomalies
changepoints_fig = add_changepoints_to_plot(fig, model, forecast)
st.subheader("Changepoint Analysis")
st.pyplot(changepoints_fig)
