import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Programming Strategy Insights", page_icon="📊", layout="wide")

# Load Dataset
@st.cache_data
def load_content_data():
    url = "https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv"
    try:
        # Parse "Video publish time" as the date column
        return pd.read_csv(url, parse_dates=["Video publish time"])
    except ValueError:
        # Fallback: Load without parsing dates if "Video publish time" doesn't exist
        data = pd.read_csv(url)
        st.warning("The column 'Video publish time' was not found. Proceeding without date-based analysis.")
        return data

# Load Data
data = load_content_data()

# Data Preparation
if "Video publish time" in data.columns:
    data["Day of Week"] = data["Video publish time"].dt.day_name()  # Extract day of the week
    average_views_day = data.groupby("Day of Week")["Views"].mean().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )  # Average views by day of week

# Layout: Proportional Content
st.title("📊 Programming Strategy Insights")

# Organize baseline performance and title-specific comparison into columns
col1, col2 = st.columns(2)

# Baseline Analysis
with col1:
    st.subheader("Baseline Viewership Performance")
    if "Day of Week" in data.columns:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=average_views_day.index, y=average_views_day.values, palette="viridis", ax=ax)
        ax.set_title("Baseline: Average Views by Day of Week", fontsize=12)
        ax.set_ylabel("Average Views")
        ax.set_xlabel("Day of Week")
        plt.xticks(rotation=45)
        st.pyplot(fig)

# Title-Specific Comparison
with col2:
    st.subheader("Compare Specific Titles to the Baseline")

    # Select a Title
    if "Video title" in data.columns:
        title_list = data["Video title"].unique().tolist()
        selected_title = st.selectbox("Select a Video Title:", title_list)

        if selected_title:
            # Extract data for the selected title
            title_data = data[data["Video title"] == selected_title]

            if "Day of Week" in title_data.columns:
                # Handle missing days gracefully
                title_views_day = title_data.groupby("Day of Week")["Views"].mean().reindex(
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], fill_value=0
                )

                # Visualize Comparison
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.barplot(x=title_views_day.index, y=title_views_day.values, palette="coolwarm", ax=ax)
                ax.set_title(f"Performance of '{selected_title}' by Day of Week", fontsize=12)
                ax.set_ylabel("Average Views")
                ax.set_xlabel("Day of Week")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            else:
                st.warning(f"No day-of-week data available for the selected title '{selected_title}'.")

# Recommendations Section
st.subheader("💡 Recommendations Based on Comparison")
if "Video title" in data.columns and selected_title:
    if not title_data.empty:
        # Compare title's average views to baseline
        title_avg_views = title_data["Views"].mean()
        baseline_avg_views = data["Views"].mean()

        if title_avg_views > baseline_avg_views:
            st.write(
                f"- The video **'{selected_title}'** is performing **above average** with an average of {title_avg_views:.0f} views compared to the baseline of {baseline_avg_views:.0f} views."
            )
        else:
            st.write(
                f"- The video **'{selected_title}'** is performing **below average** with an average of {title_avg_views:.0f} views compared to the baseline of {baseline_avg_views:.0f} views. Consider improving its visibility or content."
            )
    else:
        st.write("No data available for the selected title.")
