import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Programming Strategy Insights", page_icon="📊", layout="wide")

# Load Dataset
@st.cache_data
def load_daily_data():
    url = "https://github.com/violetzq/MYCOMM599/blob/a17ead2e63166deb9b16b041ca49876fad3b36b0/dates%20data.csv?raw=true"
    return pd.read_csv(url, parse_dates=["Date"])

# Load Data
data = load_daily_data()

# Data Preparation
data["Day of Week"] = data["Date"].dt.day_name()  # Extract day of the week
average_metrics_day = (
    data.groupby("Day of Week")[["Views", "Watch time (hours)", "Estimated revenue (USD)"]]
    .mean()
    .reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
)

# Add Baselines
overall_baseline_views = data["Views"].mean()
overall_baseline_revenue = data["Estimated revenue (USD)"].mean()

# Custom CSS for Centered and Fixed Width Content
st.markdown("""
    <style>
    .block-container {
        max-width: 900px;  /* Restrict content width */
        margin: auto;      /* Center content */
        padding: 2rem;     /* Add padding around content */
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Programming Strategy Insights")

# Baseline Analysis Section
st.subheader("Baseline Metrics by Day of Week")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=average_metrics_day.index, y=average_metrics_day["Views"], palette="viridis", ax=ax)
ax.axhline(overall_baseline_views, color="red", linestyle="--", label="Overall Baseline (Views)")
ax.legend()
ax.set_title("Average Views by Day of Week", fontsize=14)
ax.set_ylabel("Average Views")
ax.set_xlabel("Day of Week")
plt.xticks(rotation=45)
st.pyplot(fig)

# Revenue Insights Section
st.subheader("Revenue Insights by Day of Week")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=average_metrics_day.index, y=average_metrics_day["Estimated revenue (USD)"], palette="coolwarm", ax=ax)
ax.axhline(overall_baseline_revenue, color="red", linestyle="--", label="Overall Baseline (Revenue)")
ax.legend()
ax.set_title("Average Revenue by Day of Week", fontsize=14)
ax.set_ylabel("Average Revenue (USD)")
ax.set_xlabel("Day of Week")
plt.xticks(rotation=45)
st.pyplot(fig)

# Recommendations Section
st.subheader("💡 Recommendations Based on Metrics")
st.write(f"- **Highest Performing Days:** Based on average views, Thursdays and Sundays stand out as the best days to release content.")
st.write(f"- **Revenue Insights:** To maximize revenue, focus on boosting engagement on {average_metrics_day['Estimated revenue (USD)'].idxmax()}.")

# Summary Table
st.subheader("Summary of Metrics by Day of Week")
st.dataframe(average_metrics_day.reset_index())
