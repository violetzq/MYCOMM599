import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("YouTube Audience Demographic Analysis with Search and Subscription Insights")

# Load Dataset Functions
@st.cache_data
def load_subscription_chart_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Subscription%20status_Chart%20data.csv"
    return pd.read_csv(url)

@st.cache_data
def load_subscription_summary_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/Subscription_status.csv"
    return pd.read_csv(url)

# Load Data
try:
    subscription_chart_data = load_subscription_chart_data()
    subscription_summary_data = load_subscription_summary_data()
except Exception as e:
    st.error(f"Error loading subscription data: {e}")
    st.stop()

# Data Preprocessing
try:
    # Preprocess subscription chart data
    subscription_chart_data['Date'] = pd.to_datetime(subscription_chart_data['Date'], errors='coerce')

    # Remove unnecessary rows from subscription summary data
    subscription_summary_data = subscription_summary_data[
        subscription_summary_data['Subscription status'] != "Total"
    ]
except Exception as e:
    st.error(f"Error processing subscription data: {e}")
    st.stop()

# Subscription Insights
st.subheader("Subscription Status Analysis")
st.markdown("Analyze viewership metrics for subscribed vs. non-subscribed viewers.")

# Search Feature for Subscription Data
st.subheader("Search Subscription Data")
search_term = st.text_input("Search by Subscription Status (e.g., Subscribed, Not subscribed):").strip()

if search_term:
    filtered_subscription_data = subscription_summary_data[
        subscription_summary_data["Subscription status"].str.contains(search_term, case=False, na=False)
    ]
    if not filtered_subscription_data.empty:
        st.write("**Search Results:**")
        st.write(filtered_subscription_data)
    else:
        st.warning("No results found. Try searching for another term.")

# Bar Chart for Summary Data
st.write("**Views by Subscription Status**")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=subscription_summary_data,
    x="Subscription status",
    y="Views",
    ax=ax1,
    palette="viridis"
)
ax1.set_title("Views by Subscription Status")
ax1.set_ylabel("Views")
ax1.set_xlabel("Subscription Status")
st.pyplot(fig1)

# Average View Duration Comparison
st.write("**Average View Duration by Subscription Status**")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=subscription_summary_data,
    x="Subscription status",
    y="Average view duration",
    ax=ax2,
    palette="coolwarm"
)
ax2.set_title("Average View Duration by Subscription Status")
ax2.set_ylabel("Average View Duration")
ax2.set_xlabel("Subscription Status")
st.pyplot(fig2)

# Subscription Trend Over Time
st.write("**Views Over Time by Subscription Status**")
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=subscription_chart_data,
    x="Date",
    y="Views",
    hue="Subscription status",
    ax=ax3
)
ax3.set_title("Views Over Time by Subscription Status")
ax3.set_ylabel("Views")
ax3.set_xlabel("Date")
st.pyplot(fig3)

# Geographic Location Search Feature (Optional)
st.subheader("Search by City (Optional)")
city_search_term = st.text_input("Search for City (e.g., New York, London):").strip()

# Mock Data Example (replace with actual city data in integration)
city_data = pd.DataFrame({
    "City": ["New York", "London", "Los Angeles", "Tokyo", "Chicago"],
    "Views": [2000000, 1500000, 1000000, 500000, 300000]
})

if city_search_term:
    filtered_city_data = city_data[city_data["City"].str.contains(city_search_term, case=False, na=False)]
    if not filtered_city_data.empty:
        st.write("**City Search Results:**")
        st.write(filtered_city_data)
    else:
        st.warning("No results found for the city. Try another search.")

# Insights
st.write("**Insights from Subscription Analysis:**")
st.write("- Compare metrics like views and average view duration between subscribed and non-subscribed audiences.")
st.write("- Use trends over time to identify shifts in engagement and strategize content or marketing accordingly.")
st.write("- Prioritize engaging content for subscribed viewers while encouraging non-subscribed viewers to subscribe.")

# Recommendations
st.subheader("Recommendations Based on Subscription Insights")
st.write("- **Engagement Strategy:** Create content tailored to engaged (subscribed) audiences and include calls-to-action for non-subscribers.")
st.write("- **Content Promotion:** Use insights to promote specific types of content that are popular among non-subscribed viewers.")
