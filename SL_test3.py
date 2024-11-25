import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Title and Description
st.title("YouTube Programming Strategy Dashboard")
st.markdown("Analyze your YouTube performance data and get actionable programming insights.")

# Load Dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv"
    return pd.read_csv(url)

try:
    data = load_data()
    # Ensure required columns are present
    if "Video publish time" not in data.columns or "Views" not in data.columns:
        st.error("Required columns are missing from the dataset.")
        st.stop()
    # Preprocess data
    data["Video publish time"] = pd.to_datetime(data["Video publish time"], errors="coerce")
    data["day_of_week"] = data["Video publish time"].dt.day_name()
    data["hour_of_day"] = data["Video publish time"].dt.hour
except Exception as e:
    st.error(f"Error loading or processing data: {e}")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")
selected_day = st.sidebar.multiselect(
    "Select Day(s) of the Week", options=data["day_of_week"].unique(), default=data["day_of_week"].unique()
)
selected_hours = st.sidebar.slider("Select Hour Range", 0, 23, (0, 23))

# Filter Data
filtered_data = data[
    (data["day_of_week"].isin(selected_day)) & (data["hour_of_day"].between(selected_hours[0], selected_hours[1]))
]

# 1. Analyze Peak Viewing Times
st.subheader("1. Analyze Peak Viewing Times")
st.markdown("Identify trends in when viewers engage most actively with the content.")

# Heatmap of Views by Day and Hour
views_heatmap = data.pivot_table(
    index="day_of_week", columns="hour_of_day", values="Views", aggfunc="mean"
).reindex(index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

st.write("**Average Views Heatmap**")
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(views_heatmap, cmap="coolwarm", annot=True, fmt=".0f", ax=ax)
st.pyplot(fig)

# Insights
st.write("**Insights:**")
st.write(
    "- Peak viewing hours can be identified from the heatmap. Consider posting during hours with higher engagement."
    "\n- Adjust scheduling to avoid low-engagement periods."
)

# 2. Content Length Analysis
st.subheader("2. Content Length Analysis")
if "Average view duration" in data.columns:
    st.markdown("Evaluate viewer retention to determine the ideal video length for engagement.")
    content_length_analysis = data.groupby("Video publish time")["Average view duration"].mean()
    st.line_chart(content_length_analysis)

    st.write("**Insights:**")
    st.write("- Identify whether shorter or longer videos retain viewers better.")
    st.write("- Suggest adjustments to content length based on average view duration trends.")

# 3. CTR and Thumbnail Optimization
st.subheader("3. CTR and Thumbnail Optimization")
if "Impressions click-through rate (%)" in data.columns:
    st.markdown("Analyze videos with high CTR to evaluate their titles, thumbnails, and descriptions.")
    top_ctr_videos = data.sort_values("Impressions click-through rate (%)", ascending=False).head(10)
    st.write("**Top 10 Videos with Highest CTR**")
    st.write(top_ctr_videos[["Video title", "Impressions click-through rate (%)", "Views"]])

    st.write("**Insights:**")
    st.write("- Analyze the thumbnails, titles, and descriptions of these videos to identify what works best.")
    st.write("- Use these findings to optimize future content.")

# 4. Optimal Scheduling Recommendations
st.subheader("4. Optimal Scheduling Recommendations")
optimal_schedule = views_heatmap.stack().reset_index()
optimal_schedule.columns = ["Day", "Hour", "Average Views"]
optimal_schedule = optimal_schedule.sort_values(by="Average Views", ascending=False).head(5)
st.write("**Recommended Posting Times**")
st.write(optimal_schedule)

st.write("**Insights:**")
st.write("- Use the table to decide the best times for posting new videos.")

# 5. Viewer Engagement Trends
st.subheader("5. Viewer Engagement Trends")
if "Watch time (hours)" in data.columns:
    engagement_trends = data.groupby("day_of_week")["Watch time (hours)"].sum().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    st.bar_chart(engagement_trends)

    st.write("**Insights:**")
    st.write("- Identify days with the highest watch time and focus on publishing content on those days.")

# 6. Cross-Promotion Opportunities
st.subheader("6. Cross-Promotion Opportunities")
if "Content" in data.columns:
    content_performance = data.groupby("Content")["Views"].sum().sort_values(ascending=False)
    st.bar_chart(content_performance)

    st.write("**Insights:**")
    st.write("- Identify series or playlists with high engagement for cross-promotion.")
    st.write("- Use this data to prioritize high-performing categories.")

# Experimentation Plan
st.subheader("Experimentation Plan")
st.write(
    "Suggestions for testing new scheduling patterns, video formats, or cross-category content:"
    "\n1. Experiment with posting videos at different peak hours."
    "\n2. Test the impact of various thumbnail designs on CTR."
    "\n3. Introduce new content categories and measure engagement."
)
