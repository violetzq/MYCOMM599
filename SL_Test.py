import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Title and Description
st.title("Audience Demographic Analysis")
st.markdown(
    """
    Understand your audience composition and identify key demographic groups engaging with your content.
    """
)

# Load Data Function
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# Load Data
try:
    cities_url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Cities_1%20(1).csv"
    age_url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_age.csv"
    gender_url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Viewer_gender.csv"

    cities_data = load_data(cities_url)
    age_data = load_data(age_url)
    gender_data = load_data(gender_url)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Section 1.2: Age Distribution
st.subheader("1.2 Age Distribution")
st.markdown("Identify which age groups dominate the viewership.")

try:
    # Bar chart of age group views
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=age_data, x="Age Group", y="Views", ax=ax1)
    ax1.set_title("Views by Age Group")
    ax1.set_ylabel("Total Views")
    ax1.set_xlabel("Age Group")
    st.pyplot(fig1)

    # Insights
    max_age_group = age_data.loc[age_data["Views"].idxmax(), "Age Group"]
    st.write(f"The age group with the most views is **{max_age_group}**.")
except Exception as e:
    st.error(f"Error analyzing age distribution: {e}")

# Section 1.3: Gender Distribution
st.subheader("1.3 Gender Distribution")
st.markdown("Understand the gender balance of the audience.")

try:
    # Bar chart of gender distribution
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=gender_data, x="Gender", y="Views", ax=ax2)
    ax2.set_title("Views by Gender")
    ax2.set_ylabel("Total Views")
    ax2.set_xlabel("Gender")
    st.pyplot(fig2)

    # Gender ratio
    total_views = gender_data["Views"].sum()
    gender_data["Percentage"] = (gender_data["Views"] / total_views) * 100
    male_percentage = gender_data.loc[gender_data["Gender"] == "Male", "Percentage"].values[0]
    female_percentage = gender_data.loc[gender_data["Gender"] == "Female", "Percentage"].values[0]
    st.write(f"Gender ratio: **{male_percentage:.1f}% Male**, **{female_percentage:.1f}% Female**.")
except Exception as e:
    st.error(f"Error analyzing gender distribution: {e}")

# Section 1.5: Geographic Location
st.subheader("1.5 Geographic Location")
st.markdown("Identify where the audience is geographically concentrated.")

try:
    # Bar chart of top cities
    top_cities = cities_data.nlargest(10, "Views")
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_cities, x="City", y="Views", ax=ax3)
    ax3.set_title("Top 10 Cities by Views")
    ax3.set_ylabel("Total Views")
    ax3.set_xlabel("City")
    ax3.tick_params(axis='x', rotation=45)
    st.pyplot(fig3)

    # Insights
    st.write("**Top-performing cities:**")
    st.write(top_cities[["City", "Views"]])
except Exception as e:
    st.error(f"Error analyzing geographic location: {e}")

# Section 1.6: Recommendations
st.subheader("1.6 Recommendations Based on Audience Segmentation")
st.write(
    """
    - **Age Groups:** Focus on creating content tailored to the age group with the most views, while exploring ways to attract other age groups.
    - **Gender:** Leverage the gender insights to create targeted marketing strategies.
    - **Geographic Targeting:** Promote content in top-performing cities and explore opportunities to grow viewership in underperforming areas.
    """
)
