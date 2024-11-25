import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import matplotlib.pyplot as plt

# Load Dataset
data_url = 'https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv'
data = pd.read_csv(data_url, encoding='ISO-8859-1')

# Prepare Data for Prophet
# Ensure date column is in datetime format and rename for Prophet compatibility
data['Video publish time'] = pd.to_datetime(data['Video publish time'], errors='coerce')
data = data.rename(columns={'Video publish time': 'ds', 'Views': 'y'})
data = data[['ds', 'y']].dropna()  # Keep only required columns and drop missing values

# Streamlit App Setup
st.title("Audience Engagement Predictor")
st.markdown("Use historical data to predict future audience engagement metrics.")

# User Input for Prediction Periods
st.sidebar.header("Forecast Settings")
prediction_periods = st.sidebar.selectbox(
    "Select number of days to forecast:",
    options=[30, 90, 180, 365],
    index=0
)
st.sidebar.markdown(f"Forecasting {prediction_periods} days into the future.")

# Train Prophet Model
model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
model.fit(data)

# Create Future Dataframe
future = model.make_future_dataframe(periods=prediction_periods)
forecast = model.predict(future)

# Clamp Predictions to Avoid Negative Values
forecast['yhat'] = forecast['yhat'].clip(lower=0)
forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0)
forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=0)

# Visualize Predictions
st.subheader("Forecasted Views Over Time")
fig1 = plot_plotly(model, forecast)
st.plotly_chart(fig1, use_container_width=True)

# Key Insights
st.subheader("Key Insights")
highest_prediction = forecast[['ds', 'yhat']].sort_values(by='yhat', ascending=False).iloc[0]
lowest_prediction = forecast[['ds', 'yhat']].sort_values(by='yhat', ascending=True).iloc[0]

st.markdown(f"- The **highest predicted Views** is **{highest_prediction['yhat']:.2f}**, expected on **{highest_prediction['ds'].strftime('%Y-%m-%d')}**.")
st.markdown(f"- The **lowest predicted Views** is **{lowest_prediction['yhat']:.2f}**, expected on **{lowest_prediction['ds'].strftime('%Y-%m-%d')}**.")
if lowest_prediction['yhat'] == 0:
    st.markdown("- Investigate historical patterns leading to predicted zero engagement.")

# Allow User to Explore Forecasted Data
st.subheader("Explore Forecasted Data")
forecast_table = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
st.dataframe(forecast_table)

# Option to Download Forecast Data as CSV
csv = forecast_table.to_csv(index=False)
st.download_button(label="Download Forecast Data as CSV", data=csv, file_name="forecast_data.csv", mime="text/csv")

# Historical Data Visualization
st.subheader("Historical Data")
fig2, ax = plt.subplots()
data.plot(x='ds', y='y', kind='line', title='Historical Views Over Time', ax=ax)
st.pyplot(fig2)
