import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Programming Strategy Insights", page_icon="📊", layout="wide")

# Load Dataset
@st.cache_data
def load_content_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/dates%20data.csv"  # Corrected raw link
    try:
        return pd.read_csv(url, encoding="utf-8")  # Use utf-8 encoding
    except UnicodeDecodeError:
        st.warning("UTF-8 encoding failed. Trying 'latin1' encoding.")
        return pd.read_csv(url, encoding="latin1")  # Fallback to latin1 if utf-8 fails

# Load Data
data = load_content_data()

# Data Preparation
if "Date" in data.columns:
    # Ensure 'Date' is a datetime object
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data.dropna(subset=["Date"], inplace=True)  # Drop invalid dates
    data["Day of Week"] = data["Date"].dt.day_name()

    # Calculate baseline metrics for day-of-week analysis
    day_of_week_metrics = data.groupby("Day of Week").agg({
        "Views": "mean",
        "Watch time (hours)": "mean",
        "Average view duration": "first",  # Assuming this remains constant for a day
        "Estimated revenue (USD)": "mean"
    }).reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])  # Ensure correct day order

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
st.subheader("Baseline Metrics by Day of the Week")
if "Day of Week" in data.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=day_of_week_metrics.index, y=day_of_week_metrics["Views"], palette="viridis", ax=ax)
    ax.axhline(data["Views"].mean(), color="red", linestyle="--", label="Overall Baseline (Views)")
    ax.set_title("Average Views by Day of the Week")
    ax.set_ylabel("Average Views")
    ax.set_xlabel("Day of Week")
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

    st.write("**Detailed Metrics by Day of the Week:**")
    st.dataframe(day_of_week_metrics)

# Video-Level Analysis Section
st.subheader("Video Performance Analysis")
if "Video title" in data.columns:
    video_list = data["Video title"].unique().tolist()
    selected_video = st.selectbox("Select a Video Title:", video_list)

    if selected_video:
        video_data = data[data["Video title"] == selected_video]

        # Calculate video-specific baseline metrics
        video_avg_views = video_data["Views"].mean()
        video_avg_revenue = video_data["Estimated revenue (USD)"].mean()
        video_avg_watch_time = video_data["Watch time (hours)"].mean()

        st.write(f"**Average Views for '{selected_video}':** {video_avg_views:.2f}")
        st.write(f"**Average Revenue for '{selected_video}':** ${video_avg_revenue:.2f}")
        st.write(f"**Average Watch Time for '{selected_video}':** {video_avg_watch_time:.2f} hours")

        # Compare to overall baseline
        overall_avg_views = data["Views"].mean()
        overall_avg_revenue = data["Estimated revenue (USD)"].mean()

        if video_avg_views > overall_avg_views:
            st.success(f"'{selected_video}' is performing **above baseline** for views.")
        else:
            st.warning(f"'{selected_video}' is performing **below baseline** for views.")

        if video_avg_revenue > overall_avg_revenue:
            st.success(f"'{selected_video}' is generating **above baseline revenue**.")
        else:
            st.warning(f"'{selected_video}' is generating **below baseline revenue**.")

# Recommendations Section
st.subheader("💡 Recommendations Based on Metrics")
st.write("- **Highest Performing Days:** Focus on publishing content on days with the highest views and revenue.")
st.write("- **Revenue Insights:** Optimize content release schedules to align with peak revenue days.")
st.write("- **Engagement Analysis:** Use watch time and view duration metrics to refine content strategy.")
