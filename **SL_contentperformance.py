import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Overview
st.title("Content Performance Analysis")
st.header("Overview of All Categories")

category_summary = data.groupby('Category').agg({
    'Views': 'sum',
    'Watch time (hours)': 'sum',
    'Impressions click-through rate (%)': 'mean'
}).reset_index()

# Load Dataset
@st.cache_data
def load_data():
    try:
        data_url = 'https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv'
        return pd.read_csv(data_url, encoding='ISO-8859-1')
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

data = load_data()

if data.empty:
    st.stop()

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

# Function to assign categories
def assign_category(title):
    for category, keywords in categories.items():
        if any(keyword.lower() in str(title).lower() for keyword in keywords):
            return category
    return "Other"

# Add a 'Category' column
data['Category'] = data['Video title'].apply(assign_category)

# Aggregate data by category
category_summary = data.groupby('Category').agg({
    'Views': 'sum',
    'Watch time (hours)': 'sum',
    'Impressions click-through rate (%)': 'mean'
}).reset_index()

# 1. Bar chart for total views by category
st.subheader("Total Views by Category")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='Views', y='Category', data=category_summary, palette='viridis', ax=ax)
ax.set_title('Total Views by Category')
ax.set_xlabel('Total Views')
ax.set_ylabel('Category')
st.pyplot(fig)

# Insights
st.subheader("Category Insights")
if not category_summary.empty:
    top_category_views = category_summary.loc[category_summary['Views'].idxmax()]
    top_category_ctr = category_summary.loc[category_summary['Impressions click-through rate (%)'].idxmax()]
    st.write(f"- The category with the **highest total views** is **{top_category_views['Category']}** with **{top_category_views['Views']:.0f} views**.")
    st.write(f"- The category with the **highest average CTR** is **{top_category_ctr['Category']}** with **{top_category_ctr['Impressions click-through rate (%)']:.2f}% CTR**.")
else:
    st.write("No data available for insights.")

# 2. Top Videos by Category
st.subheader("Top Videos by Category")
categories_list = category_summary['Category'].tolist()
selected_category = st.selectbox("Select a Category:", categories_list)

if selected_category:
    filtered_data = data[data['Category'] == selected_category]
    if not filtered_data.empty:
        st.write(f"**Top 10 Videos in {selected_category}:**")
        top_videos = filtered_data.sort_values(by='Views', ascending=False).head(10)
        st.write(top_videos[['Video title', 'Views', 'Watch time (hours)', 'Impressions click-through rate (%)']])
    else:
        st.warning(f"No videos found in category {selected_category}.")
        
# Search Functionality
st.header("Search for a Specific Video")
search_query = st.text_input("Enter a video title or keyword:")
if search_query:
    search_results = data[data['Video title'].str.contains(search_query, case=False, na=False)]
    if not search_results.empty:
        st.write("Search Results:")
        st.dataframe(search_results[['Video title', 'Category', 'Views', 'Watch time (hours)', 'Impressions click-through rate (%)']])
    else:
        st.write("No results found for your search query.")
