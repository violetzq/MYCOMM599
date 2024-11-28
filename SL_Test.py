import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Title and Description
st.title("Audience Demographic Insights")
st.markdown("Analyze audience demographics by age, gender, and geographic location.")

# Load Datasets
@st.cache_data
def load_data():
    age_data_url = "https://github.com/violetzq/MYCOMM599/blob/e5c370493167f24014feb88f6ab158e1dda1dad3/Viewer_age.csv?raw=true"
    gender_data_url = "https://github.com/violetzq/MYCOMM599/blob/e5c370493167f24014feb88f6ab158e1dda1dad3/Viewer_gender.csv?raw=true"
    city_data_url = "https://github.com/violetzq/MYCOMM599/blob/05a00ee4078e0b56c6cc6a433d7a3dba1d1e8942/Viewer_Cities.csv?raw=true"
    age_data = pd.read_csv(age_data_url)
    gender_data = pd.read_csv(gender_data_url)
    city_data = pd.read_csv(city_data_url)
    return age_data, gender_data, city_data

try:
    age_data, gender_data, city_data = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# 1. Age Distribution
st.subheader("1. Age Distribution")
try:
    st.markdown("**Percentage of Views by Age Group**")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Viewer age", y="Views (%)", data=age_data, ax=ax)
    ax.set_ylabel("Views (%)")
    ax.set_xlabel("Age Group")
    ax.set_title("Viewership by Age Group")
    st.pyplot(fig)

    st.markdown("**Insights:**")
    st.write("- Identify the age group that dominates the viewership.")
    st.write("- Adjust programming to cater to high-engagement age groups.")
except Exception as e:
    st.error(f"Error in Age Distribution Analysis: {e}")

# 2. Gender Distribution
st.subheader("2. Gender Distribution")
try:
    st.markdown("**Percentage of Views by Gender**")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Viewer gender", y="Views (%)", data=gender_data, ax=ax)
    ax.set_ylabel("Views (%)")
    ax.set_xlabel("Gender")
    ax.set_title("Viewership by Gender")
    st.pyplot(fig)

    st.markdown("**Insights:**")
    st.write("- Understand whether one gender dominates the viewership.")
    st.write("- Tailor marketing and programming strategies accordingly.")
except Exception as e:
    st.error(f"Error in Gender Distribution Analysis: {e}")

# 3. Geographic Location
st.subheader("3. Geographic Location")
try:
    st.markdown("**Top Cities by Views**")
    top_cities = city_data.sort_values("Views", ascending=False).head(10)
    st.dataframe(top_cities)

    st.markdown("**City Viewership Distribution**")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y="City name", x="Views", data=top_cities, ax=ax)
    ax.set_ylabel("City")
    ax.set_xlabel("Total Views")
    ax.set_title("Top Cities by Total Views")
    st.pyplot(fig)

    st.markdown("**Insights:**")
    st.write("- Identify regions with high engagement.")
    st.write("- Adjust content or promotions for underperforming regions.")
except Exception as e:
    st.error(f"Error in Geographic Location Analysis: {e}")
