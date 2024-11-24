{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPiSd1G3Rj4a5wADT8hRYTY",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/violetzq/MYCOMM599/blob/main/SL_Test.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install streamlit"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "JVxvMOsJMHRD",
        "outputId": "7b223e68-3cfa-4fd7-8de7-2d17d85224ca"
      },
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting streamlit\n",
            "  Downloading streamlit-1.40.1-py2.py3-none-any.whl.metadata (8.5 kB)\n",
            "Requirement already satisfied: altair<6,>=4.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (4.2.2)\n",
            "Requirement already satisfied: blinker<2,>=1.0.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (1.9.0)\n",
            "Requirement already satisfied: cachetools<6,>=4.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (5.5.0)\n",
            "Requirement already satisfied: click<9,>=7.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (8.1.7)\n",
            "Requirement already satisfied: numpy<3,>=1.20 in /usr/local/lib/python3.10/dist-packages (from streamlit) (1.26.4)\n",
            "Requirement already satisfied: packaging<25,>=20 in /usr/local/lib/python3.10/dist-packages (from streamlit) (24.2)\n",
            "Requirement already satisfied: pandas<3,>=1.4.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (2.2.2)\n",
            "Requirement already satisfied: pillow<12,>=7.1.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (11.0.0)\n",
            "Requirement already satisfied: protobuf<6,>=3.20 in /usr/local/lib/python3.10/dist-packages (from streamlit) (4.25.5)\n",
            "Requirement already satisfied: pyarrow>=7.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (17.0.0)\n",
            "Requirement already satisfied: requests<3,>=2.27 in /usr/local/lib/python3.10/dist-packages (from streamlit) (2.32.3)\n",
            "Requirement already satisfied: rich<14,>=10.14.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (13.9.4)\n",
            "Requirement already satisfied: tenacity<10,>=8.1.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (9.0.0)\n",
            "Requirement already satisfied: toml<2,>=0.10.1 in /usr/local/lib/python3.10/dist-packages (from streamlit) (0.10.2)\n",
            "Requirement already satisfied: typing-extensions<5,>=4.3.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (4.12.2)\n",
            "Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /usr/local/lib/python3.10/dist-packages (from streamlit) (3.1.43)\n",
            "Collecting pydeck<1,>=0.8.0b4 (from streamlit)\n",
            "  Downloading pydeck-0.9.1-py2.py3-none-any.whl.metadata (4.1 kB)\n",
            "Requirement already satisfied: tornado<7,>=6.0.3 in /usr/local/lib/python3.10/dist-packages (from streamlit) (6.3.3)\n",
            "Collecting watchdog<7,>=2.1.5 (from streamlit)\n",
            "  Downloading watchdog-6.0.0-py3-none-manylinux2014_x86_64.whl.metadata (44 kB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m44.3/44.3 kB\u001b[0m \u001b[31m882.5 kB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hRequirement already satisfied: entrypoints in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (0.4)\n",
            "Requirement already satisfied: jinja2 in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (3.1.4)\n",
            "Requirement already satisfied: jsonschema>=3.0 in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (4.23.0)\n",
            "Requirement already satisfied: toolz in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (0.12.1)\n",
            "Requirement already satisfied: gitdb<5,>=4.0.1 in /usr/local/lib/python3.10/dist-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.11)\n",
            "Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.10/dist-packages (from pandas<3,>=1.4.0->streamlit) (2.8.2)\n",
            "Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.10/dist-packages (from pandas<3,>=1.4.0->streamlit) (2024.2)\n",
            "Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.10/dist-packages (from pandas<3,>=1.4.0->streamlit) (2024.2)\n",
            "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.27->streamlit) (3.4.0)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.27->streamlit) (3.10)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.27->streamlit) (2.2.3)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.27->streamlit) (2024.8.30)\n",
            "Requirement already satisfied: markdown-it-py>=2.2.0 in /usr/local/lib/python3.10/dist-packages (from rich<14,>=10.14.0->streamlit) (3.0.0)\n",
            "Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /usr/local/lib/python3.10/dist-packages (from rich<14,>=10.14.0->streamlit) (2.18.0)\n",
            "Requirement already satisfied: smmap<6,>=3.0.1 in /usr/local/lib/python3.10/dist-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.1)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.10/dist-packages (from jinja2->altair<6,>=4.0->streamlit) (3.0.2)\n",
            "Requirement already satisfied: attrs>=22.2.0 in /usr/local/lib/python3.10/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (24.2.0)\n",
            "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /usr/local/lib/python3.10/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (2024.10.1)\n",
            "Requirement already satisfied: referencing>=0.28.4 in /usr/local/lib/python3.10/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.35.1)\n",
            "Requirement already satisfied: rpds-py>=0.7.1 in /usr/local/lib/python3.10/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.21.0)\n",
            "Requirement already satisfied: mdurl~=0.1 in /usr/local/lib/python3.10/dist-packages (from markdown-it-py>=2.2.0->rich<14,>=10.14.0->streamlit) (0.1.2)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.10/dist-packages (from python-dateutil>=2.8.2->pandas<3,>=1.4.0->streamlit) (1.16.0)\n",
            "Downloading streamlit-1.40.1-py2.py3-none-any.whl (8.6 MB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m8.6/8.6 MB\u001b[0m \u001b[31m26.3 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading pydeck-0.9.1-py2.py3-none-any.whl (6.9 MB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m6.9/6.9 MB\u001b[0m \u001b[31m27.1 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading watchdog-6.0.0-py3-none-manylinux2014_x86_64.whl (79 kB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m79.1/79.1 kB\u001b[0m \u001b[31m4.1 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hInstalling collected packages: watchdog, pydeck, streamlit\n",
            "Successfully installed pydeck-0.9.1 streamlit-1.40.1 watchdog-6.0.0\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 5,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 287
        },
        "id": "PkRqqTK-L29j",
        "outputId": "6190642e-946c-4ce9-86e6-ae1ca0a4047f"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "Downloading...\n",
            "From: https://drive.google.com/uc?id=1s43YIPGUU8OmPil3dbsMAyul8tg-nwON\n",
            "To: /content/DangerTV_Content_1.csv\n",
            "100%|██████████| 71.8k/71.8k [00:00<00:00, 36.9MB/s]\n"
          ]
        },
        {
          "output_type": "error",
          "ename": "NameError",
          "evalue": "name 'data' is not defined",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-5-838714352d84>\u001b[0m in \u001b[0;36m<cell line: 35>\u001b[0;34m()\u001b[0m\n\u001b[1;32m     33\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     34\u001b[0m \u001b[0;31m# Add a 'Category' column\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 35\u001b[0;31m \u001b[0mdata\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'Category'\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mdata\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'Video title'\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mapply\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0massign_category\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     36\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     37\u001b[0m \u001b[0;31m# Sidebar for filtering\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mNameError\u001b[0m: name 'data' is not defined"
          ]
        }
      ],
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import seaborn as sns\n",
        "import matplotlib.pyplot as plt\n",
        "import gdown\n",
        "\n",
        "# Load your dataset\n",
        "file_id = '1s43YIPGUU8OmPil3dbsMAyul8tg-nwON'\n",
        "gdown.download(f'https://drive.google.com/uc?id={file_id}', 'DangerTV_Content_1.csv', quiet=False)\n",
        "\n",
        "df = pd.read_csv('DangerTV_Content_1.csv', encoding='ISO-8859-1')\n",
        "df.head()\n",
        "\n",
        "# Add categories (assuming you've already assigned them)\n",
        "categories = {\n",
        "    \"Border Security\": [\"border\", \"customs\", \"security\"],\n",
        "    \"Wildlife\": [\"wildlife\", \"animal\", \"nature\", \"wild\", \"hunting\", \"bear\"],\n",
        "    \"Adventure\": [\"adventure\", \"journey\", \"explore\", \"trap\", \"wilderness\", \"weather\", \"severe\", \"survive\", \"climbing\", \"storm\", \"coast guard\"],\n",
        "    \"Crime\": [\"crime\", \"criminal\", \"police\", \"investigation\", \"drug\", \"jail\", \"sin\"],\n",
        "    \"Human Stories & Disaster\": [\"life\", \"story\", \"family\", \"personal\", \"survive\", \"tsunami\", \"earthquake\", \"tornado\", \"dead\", \"risk\", \"tribe\"],\n",
        "    \"Vehicles\": [\"car\", \"truck\", \"vehicle\", \"auto\", \"transport\"],\n",
        "    \"Maritime\": [\"ship\", \"boat\", \"ocean\", \"sea\", \"fish\", \"fishing\", \"sail\", \"sailor\"],\n",
        "    \"Bull Fight\": [\"bulls\", \"matadors\"],\n",
        "    \"Battle & Special Forces\": [\"battle\", \"war\", \"afghanistan\", \"training\", \"special forces\", \"rescue\", \"fight\", \"swat\", \"k-9\"]\n",
        "}\n",
        "\n",
        "# Function to assign categories\n",
        "def assign_category(title):\n",
        "    for category, keywords in categories.items():\n",
        "        if any(keyword.lower() in str(title).lower() for keyword in keywords):\n",
        "            return category\n",
        "    return \"Other\"\n",
        "\n",
        "# Add a 'Category' column\n",
        "data['Category'] = data['Video title'].apply(assign_category)\n",
        "\n",
        "# Sidebar for filtering\n",
        "st.sidebar.header(\"Filter Options\")\n",
        "selected_category = st.sidebar.selectbox(\"Select a Category\", options=[\"All\"] + list(categories.keys()))\n",
        "\n",
        "# Filter data based on category\n",
        "if selected_category != \"All\":\n",
        "    filtered_data = data[data['Category'] == selected_category]\n",
        "else:\n",
        "    filtered_data = data\n",
        "\n",
        "# Overview Section\n",
        "st.title(\"Content Performance Analysis\")\n",
        "st.header(\"Overview of All Categories\")\n",
        "\n",
        "# Aggregate data by category\n",
        "category_summary = data.groupby('Category').agg({\n",
        "    'Views': 'sum',\n",
        "    'Watch time (hours)': 'sum',\n",
        "    'Impressions click-through rate (%)': 'mean'\n",
        "}).reset_index()\n",
        "\n",
        "# Bar chart for total views by category\n",
        "st.subheader(\"Total Views by Category\")\n",
        "fig, ax = plt.subplots(figsize=(10, 6))\n",
        "sns.barplot(x='Views', y='Category', data=category_summary, palette='viridis', ax=ax)\n",
        "st.pyplot(fig)\n",
        "\n",
        "# Insights Section\n",
        "st.header(\"Insights\")\n",
        "top_category_views = category_summary.loc[category_summary['Views'].idxmax()]\n",
        "top_category_ctr = category_summary.loc[category_summary['Impressions click-through rate (%)'].idxmax()]\n",
        "\n",
        "st.markdown(f\"- The category with the **highest total views** is **{top_category_views['Category']}** with **{top_category_views['Views']:.0f} views**.\")\n",
        "st.markdown(f\"- The category with the **highest average CTR** is **{top_category_ctr['Category']}** with **{top_category_ctr['Impressions click-through rate (%)']:.2f}% CTR**.\")\n",
        "\n",
        "# Top Videos by Category Section\n",
        "st.header(\"Top Videos by Selected Category\")\n",
        "if not filtered_data.empty:\n",
        "    top_videos = filtered_data.sort_values(by='Views', ascending=False).head(10)\n",
        "    st.write(\"Top 10 Videos:\")\n",
        "    st.dataframe(top_videos[['Video title', 'Views', 'Watch time (hours)', 'Impressions click-through rate (%)']])\n",
        "else:\n",
        "    st.write(\"No videos found for the selected category.\")\n",
        "\n",
        "# Search Functionality\n",
        "st.header(\"Search for a Specific Video\")\n",
        "search_query = st.text_input(\"Enter a video title or keyword:\")\n",
        "if search_query:\n",
        "    search_results = data[data['Video title'].str.contains(search_query, case=False, na=False)]\n",
        "    if not search_results.empty:\n",
        "        st.write(\"Search Results:\")\n",
        "        st.dataframe(search_results[['Video title', 'Category', 'Views', 'Watch time (hours)', 'Impressions click-through rate (%)']])\n",
        "    else:\n",
        "        st.write(\"No results found for your search query.\")"
      ]
    }
  ]
}
