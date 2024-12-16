import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="YouTube Analytics & Insights", page_icon="📊", layout="wide")

# Custom CSS for Layout
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1000px; /* Set max width for content */
            margin: auto;
            padding: 2rem;
        }
        h1 {
            text-align: center;
            color: #4a90e2;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Centered Title
st.markdown("<h1>📊 DangerTV Audience Insights Dashboard</h1>", unsafe_allow_html=True)

# Helper Functions for Visualizations
def plot_bar(data, x, y, title, palette, figsize=(10, 5), xlabel=None, ylabel=None):
    fig, ax = plt.subplots(figsize=figsize)
    sns.barplot(data=data, x=x, y=y, palette=palette, ax=ax)
    ax.set_title(title, fontsize=14)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    st.pyplot(fig)

def plot_heatmap(data, index, value, title, cmap, figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        data.pivot_table(index=index, values=value, aggfunc="sum"),
        cmap=cmap,
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        cbar_kws={"label": value},
        ax=ax,
    )
    ax.set_title(title, fontsize=14)
    st.pyplot(fig)

# Tab for Navigation
tabs = st.tabs([
    "📊 DangerTV Programming Strategy"
])

# Data Loading Functions
@st.cache_data
def load_csv(url):
    return pd.read_csv(url)

# URLs for datasets
urls = {
    "age": "https://raw.githubusercontent.com/violetzq/MYCOMM599/028782a8bd347b54aa1c748cd8c985e8b1d39645/viewer_age.csv",
    "gender": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_gender.csv",
    "cities": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_Cities.csv",
    "subscriptions": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Subscription_status.csv",
    "content": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv",
    "strategy": "https://raw.githubusercontent.com/violetzq/MYCOMM599/919d85a4502a9906dafce8935dc413e86f8690c3/dates%20data.csv",
}

# DangerTV Programming Strategy
with tabs[0]:
    st.header("📊 DangerTV Programming Strategy Insights")
    
    # Load Strategy Data
    try:
        data = load_csv(urls["strategy"])
    except Exception as e:
        st.error(f"Error loading strategy data: {e}")
        st.stop()

    data["Date"] = pd.to_datetime(data["Date"])
    data["Day of Week"] = data["Date"].dt.day_name()

    # Baselines
    baseline_views = data["Views"].mean()
    baseline_video_views = data["Video views"].mean()
    baseline_watch_time = data["Watch time (hours)"].mean()
    baseline_video_revenue = data["Video estimated revenue (USD)"].mean()
    baseline_estimated_revenue = data["Estimated revenue (USD)"].mean()

    # Day of Week Analysis
    average_metrics_day = data.groupby("Day of Week")[["Views", "Watch time (hours)", "Estimated revenue (USD)"]].mean().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )

    # Charts for Day of Week Analysis
    fig_views = px.bar(
        average_metrics_day,
        x=average_metrics_day.index,
        y="Views",
        title="Average Views by Day of Week",
        labels={"x": "Day of Week", "Views": "Average Views"},
        text_auto=True
    )
    fig_views.add_hline(y=baseline_views, line_dash="dash", line_color="red", 
        annotation_text=f"Daily Views Baseline ({baseline_views:.0f})", annotation_position="bottom right")
    
    fig_watch_time = px.bar(
        average_metrics_day,
        x=average_metrics_day.index,
        y="Watch time (hours)",
        title="Average Watch Time by Day of Week",
        labels={"x": "Day of Week", "Watch time (hours)": "Average Watch Time (hours)"},
        text_auto=True
    )
    fig_watch_time.add_hline(y=baseline_watch_time, line_dash="dash", line_color="red", 
        annotation_text=f"Watch Time Baseline ({baseline_watch_time:.0f} hours)", annotation_position="bottom right")
    
    fig_revenue = px.bar(
        average_metrics_day,
        x=average_metrics_day.index,
        y="Estimated revenue (USD)",
        title="Average Revenue (USD) by Day of Week",
        labels={"x": "Day of Week", "Estimated revenue (USD)": "Average Revenue (USD)"},
        text_auto=True
    )
    fig_revenue.add_hline(y=baseline_estimated_revenue, line_dash="dash", line_color="red", 
        annotation_text=f"Revenue Baseline (${baseline_estimated_revenue:.2f})", annotation_position="bottom right")

    st.plotly_chart(fig_views, use_container_width=True)
    st.plotly_chart(fig_watch_time, use_container_width=True)
    st.plotly_chart(fig_revenue, use_container_width=True)

    # Section 2: Video Analysis with CSV Download
    st.subheader("🎥 Video Performance Insights")
    if "Video title" in data.columns:
        selected_video = st.selectbox("Select a Video Title:", data["Video title"].unique())

        if selected_video:
            selected_video = selected_video.strip()  # Ensure selected title is stripped of whitespace
            video_data = data[data["Video title"] == selected_video]

            if not video_data.empty:
                st.write(f"### Total Views for **{selected_video}**: {video_data['Video views'].iloc[0]:.2f}")
                st.write(f"### Total Watch Time: {video_data['Watch time (hours)'].iloc[0]:.2f} hours")
                st.write(f"### Total Revenue: ${video_data['Video estimated revenue (USD)'].iloc[0]:.2f}")

                # Comparison with baselines
                st.write(f"### Video Views Baseline: {baseline_video_views:.2f}")
                st.write(f"### Watch Time Baseline: {baseline_watch_time:.2f} hours")
                st.write(f"### Revenue Baseline: ${baseline_video_revenue:.2f}")

                # Add interactive chart for selected video
                video_metrics = pd.DataFrame({
                    "Metric": ["Video views", "Watch time (hours)", "Video estimated revenue (USD)"],
                    "Selected Video": [
                        video_data["Video views"].iloc[0],
                        video_data["Watch time (hours)"].iloc[0],
                        video_data["Video estimated revenue (USD)"].iloc[0]
                    ],
                    "Baseline": [baseline_video_views, baseline_watch_time, baseline_video_revenue]
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
            else:
                st.warning("No data available for the selected video. Please try another title.")
    else:
        st.error("Column 'Video title' not found in the dataset.")

    # Section 3: Recommendations Based on Insights
    st.subheader("💡 Recommendations Based on Metrics")
    st.write("- **Highest Performing Days**: Based on average views and revenue, Thursdays and Sundays stand out as the best days to release content.")
    st.write("- **Revenue Insights**: To maximize revenue, focus on boosting engagement on high-performing days.")
    st.write("- **Video-Specific Strategies**: Optimize and promote videos performing below the baselines to increase their overall impact.")
    st.write("- **Watch Time Focus**: Improve viewer retention strategies to boost watch time, as longer engagement correlates with higher revenue.")
