import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="DangerTV Programming Strategy", page_icon="📊", layout="wide")

# Load Dataset
@st.cache_data
def load_content_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/a85abe1474fb7fe6665e8a37f3db333e897f66d2/dates_data.csv"
    return pd.read_csv(url)

# Load Data
data = load_content_data()

# Data Preparation
data["Date"] = pd.to_datetime(data["Date"])  # Ensure 'Date' is in datetime format
data["Day of Week"] = data["Date"].dt.day_name()  # Extract day of the week

# Filter for numeric columns for grouping
numeric_columns = ["Views", "Watch time (hours)", "Estimated revenue (USD)"]
average_metrics_day = data.groupby("Day of Week")[numeric_columns].mean().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

# Calculate Baselines
baseline_views = data["Views"].mean()
baseline_video_views = data["Video views"].mean()
baseline_watch_time = data["Watch time (hours)"].mean()
baseline_revenue = data["Estimated revenue (USD)"].mean()

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

st.title("📊 DangerTV Programming Strategy Insights")

# Section 1: Day of Week Analysis
st.subheader("📅 Baseline Performance by Day of Week")

fig, ax = plt.subplots(3, 1, figsize=(8, 12), sharex=True)

# Views
sns.barplot(x=average_metrics_day.index, y=average_metrics_day["Views"], palette="viridis", ax=ax[0])
ax[0].axhline(baseline_views, color="red", linestyle="--", label="Daily Views Baseline")
ax[0].legend()
ax[0].set_title("Average Views by Day of Week", fontsize=12)
ax[0].set_ylabel("Views")

# Watch time
sns.barplot(x=average_metrics_day.index, y=average_metrics_day["Watch time (hours)"], palette="Blues", ax=ax[1])
ax[1].axhline(baseline_watch_time, color="red", linestyle="--", label="Watch Time Baseline")
ax[1].legend()
ax[1].set_title("Average Watch Time (hours) by Day of Week", fontsize=12)
ax[1].set_ylabel("Watch Time (hours)")

# Revenue
sns.barplot(x=average_metrics_day.index, y=average_metrics_day["Estimated revenue (USD)"], palette="Oranges", ax=ax[2])
ax[2].axhline(baseline_revenue, color="red", linestyle="--", label="Revenue Baseline")
ax[2].legend()
ax[2].set_title("Average Revenue (USD) by Day of Week", fontsize=12)
ax[2].set_ylabel("Estimated Revenue (USD)")

plt.xticks(rotation=45)
st.pyplot(fig)

# Section 2: Video Analysis
st.subheader("🎥 Video Performance Insights")
selected_video = st.selectbox("Select a Video Title:", data["Video title"].unique())

if selected_video:
    video_data = data[data["Video title"] == selected_video]
    video_total_views = video_data["Video views"].iloc[0]
    video_watch_time = video_data["Watch time (hours)"].iloc[0]
    video_revenue = video_data["Estimated revenue (USD)"].iloc[0]
    
    st.write(f"### Total Views for **{selected_video}**: {video_total_views:.2f}")
    st.write(f"### Total Watch Time: {video_watch_time:.2f} hours")
    st.write(f"### Total Revenue: ${video_revenue:.2f}")
    
    # Comparison with baselines
    st.write(f"### Video Views Baseline: {baseline_video_views:.2f}")
    st.write(f"### Watch Time Baseline: {baseline_watch_time:.2f} hours")
    st.write(f"### Revenue Baseline: ${baseline_revenue:.2f}")
    
    if video_total_views > baseline_video_views:
        st.success(f"The video **{selected_video}** is performing **above average in views**, exceeding the baseline by {video_total_views - baseline_video_views:.2f} views.")
    else:
        st.warning(f"The video **{selected_video}** is performing **below average in views**, falling short of the baseline by {baseline_video_views - video_total_views:.2f} views.")
    
    if video_watch_time > baseline_watch_time:
        st.success(f"The video has **above average watch time**, exceeding the baseline by {video_watch_time - baseline_watch_time:.2f} hours.")
    else:
        st.warning(f"The video has **below average watch time**, falling short of the baseline by {baseline_watch_time - video_watch_time:.2f} hours.")
    
    if video_revenue > baseline_revenue:
        st.success(f"The video has **above average revenue**, exceeding the baseline by ${video_revenue - baseline_revenue:.2f}.")
    else:
        st.warning(f"The video has **below average revenue**, falling short of the baseline by ${baseline_revenue - video_revenue:.2f}.")

# Section 3: Recommendations Based on Insights
st.subheader("💡 Recommendations Based on Metrics")
st.write("- **Highest Performing Days**: Based on average views and revenue, Thursdays and Sundays stand out as the best days to release content.")
st.write("- **Revenue Insights**: To maximize revenue, focus on boosting engagement on high-performing days.")
st.write("- **Video-Specific Strategies**: Optimize and promote videos performing below the baselines to increase their overall impact.")
st.write("- **Watch Time Focus**: Improve viewer retention strategies to boost watch time, as longer engagement correlates with higher revenue.")
