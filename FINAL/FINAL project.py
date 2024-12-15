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
            max-width: 1000px;
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

# Data Loading Function
@st.cache_data
def load_csv(url):
    return pd.read_csv(url)

# URLs for Datasets
urls = {
    "age": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/FINAL/dataset/viewer_age.csv",
    "gender": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/FINAL/dataset/Viewer_gender.csv",
    "cities": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/FINAL/dataset/Viewer_Cities.csv",
    "subscriptions": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/FINAL/dataset/Subscription_status.csv",
    "content": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/FINAL/dataset/DangerTV_Content.csv",
    "dates": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/FINAL/dataset/dates%20data.csv",
}

# Load Datasets
age_data = load_csv(urls["age"])
gender_data = load_csv(urls["gender"])
cities_data = load_csv(urls["cities"])
subscriptions_data = load_csv(urls["subscriptions"])
content_data = load_csv(urls["content"])
dates_data = load_csv(urls["dates"])

# Preprocessing for dates_data
dates_data["Date"] = pd.to_datetime(dates_data["Date"])
dates_data["Day of Week"] = dates_data["Date"].dt.day_name()

# Helper Functions
def plot_bar(data, x, y, title, palette, xlabel=None, ylabel=None):
    """Generates a bar plot using Seaborn."""
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=data, x=x, y=y, palette=palette, ax=ax)
    ax.set_title(title, fontsize=14)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    st.pyplot(fig)

def plot_heatmap(data, index, value, title, cmap):
    """Generates a heatmap."""
    pivot_data = data.pivot_table(index=index, values=value, aggfunc="sum")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot_data, cmap=cmap, annot=True, fmt=".0f", linewidths=0.5, cbar_kws={"label": value}, ax=ax)
    ax.set_title(title, fontsize=14)
    st.pyplot(fig)

# Tab 1: YouTube Audience Insights
with tabs[0]:
    st.header("🎥 YouTube Audience Insights")

    st.subheader("📊 Age Distribution")
    plot_bar(age_data, "Viewer age", "Views (%)", "Age Group Distribution of Views", "viridis")

    st.subheader("👩‍💼👨‍💼 Gender Distribution")
    gender_data = gender_data[gender_data["Viewer gender"] != "User-specified"]
    plot_bar(gender_data, "Viewer gender", "Views (%)", "Gender Distribution of Views", "coolwarm")

    st.subheader("🔔 Subscription Status")
    plot_bar(subscriptions_data, "Subscription status", "Views", "Views by Subscription Status", "Set2")

    st.subheader("🌆 Top Cities by Views")
    top_cities = cities_data.sort_values(by="Views", ascending=False).head(10)
    plot_bar(top_cities, "Views", "City name", "Top 10 Cities by Views", "mako", xlabel="Views", ylabel="City")

    st.subheader("🌍 Search by City")
    city_search = st.text_input("Enter a City (e.g., New York, London):").strip()
    if city_search:
        city_results = cities_data[cities_data["City name"].str.contains(city_search, case=False, na=False)]
        if not city_results.empty:
            st.write("**City Search Results:**")
            st.write(city_results)
        else:
            st.warning("No results found for the city.")

# Tab 2: Content Performance Analysis
with tabs[1]:
    st.header("📈 Content Performance Analysis")

    categories = {
        "Border Security": ["border", "customs", "security"],
        "Wildlife": ["wildlife", "animal", "nature", "wild"],
        "Adventure": ["adventure", "explore", "journey"],
    }

    def assign_category(title):
        for category, keywords in categories.items():
            if any(keyword.lower() in title.lower() for keyword in keywords):
                return category
        return "Other"

    content_data["Category"] = content_data["Video title"].apply(assign_category)

    st.subheader("📊 Total Views by Category")
    category_summary = content_data.groupby("Category").agg({"Views": "sum", "Watch time (hours)": "sum"}).reset_index()
    plot_bar(category_summary, "Category", "Views", "Total Views by Category", "viridis", ylabel="Views")

    st.subheader("🔍 Search for a Specific Video")
    video_search = st.text_input("Enter a video title or keyword:")
    if video_search:
        search_results = content_data[content_data["Video title"].str.contains(video_search, case=False, na=False)]
        if not search_results.empty:
            st.write("Search Results:")
            st.write(search_results[["Video title", "Category", "Views", "Watch time (hours)"]])
        else:
            st.warning("No results found.")

# Tab 3: DangerTV Programming Strategy
with tabs[2]:
    st.header("📊 DangerTV Programming Strategy Insights")

    baseline_views = dates_data["Views"].mean()
    baseline_watch_time = dates_data["Watch time (hours)"].mean()
    baseline_estimated_revenue = dates_data["Estimated revenue (USD)"].mean()

    average_metrics_day = dates_data.groupby("Day of Week")[["Views", "Watch time (hours)", "Estimated revenue (USD)"]].mean()

    st.subheader("📅 Average Metrics by Day of Week")
    fig_views = px.bar(average_metrics_day, x=average_metrics_day.index, y="Views",
                       title="Average Views by Day of Week", text_auto=True)
    st.plotly_chart(fig_views, use_container_width=True)

    st.subheader("🔍 Search for Video Insights")
    if "Video title" in dates_data.columns:
        selected_video = st.selectbox("Select a Video Title:", dates_data["Video title"].dropna().unique())
        if selected_video:
            video_data = dates_data[dates_data["Video title"] == selected_video]
            if not video_data.empty:
                st.write(f"### Video Data for **{selected_video}**")
                st.write(video_data)
                st.download_button(
                    label="Download Video Data as CSV",
                    data=video_data.to_csv(index=False),
                    file_name=f"{selected_video}_performance.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data available for the selected video.")
    else:
        st.error("Column 'Video title' not found in the dataset.")
