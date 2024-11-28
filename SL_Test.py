import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("YouTube Audience Demographics and Insights")

# Load Dataset Functions
@st.cache_data
def load_age_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_age.csv"
    return pd.read_csv(url)

@st.cache_data
def load_gender_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_gender.csv"
    data = pd.read_csv(url)
    # Remove "User-specified" from gender data
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

# 1. Age Distribution
st.subheader("1. Age Distribution")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(data=age_data, x="Viewer age", y="Views (%)", palette="viridis", ax=ax1)
ax1.set_title("Age Group Distribution of Views")
ax1.set_ylabel("Views (%)")
ax1.set_xlabel("Age Group")
st.pyplot(fig1)

# 2. Gender Distribution
st.subheader("2. Gender Distribution")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(data=gender_data, x="Viewer gender", y="Views (%)", palette="coolwarm", ax=ax2)
ax2.set_title("Gender Distribution of Views")
ax2.set_ylabel("Views (%)")
ax2.set_xlabel("Gender")
st.pyplot(fig2)

# 3. Geographic Location
st.subheader("3. Geographic Location")

# Search Feature for City Data
st.subheader("Search by City")
city_search_term = st.text_input("Search for City (e.g., New York, London):").strip()
if city_search_term:
    filtered_city_data = cities_data[cities_data["City name"].str.contains(city_search_term, case=False, na=False)]
    if not filtered_city_data.empty:
        st.write("**City Search Results:**")
        st.write(filtered_city_data)
    else:
        st.warning("No results found for the city. Try another search.")

# Bar Chart for Top Cities by Views
st.write("**Top Cities by Views**")
top_cities = cities_data.sort_values(by="Views", ascending=False).head(10)
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_cities, x="Views", y="City name", palette="mako", ax=ax3)
ax3.set_title("Top 10 Cities by Views")
ax3.set_xlabel("Views")
ax3.set_ylabel("City")
st.pyplot(fig3)

# Heatmap for City Data
st.write("**City Heatmap (Views and Watch Time)**")
if "Views" in cities_data.columns and "Watch time (hours)" in cities_data.columns:
    heatmap_data = cities_data.pivot_table(
        index="City name", values=["Views", "Watch time (hours)"], aggfunc="sum"
    )
    fig4, ax4 = plt.subplots(figsize=(10, 12))
    sns.heatmap(
        heatmap_data,
        cmap="YlGnBu",
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        cbar_kws={"label": "Value"},
        ax=ax4,
    )
    ax4.set_title("Heatmap of Views and Watch Time by City")
    st.pyplot(fig4)
else:
    st.warning("Data for heatmap is missing.")

# 4. Subscription Data
st.subheader("4. Subscription Status")

# Bar Chart for Subscription Data
fig5, ax5 = plt.subplots(figsize=(8, 5))
sns.barplot(data=subscription_data, x="Subscription status", y="Views", palette="Set2", ax=ax5)
ax5.set_title("Views by Subscription Status")
ax5.set_ylabel("Total Views")
ax5.set_xlabel("Subscription Status")
st.pyplot(fig5)
