import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
tabs = st.tabs(["🎥 YouTube Audience Insights", "📈 Content Performance Analysis"])

# Data Loading Functions
@st.cache_data
def load_csv(url):
    return pd.read_csv(url)

# URLs for datasets
urls = {
    "age": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_age.csv",
    "gender": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_gender.csv",
    "cities": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_Cities.csv",
    "subscriptions": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Subscription_status.csv",
    "content": "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv",
}

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

# Tab 1: YouTube Audience Insights
with tabs[0]:
    st.header("🎥 YouTube Audience Insights")

    # Load Audience Data
    try:
        age_data = load_csv(urls["age"])
        gender_data = load_csv(urls["gender"])
        cities_data = load_csv(urls["cities"])
        subscription_data = load_csv(urls["subscriptions"])
        gender_data = gender_data[gender_data["Viewer gender"] != "User-specified"]  # Clean gender data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    # Age Distribution
    st.subheader("📊 Age Distribution")
    plot_bar(age_data, "Viewer age", "Views (%)", "Age Group Distribution of Views", "viridis")

    # Gender Distribution
    st.subheader("👩‍💼👨‍💼 Gender Distribution")
    plot_bar(gender_data, "Viewer gender", "Views (%)", "Gender Distribution of Views", "coolwarm")

    # Subscription Status
    st.subheader("🔔 Subscription Status")
    plot_bar(subscription_data, "Subscription status", "Views", "Views by Subscription Status", "Set2")

    # Top Cities by Views
    st.subheader("🌆 Top Cities by Views")
    top_cities = cities_data.sort_values(by="Views", ascending=False).head(10)
    plot_bar(top_cities, "Views", "City name", "Top 10 Cities by Views", "mako", xlabel="Views", ylabel="City")

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

    # Heatmaps
    st.subheader("🗺️ Heatmap of Views by City")
    plot_heatmap(cities_data.sort_values(by="Views", ascending=False).head(20), "City name", "Views", "Views by City", "Blues")

    st.subheader("⏱️ Heatmap of Watch Time by City")
    plot_heatmap(cities_data.sort_values(by="Watch time (hours)", ascending=False).head(20), "City name", "Watch time (hours)", "Watch Time by City", "Greens")

# Tab 2: Content Performance Analysis
with tabs[1]:
    st.header("📈 Content Performance Analysis")

    # Load Content Data
    try:
        content_data = load_csv(urls["content"])
    except Exception as e:
        st.error(f"Error loading content data: {e}")
        st.stop()

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
