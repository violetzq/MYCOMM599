import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="YouTube Analytics & Insights", page_icon="📊", layout="wide")

# Title with Emoji
st.title("📊 YouTube Analytics & Content Insights")

# Tabs with Icons
tabs = st.tabs(
    [
        "🎥 YouTube Audience Insights",
        "📈 Content Performance Analysis"
    ]
)

# Tab 1: YouTube Audience Insights
with tabs[0]:
    st.header("🎥 YouTube Audience Insights")

    # Load Dataset Functions
    @st.cache_data
    def load_age_data():
        url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_age.csv"
        return pd.read_csv(url)

    @st.cache_data
    def load_gender_data():
        url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_gender.csv"
        data = pd.read_csv(url)
        return data[data["Viewer gender"] != "User-specified"]

    @st.cache_data
    def load_cities_data():
        url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_Cities.csv"
        return pd.read_csv(url)

    @st.cache_data
    def load_subscription_data():
        url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Subscription_status.csv"
        return pd.read_csv(url)

    # Load Data
    try:
        age_data = load_age_data()
        gender_data = load_gender_data()
        cities_data = load_cities_data()
        subscription_data = load_subscription_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    # Age Distribution
    st.subheader("📊 Age Distribution")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=age_data, x="Viewer age", y="Views (%)", palette="viridis", ax=ax1)
    ax1.set_title("Age Group Distribution of Views", fontsize=16)
    st.pyplot(fig1)

    # Gender Distribution
    st.subheader("👩‍💼👨‍💼 Gender Distribution")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=gender_data, x="Viewer gender", y="Views (%)", palette="coolwarm", ax=ax2)
    ax2.set_title("Gender Distribution of Views", fontsize=16)
    st.pyplot(fig2)

    # Geographic Location
    st.subheader("🌍 Geographic Location")

    # Search Feature for City Data
    st.markdown("### 🔎 Search by City")
    city_search_term = st.text_input("Enter a City (e.g., New York, London):").strip()
    if city_search_term:
        filtered_city_data = cities_data[cities_data["City name"].str.contains(city_search_term, case=False, na=False)]
        if not filtered_city_data.empty:
            filtered_city_data = filtered_city_data.drop(columns=["Cities"], errors="ignore")
            st.write("**City Search Results:**")
            st.write(filtered_city_data)
        else:
            st.warning("No results found for the city. Try another search.")

    # Bar Chart for Top Cities by Views
    st.markdown("### 🌆 Top Cities by Views")
    top_cities = cities_data.sort_values(by="Views", ascending=False).head(10)
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_cities, x="Views", y="City name", palette="mako", ax=ax3)
    ax3.set_title("Top 10 Cities by Views", fontsize=16)
    st.pyplot(fig3)

    # Heatmaps
    st.markdown("### 🗺️ City Heatmap - Views")
    top_cities_views = cities_data.sort_values(by="Views", ascending=False).head(20)
    fig1, ax1 = plt.subplots(figsize=(10, 10))
    sns.heatmap(
        top_cities_views.pivot_table(index="City name", values="Views", aggfunc="sum"),
        cmap="Blues",
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        cbar_kws={"label": "Views"},
        ax=ax1,
    )
    ax1.set_title("Heatmap of Views by City", fontsize=16)
    st.pyplot(fig1)

    st.markdown("### ⏱️ City Heatmap - Watch Time")
    top_cities_watch_time = cities_data.sort_values(by="Watch time (hours)", ascending=False).head(20)
    fig2, ax2 = plt.subplots(figsize=(10, 10))
    sns.heatmap(
        top_cities_watch_time.pivot_table(index="City name", values="Watch time (hours)", aggfunc="sum"),
        cmap="Greens",
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        cbar_kws={"label": "Watch Time (hours)"},
        ax=ax2,
    )
    ax2.set_title("Heatmap of Watch Time by City", fontsize=16)
    st.pyplot(fig2)

    # Subscription Data
    st.subheader("🔔 Subscription Status")
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=subscription_data, x="Subscription status", y="Views", palette="Set2", ax=ax6)
    ax6.set_title("Views by Subscription Status", fontsize=16)
    st.pyplot(fig6)

# Tab 2: Content Performance Analysis
with tabs[1]:
    st.header("📈 Content Performance Analysis")

    # Load Dataset
    @st.cache_data
    def load_content_data():
        url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv"
        return pd.read_csv(url, encoding='ISO-8859-1')

    data = load_content_data()

    # Define categories
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

    data['Category'] = data['Video title'].apply(assign_category)

    # Aggregate data by category
    category_summary = data.groupby('Category').agg({
        'Views': 'sum',
        'Watch time (hours)': 'sum',
        'Impressions click-through rate (%)': 'mean'
    }).reset_index()

    # Bar chart for total views by category
    st.subheader("📊 Total Views by Category")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Views', y='Category', data=category_summary, palette='viridis', ax=ax)
    ax.set_title('Total Views by Category', fontsize=16)
    st.pyplot(fig)

    # Insights
    st.subheader("💡 Category Insights")
    top_category_views = category_summary.loc[category_summary['Views'].idxmax()]
    top_category_ctr = category_summary.loc[category_summary['Impressions click-through rate (%)'].idxmax()]
    st.write(f"- The category with the **highest total views** is **{top_category_views['Category']}** with **{top_category_views['Views']:.0f} views**.")
    st.write(f"- The category with the **highest average CTR** is **{top_category_ctr['Category']}** with **{top_category_ctr['Impressions click-through rate (%)']:.2f}% CTR**.")

   # Top Videos by Category
    st.subheader("🎬 Top Videos by Category")
    selected_category = st.selectbox("Select a Category:", category_summary['Category'].tolist())
    if selected_category:
        filtered_data = data[data['Category'] == selected_category]
        st.write(f"**Top 10 Videos in {selected_category} Category:**")
        top_videos = filtered_data.sort_values(by='Views', ascending=False).head(10)
        st.write(top_videos[['Video title', 'Views', 'Watch time (hours)', 'Impressions click-through rate (%)']])

# Search Functionality
    st.header("🔍 Search for a Specific Video")
    search_query = st.text_input("Enter a video title or keyword:")
    if search_query:
        search_results = data[data['Video title'].str.contains(search_query, case=False, na=False)]
        if not search_results.empty:
            st.write("Search Results:")
            st.dataframe(search_results[['Video title', 'Category', 'Views', 'Watch time (hours)', 'Impressions click-through rate (%)']])
        else:
            st.warning("No results found for your search query.")
