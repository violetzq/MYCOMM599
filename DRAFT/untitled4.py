# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I4uJ3kniYj9u9M4nVW29Kvox6idckQlg
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Streamlit page configuration
st.set_page_config(page_title="Content Performance Analysis", layout="wide")

# Load your dataset from GitHub
@st.cache
def load_data():
    data_url = 'https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv'
    data = pd.read_csv(data_url, encoding='ISO-8859-1')
    return data

data = load_data()

# Add categories
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

# Assign categories
data['Category'] = data['Video title'].apply(assign_category)

# Sidebar filters
st.sidebar.header("Filter Options")
selected_category = st.sidebar.selectbox("Select a Category", options=["All"] + list(categories.keys()))

# Filter data
filtered_data = data if selected_category == "All" else data[data['Category'] == selected_category]

# Overview
st.title("Content Performance Analysis")
st.header("Overview of All Categories")

category_summary = data.groupby('Category').agg({
    'Views': 'sum',
    'Watch time (hours)': 'sum',
    'Impressions click-through rate (%)': 'mean'
}).reset_index()

# Total Views by Category
st.subheader("Total Views by Category")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Views', y='Category', data=category_summary, palette='viridis', ax=ax)
st.pyplot(fig)

# Insights
st.header("Insights")
top_category_views = category_summary.loc[category_summary['Views'].idxmax()]
top_category_ctr = category_summary.loc[category_summary['Impressions click-through rate (%)'].idxmax()]

st.markdown(f"- The category with the **highest total views** is **{top_category_views['Category']}** with **{top_category_views['Views']:.0f} views**.")
st.markdown(f"- The category with the **highest average CTR** is **{top_category_ctr['Category']}** with **{top_category_ctr['Impressions click-through rate (%)']:.2f}% CTR**.")

# Top Videos
st.header(f"Top Videos in {selected_category if selected_category != 'All' else 'All Categories'}")
if not filtered_data.empty:
    top_videos = filtered_data.sort_values(by='Views', ascending=False).head(10)
    st.write("Top 10 Videos:")
    st.dataframe(top_videos[['Video title', 'Category', 'Views', 'Watch time (hours)', 'Impressions click-through rate (%)']])
else:
    st.write("No videos found for the selected category.")

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
