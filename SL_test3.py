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
        # Try parsing with the assumed date column "Upload date"
        return pd.read_csv(url, parse_dates=["Upload date"])  # Replace with correct column if needed
    except ValueError:
        # Fallback: Load without parsing dates if "Upload date" doesn't exist
        data = pd.read_csv(url)
        st.warning("The column 'Upload date' was not found. Proceeding without date-based analysis.")
        return data

# Load Data
data = load_content_data()

# Inspect Columns and Handle Missing Date Column
if "Upload date" not in data.columns:
    st.warning("Date-based analysis is unavailable because the 'Upload date' column is missing.")
else:
    data["Day of Week"] = data["Upload date"].dt.day_name()  # Extract day of the week
    average_views_day = data.groupby("Day of Week")["Views"].mean().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )  # Average views by day of week

# Group by Day and Category for deeper insights
if "Day of Week" in data.columns and "Category" in data.columns:
    day_category = data.groupby(["Day of Week", "Category"])["Views"].mean().unstack()

# Streamlit Layout
st.title("📊 Programming Strategy Insights")
st.subheader("Baseline Viewership Performance")

# Average Views by Day of Week (Baseline)
if "Day of Week" in data.columns:
    st.write("**Average Views by Day of Week**")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=average_views_day.index, y=average_views_day.values, palette="viridis", ax=ax)
    ax.set_title("Baseline: Average Views by Day of Week", fontsize=12)
    ax.set_ylabel("Average Views")
    ax.set_xlabel("Day of Week")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Average Views by Day of Week and Category
    if "Category" in data.columns:
        st.subheader("Average Views by Day of Week and Category")
        st.dataframe(day_category.style.background_gradient(cmap="coolwarm"))

# Allow the user to compare specific titles
st.subheader("Compare Specific Titles to the Baseline")

# Select a Title
if "Video title" in data.columns:
    title_list = data["Video title"].unique().tolist()
    selected_title = st.selectbox("Select a Video Title:", title_list)

    if selected_title:
        # Extract data for the selected title
        title_data = data[data["Video title"] == selected_title]

        # Calculate views by day of week for the selected title
        if "Day of Week" in title_data.columns:
            title_views_day = title_data.groupby("Day of Week")["Views"].mean().reindex(
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            )

            # Visualize Comparison
            st.write(f"**Performance of '{selected_title}' by Day of Week**")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=title_views_day.index, y=title_views_day.values, palette="coolwarm", ax=ax)
            ax.set_title(f"Performance of '{selected_title}' vs Baseline", fontsize=12)
            ax.set_ylabel("Average Views")
            ax.set_xlabel("Day of Week")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Highlight Recommendations
        st.subheader("💡 Recommendations Based on Comparison")
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
else:
    st.warning("The dataset does not contain 'Video title' column, so title-specific analysis is unavailable.")
