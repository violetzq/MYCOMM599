import streamlit as st
import pandas as pd
import plotly.express as px

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

# Calculate Baselines
baseline_views = data["Views"].mean()
baseline_video_views = data["Video views"].mean()
baseline_watch_time = data["Watch time (hours)"].mean()
baseline_revenue = data["Estimated revenue (USD)"].mean()

st.title("📊 DangerTV Programming Strategy Insights")

# Section 1: Interactive Day of Week Analysis
st.subheader("📅 Baseline Performance by Day of Week")

average_metrics_day = data.groupby("Day of Week")[["Views", "Watch time (hours)", "Estimated revenue (USD)"]].mean().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

# Interactive charts using Plotly
fig_views = px.bar(
    average_metrics_day,
    x=average_metrics_day.index,
    y="Views",
    title="Average Views by Day of Week",
    labels={"x": "Day of Week", "Views": "Average Views"},
    text_auto=True
)
fig_views.add_hline(y=baseline_views, line_dash="dash", line_color="red", annotation_text="Daily Views Baseline")

fig_watch_time = px.bar(
    average_metrics_day,
    x=average_metrics_day.index,
    y="Watch time (hours)",
    title="Average Watch Time (hours) by Day of Week",
    labels={"x": "Day of Week", "Watch time (hours)": "Average Watch Time (hours)"},
    text_auto=True
)
fig_watch_time.add_hline(y=baseline_watch_time, line_dash="dash", line_color="red", annotation_text="Watch Time Baseline")

fig_revenue = px.bar(
    average_metrics_day,
    x=average_metrics_day.index,
    y="Estimated revenue (USD)",
    title="Average Revenue (USD) by Day of Week",
    labels={"x": "Day of Week", "Estimated revenue (USD)": "Average Revenue (USD)"},
    text_auto=True
)
fig_revenue.add_hline(y=baseline_revenue, line_dash="dash", line_color="red", annotation_text="Revenue Baseline")

# Display interactive plots
st.plotly_chart(fig_views, use_container_width=True)
st.plotly_chart(fig_watch_time, use_container_width=True)
st.plotly_chart(fig_revenue, use_container_width=True)

# Section 2: Video Analysis with CSV Download
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
    
    # Add interactive chart for selected video
    video_metrics = pd.DataFrame({
        "Metric": ["Video views", "Watch time (hours)", "Estimated revenue (USD)"],
        "Selected Video": [video_total_views, video_watch_time, video_revenue],
        "Baseline": [baseline_video_views, baseline_watch_time, baseline_revenue]
    })

    fig_video = px.bar(
        video_metrics,
        x="Metric",
        y=["Selected Video", "Baseline"],
        barmode="group",
        title=f"Performance Metrics for '{selected_video}' vs. Baseline",
        text_auto=True
    )
    st.plotly_chart(fig_video, use_container_width=True)

    # Download button for CSV
    st.download_button(
        label="Download Selected Video Data as CSV",
        data=video_data.to_csv(index=False),
        file_name=f"{selected_video}_data.csv",
        mime="text/csv"
    )

# Section 3: Recommendations Based on Insights
st.subheader("💡 Recommendations Based on Metrics")
st.write("- **Highest Performing Days**: Based on average views and revenue, Thursdays and Sundays stand out as the best days to release content.")
st.write("- **Revenue Insights**: To maximize revenue, focus on boosting engagement on high-performing days.")
st.write("- **Video-Specific Strategies**: Optimize and promote videos performing below the baselines to increase their overall impact.")
st.write("- **Watch Time Focus**: Improve viewer retention strategies to boost watch time, as longer engagement correlates with higher revenue.")
