import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset from GitHub
data_url = 'https://raw.githubusercontent.com/violetzq/MYCOMM599/main/DangerTV_Content.csv'
data = pd.read_csv(data_url, encoding='ISO-8859-1')

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

# Bar chart for total views by category
plt.figure(figsize=(12, 6))
sns.barplot(x='Views', y='Category', data=category_summary, palette='viridis')
plt.title('Total Views by Category')
plt.xlabel('Total Views')
plt.ylabel('Category')
plt.tight_layout()
plt.show()
plt.close('all')  # Close the figure to prevent it from stacking in future plots

# Insights
print("Insights:")
top_category_views = category_summary.loc[category_summary['Views'].idxmax()]
top_category_ctr = category_summary.loc[category_summary['Impressions click-through rate (%)'].idxmax()]
print(f"- The category with the highest total views is {top_category_views['Category']} with {top_category_views['Views']:.0f} views.")
print(f"- The category with the highest average CTR is {top_category_ctr['Category']} with {top_category_ctr['Impressions click-through rate (%)']:.2f}% CTR.")

# Top Videos by Category
selected_category = "Wildlife"  # Replace with your choice
filtered_data = data[data['Category'] == selected_category]

if not filtered_data.empty:
    print(f"\nTop 10 Videos in {selected_category}:")
    top_videos = filtered_data.sort_values(by='Views', ascending=False).head(10)
    print(top_videos[['Video title', 'Views', 'Watch time (hours)', 'Impressions click-through rate (%)']])
else:
    print(f"No videos found in category {selected_category}.")
