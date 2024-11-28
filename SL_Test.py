import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Title and Description
st.title("Audience Demographics Analysis Dashboard")
st.markdown("Analyze the audience demographics and extract actionable insights.")

# Load Dataset
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

try:
    # Correct URLs
    cities_data = load_data("https://raw.githubusercontent.com/violetzq/MYCOMM599/05a00ee4078e0b56c6cc6a433d7a3dba1d1e8942/Viewer_Cities.csv")
    age_data = load_data("https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_age.csv")
    gender_data = load_data("https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_gender.csv")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# 1. Audience Demographics Overview
st.subheader("1. Audience Demographics Overview")
st.markdown("Understand the composition of your audience.")

# 1.1 Age Distribution
st.subheader("1.1 Age Distribution")
try:
    if "Age Group" in age_data.columns and "Views" in age_data.columns:
        age_chart = age_data.groupby("Age Group")[["Views"]].sum().sort_values(by="Views", ascending=False)

        # Bar chart
        st.bar_chart(age_chart)

        st.write("**Insights:**")
        st.write("- Identify which age groups dominate the viewership.")
        st.write("- Suggest content tailored to the interests of dominant age groups.")
    else:
        st.error("Age data does not have the required columns ('Age Group', 'Views').")
except Exception as e:
    st.error(f"Error processing age data: {e}")

# 1.2 Gender Distribution
st.subheader("1.2 Gender Distribution")
try:
    if "Gender" in gender_data.columns and "Views" in gender_data.columns:
        gender_chart = gender_data.groupby("Gender")[["Views"]].sum()

        # Pie chart
        fig, ax = plt.subplots()
        ax.pie(gender_chart["Views"], labels=gender_chart.index, autopct="%1.1f%%", startangle=90, colors=["#ff9999","#66b3ff"])
        ax.set_title("Gender Distribution")
        st.pyplot(fig)

        st.write("**Insights:**")
        st.write("- Understand the gender balance in the audience.")
        st.write("- Suggest content strategies for engaging with underrepresented genders.")
    else:
        st.error("Gender data does not have the required columns ('Gender', 'Views').")
except Exception as e:
    st.error(f"Error processing gender data: {e}")

# 1.3 Geographic Location
st.subheader("1.3 Geographic Location")
try:
    if "City" in cities_data.columns and "Views" in cities_data.columns:
        city_chart = cities_data.groupby("City")[["Views"]].sum().sort_values(by="Views", ascending=False).head(10)

        # Bar chart
        st.bar_chart(city_chart)

        st.write("**Insights:**")
        st.write("- Identify top-performing cities based on viewership.")
        st.write("- Suggest promotional strategies targeting high-performing locations.")
    else:
        st.error("City data does not have the required columns ('City', 'Views').")
except Exception as e:
    st.error(f"Error processing city data: {e}")

# 1.4 Recommendations
st.subheader("1.4 Recommendations Based on Audience Segmentation")
st.markdown(
    """
    - **Personalization:** Create content tailored for dominant age and gender groups.
    - **Geographic Targeting:** Focus marketing efforts on top-performing cities.
    - **Expansion Opportunities:** Explore strategies to engage underrepresented demographics.
    """
)
