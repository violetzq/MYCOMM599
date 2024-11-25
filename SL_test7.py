import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt

# Set Streamlit page configuration
st.set_page_config(page_title="Audience Engagement Predictor", layout="wide")

# Load your dataset
st.title("Audience Engagement Predictor")
data_url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv"
data = pd.read_csv(data_url, encoding='ISO-8859-1')

# Preprocess the data
st.header("Data Preprocessing")
if 'Video publish time' in data.columns:
    data.rename(columns={'Video publish time': 'ds', 'Views': 'y'}, inplace=True)
    data['ds'] = pd.to_datetime(data['ds'], errors='coerce')
    data = data.dropna(subset=['ds', 'y'])  # Remove rows with NaN in 'ds' or 'y'
    st.write(f"Data after cleaning: {data.shape[0]} rows")
else:
    st.error("The required columns 'Video publish time' and 'Views' are missing in the dataset!")

# Display historical data
st.subheader("Historical Data")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(data['ds'], data['y'], label='Historical Views')
ax.set_title("Historical Views Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Views")
ax.legend()
st.pyplot(fig)

# Prophet model
st.subheader("Forecast Audience Engagement")
with st.sidebar:
    st.header("Forecast Configuration")
    prediction_period = st.slider("Select prediction period (days):", min_value=30, max_value=365, value=90, step=30)

model = Prophet(yearly_seasonality=True, daily_seasonality=False)
model.fit(data[['ds', 'y']])

# Create future dataframe
future = model.make_future_dataframe(periods=prediction_period)
forecast = model.predict(future)

# Plot forecast
st.subheader("Forecasted Views Over Time")
fig_forecast = plot_plotly(model, forecast)
st.plotly_chart(fig_forecast, use_container_width=True)

# Insights
st.subheader("Key Insights")
max_predicted_views = forecast['yhat'].max()
max_predicted_date = forecast.loc[forecast['yhat'].idxmax(), 'ds']
min_predicted_views = max(0, forecast['yhat'].min())  # Clamp negative values to zero
min_predicted_date = forecast.loc[forecast['yhat'].idxmin(), 'ds']

st.markdown(f"- **Maximum predicted views:** {max_predicted_views:.0f} on {max_predicted_date.date()}")
st.markdown(f"- **Minimum predicted views:** {min_predicted_views:.0f} on {min_predicted_date.date()}")
