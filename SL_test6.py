import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Main Title
st.title("Multi-Feature Analysis App")

# Sidebar Navigation
menu = st.sidebar.radio("Choose a Feature", ("YouTube Audience Insights", "Content Performance Analysis"))

# Feature 1: YouTube Audience Insights
if menu == "YouTube Audience Insights":
    st.header("YouTube Audience Insights")

    # Data Loading Functions
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

    # Data Visualization
    st.subheader("1. Age Distribution")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=age_data, x="Viewer age", y="Views (%)", palette="viridis", ax=ax1)
    ax1.set_title("Age Group Distribution of Views")
    st.pyplot(fig1)

    st.subheader("2. Gender Distribution")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=gender_data, x="Viewer gender", y="Views (%)", palette="coolwarm", ax=ax2)
    ax2.set_title("Gender Distribution of Views")
    st.pyplot(fig2)

    st.subheader("3. Geographic Location Analysis")
    city_search_term = st.text_input("Search for a City (e.g., New York, London):").strip()
    if city_search_term:
        filtered_city_data = cities_data[cities_data["City name"].str.contains(city_search_term, case=False, na=False)]
        if not filtered_city_data.empty:
            st.write("Search Results:")
            st.write(filtered_city_data)
        else:
            st.warning("No results found for the specified city.")

# Feature 2: Content Performance Analysis
elif menu == "Content Performance Analysis":
    st.header("Content Performance Analysis")

    # Data Loading Function
    @st.cache_data
    def load_content_data():
        url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv"
        return pd.read_csv(url, encoding='ISO-8859-1')

    data = load_content_data()

    if not data.empty:
        categories = {
            "Border Security": ["border", "customs", "security"],
            "Wildlife": ["wildlife", "animal", "nature"],
            "Adventure": ["adventure", "journey", "explore"],
            "Crime": ["crime", "criminal", "police"],
        }

        def assign_category(title):
            for category, keywords in categories.items():
                if any(keyword.lower() in str(title).lower() for keyword in keywords):
                    return category
            return "Other"

        data['Category'] = data['Video title'].apply(assign_category)

        category_summary = data.groupby('Category').agg({
            'Views': 'sum',
            'Watch time (hours)': 'sum'
        }).reset_index()

        st.subheader("Category Performance Overview")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='Views', y='Category', data=category_summary, palette='viridis', ax=ax)
        ax.set_title('Total Views by Category')
        st.pyplot(fig)

        selected_category = st.selectbox("Select a Category:", category_summary['Category'].tolist())
        if selected_category:
            filtered_data = data[data['Category'] == selected_category]
            st.write(f"Top 10 Videos in {selected_category} Category:")
            st.dataframe(filtered_data[['Video title', 'Views', 'Watch time (hours)']].head(10))
