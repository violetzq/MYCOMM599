import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="DangerTV Programming Strategy", page_icon="📊", layout="wide")

# Load Dataset
@st.cache_data
def load_content_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/dates%20data.csv"
    return pd.read_csv(url)

# Load Data
data = load_content_data()

# Data Preparation
data["Date"] = pd.to_datetime(data["Date"])  # Ensure 'Date' is in datetime format
data["Day of Week"] = data["Date"].dt.day_name()  # Extract day of the week

# Calculate Baselines
baseline_views = data["Views"].mean()  # Baseline for daily views
baseline_video_views = data["Video views"].mean()  # Baseline for video views

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
st.subheader("📅 Baseline Viewership Performance by Day of Week")
average_views_day = data.groupby("Day of Week")["Views"].mean().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=average_views_day.index, y=average_views_day.values, palette="viridis", ax=ax)
ax.axhline(baseline_views, color="red", linestyle="--", label="Daily Views Baseline")
ax.legend()
ax.set_title("Average Views by Day of Week", fontsize=12)
ax.set_ylabel("Average Views")
ax.set_xlabel("Day of Week")
plt.xticks(rotation=45)
st.pyplot(fig)

# Section 2: Video Analysis
st.subheader("🎥 Video Performance Insights")
selected_video = st.selectbox("Select a Video Title:", data["Video title"].unique())

if selected_video:
    video_data = data[data["Video title"] == selected_video]
    video_total_views = video_data["Video views"].iloc[0]  # Get total views for the video
    
    st.write(f"### Total Views for **{selected_video}**: {video_total_views:.2f}")
    st.write(f"### Video Views Baseline: {baseline_video_views:.2f}")
    
    if video_total_views > baseline_video_views:
        st.success(f"The video **{selected_video}** is performing **above average**, exceeding the baseline by {video_total_views - baseline_video_views:.2f} views.")
        st.write("✅ **Recommendation**: Continue promoting this video as it is performing well!")
    else:
        st.warning(f"The video **{selected_video}** is performing **below average**, falling short of the baseline by {baseline_video_views - video_total_views:.2f} views.")
        st.write("⚠️ **Recommendation**: Explore optimization opportunities for this video, such as improving its title or thumbnail.")

# Section 3: Recommendations Based on Insights
st.subheader("💡 Recommendations Based on Metrics")
st.write("- **Highest Performing Days**: Based on average views, Thursdays and Sundays stand out as the best days to release content.")
st.write("- **Revenue Insights**: To maximize revenue, focus on boosting engagement on Thursdays and Sundays.")
st.write("- **Video-Specific Strategies**: Tailor promotional strategies for videos performing below the baseline.")
