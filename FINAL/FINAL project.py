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
st.markdown("<h1>📊 YouTube Analytics & Content Insights</h1>", unsafe_allow_html=True)

# Tabs for Navigation
tabs = st.tabs(["🎥 YouTube Audience Insights", "📈 Content Performance Analysis", "📊 DangerTV Programming Strategy"])

# Data Loading Functions
@st.cache_data
def load_csv(url):
    return pd.read_csv(url)

# URLs for datasets
urls = {
    "age": "https://raw.githubusercontent.com/violetzq/MYCOMM599/0fdc8759eec374661699f73e76828909d7735a46/FINAL/dataset/viewer_age.csv",
    "gender": "https://raw.githubusercontent.com/violetzq/MYCOMM599/0fdc8759eec374661699f73e76828909d7735a46/FINAL/dataset/Viewer_gender.csv",
    "cities": "https://raw.githubusercontent.com/violetzq/MYCOMM599/0fdc8759eec374661699f73e76828909d7735a46/FINAL/dataset/Viewer_Cities.csv",
    "subscriptions": "https://raw.githubusercontent.com/violetzq/MYCOMM599/0fdc8759eec374661699f73e76828909d7735a46/FINAL/dataset/Subscription_status.csv",
    "content": "https://raw.githubusercontent.com/violetzq/MYCOMM599/0fdc8759eec374661699f73e76828909d7735a46/FINAL/dataset/DangerTV_Content.csv",
    "dates": "https://raw.githubusercontent.com/violetzq/MYCOMM599/0fdc8759eec374661699f73e76828909d7735a46/FINAL/dataset/dates%20data.csv",
}

# Load datasets
age_data = load_csv(urls["age"])
gender_data = load_csv(urls["gender"])
cities_data = load_csv(urls["cities"])
subscriptions_data = load_csv(urls["subscriptions"])
content_data = load_csv(urls["content"])
dates_data = load_csv(urls["dates"])

# Preprocessing for dates_data
dates_data["Date"] = pd.to_datetime(dates_data["Date"])
dates_data["Day of Week"] = dates_data["Date"].dt.day_name()

# Helper Functions for Visualizations
def plot_bar(data, x, y, title, palette, figsize=(10, 5), xlabel=None, ylabel=None):
    fig, ax = plt.subplots(figsize=figsize)
    sns.barplot(data=data, x=x, y=y, palette=palette, ax=ax)
    ax.set_title(title, fontsize=14)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    st.pyplot(fig)

def plot_heatmap(data, index, value, title, cmap, figsize=(10, 6)):
    pivot_data = data.pivot_table(index=index, values=value, aggfunc="sum")
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        pivot_data,
        cmap=cmap,
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        cbar_kws={"label": value},
        ax=ax,
    )
    ax.set_title(title, fontsize=14)
    st.pyplot(fig)

# Tab 1: YouTube Audience Insights
with tabs[0]:
    st.header("🎥 YouTube Audience Insights")

    # Age Distribution
    st.subheader("📊 Age Distribution")
    plot_bar(age_data, "Viewer age", "Views (%)", "Age Group Distribution of Views", "viridis")

    # Gender Distribution
    st.subheader("👩‍💼👨‍💼 Gender Distribution")
    gender_data = gender_data[gender_data["Viewer gender"] != "User-specified"]  # Clean gender data
    plot_bar(gender_data, "Viewer gender", "Views (%)", "Gender Distribution of Views", "coolwarm")

    # Subscription Status
    st.subheader("🔔 Subscription Status")
    plot_bar(subscriptions_data, "Subscription status", "Views", "Views by Subscription Status", "Set2")

    # Top Cities by Views
    st.subheader("🌆 Top Cities by Views")
    top_cities = cities_data.sort_values(by="Views", ascending=False).head(10)
    plot_bar(top_cities, "Views", "City name", "Top 10 Cities by Views", "mako", xlabel="Views", ylabel="City")

    # Heatmaps
    st.subheader("🗺️ Heatmap of Views by City")
    plot_heatmap(cities_data.sort_values(by="Views", ascending=False).head(20), "City name", "Views", "Views by City", "Blues")

    st.subheader("⏱️ Heatmap of Watch Time by City")
    plot_heatmap(cities_data.sort_values(by="Watch time (hours)", ascending=False).head(20), "City name", "Watch time (hours)", "Watch Time by City", "Greens")

    # Geographic Location - Search Feature
    st.subheader("🌍 Search by City")
    city_search = st.text_input("Enter a City (e.g., New York, London):").strip()
    if city_search:
        city_results = cities_data[cities_data["City name"].str.contains(city_search, case=False, na=False)]
        if not city_results.empty:
            st.write("**City Search Results:**")
            st.write(city_results.drop(columns=["Cities"], errors="ignore"))
        else:
            st.warning("No results found for the city.")

# Tab 2: Content Performance Analysis
with tabs[1]:
    st.header("📈 Content Performance Analysis")

    # Assign Categories
    categories = {
        "Border Security": ["border", "customs", "security"],
        "Wildlife": ["wildlife", "animal", "nature", "wild", "hunting", "bear"],
        "Adventure": ["adventure", "journey", "explore", "trap", "wilderness", "weather", "severe", "survive", "climbing", "storm", "coast guard"],
        "Crime": ["crime", "criminal", "police", "investigation", "drug", "jail", "sin"],
        "Human Stories & Disaster": ["life", "story", "family", "personal", "survive", "tsunami", "earthquake", "tornado", "dead", "risk", "tribe"],
        "Vehicles": ["car", "truck", "vehicle", "auto", "transport"],
        "Maritime": ["ship", "boat", "ocean", "sea", "fish", "fishing", "sail", "sailor"],
        "Bull Fight": ["bulls", "matadors"],
        "Battle & Special Forces": ["battle", "war", "afghanistan", "training", "special forces", "rescue", "fight", "swat", "k-9"]
    }

    def assign_category(title):
        for category, keywords in categories.items():
            if any(keyword.lower() in str(title).lower() for keyword in keywords):
                return category
        return "Other"

    content_data["Category"] = content_data["Video title"].apply(assign_category)

    # Aggregate Data
    category_summary = content_data.groupby("Category").agg({
        "Views": "sum",
        "Watch time (hours)": "sum",
        "Impressions click-through rate (%)": "mean"
    }).reset_index()

    # Total Views by Category
    st.subheader("📊 Total Views by Category")
    plot_bar(category_summary, "Views", "Category", "Total Views by Category", "viridis", xlabel="Total Views", ylabel="Category")

    # Insights
    st.subheader("💡 Category Insights")
    most_viewed = category_summary.loc[category_summary["Views"].idxmax()]
    highest_ctr = category_summary.loc[category_summary["Impressions click-through rate (%)"].idxmax()]
    st.write(f"- **Most viewed category:** {most_viewed['Category']} with {most_viewed['Views']:.0f} views.")
    st.write(f"- **Highest average CTR:** {highest_ctr['Category']} with {highest_ctr['Impressions click-through rate (%)']:.2f}% CTR.")

    # Top Videos by Category
    st.subheader("🎬 Top Videos by Category")
    selected_category = st.selectbox("Select a Category:", category_summary["Category"].tolist())
    if selected_category:
        top_videos = content_data[content_data["Category"] == selected_category].sort_values(by="Views", ascending=False).head(10)
        st.write(top_videos[["Video title", "Views", "Watch time (hours)", "Impressions click-through rate (%)"]])

    # Search for Videos
    st.subheader("🔍 Search for a Specific Video")
    video_search = st.text_input("Enter a video title or keyword:")
    if video_search:
        search_results = content_data[content_data["Video title"].str.contains(video_search, case=False, na=False)]
        if not search_results.empty:
            st.write("Search Results:")
            st.write(search_results[["Video title", "Category", "Views", "Watch time (hours)", "Impressions click-through rate (%)"]])
        else:
            st.warning("No results found.")

# Tab 3: DangerTV Programming Strategy
with tabs[2]:
    st.header("📊 DangerTV Programming Strategy Insights")

    # Baselines
    baseline_views = dates_data["Views"].mean()
    baseline_video_views = dates_data["Video views"].mean()
    baseline_watch_time = dates_data["Watch time (hours)"].mean()
    baseline_video_revenue = dates_data["Video estimated revenue (USD)"].mean()
    baseline_estimated_revenue = dates_data["Estimated revenue (USD)"].mean()

    # Day of Week Analysis
    average_metrics_day = dates_data.groupby("Day of Week")[["Views", "Watch time (hours)", "Estimated revenue (USD)"]].mean().reindex(
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
        title="Average Watch Time (hours) by Day of Week",
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
    if "Video title" in dates_data.columns:
        selected_video = st.selectbox("Select a Video Title:", dates_data["Video title"].dropna().unique())

        if selected_video:
            video_data = dates_data[dates_data["Video title"] == selected_video]

            if not video_data.empty:
                # Safely access the metrics
                video_total_views = video_data["Video views"].iloc[0]
                video_watch_time = video_data["Watch time (hours)"].iloc[0]
                video_revenue = video_data["Video estimated revenue (USD)"].iloc[0]

                st.write(f"### Total Views for **{selected_video}**: {video_total_views:.2f}")
                st.write(f"### Total Watch Time: {video_watch_time:.2f} hours")
                st.write(f"### Total Revenue: ${video_revenue:.2f}")

                # Comparison with baselines
                st.write(f"### Video Views Baseline: {baseline_video_views:.2f}")
                st.write(f"### Watch Time Baseline: {baseline_watch_time:.2f} hours")
                st.write(f"### Revenue Baseline: ${baseline_video_revenue:.2f}")

                # Add interactive chart for selected video
                video_metrics = pd.DataFrame({
                    "Metric": ["Video views", "Watch time (hours)", "Video estimated revenue (USD)"],
                    "Selected Video": [video_total_views, video_watch_time, video_revenue],
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
