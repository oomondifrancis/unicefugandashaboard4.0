import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set the layout to wide mode
st.set_page_config(layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('media_data3.csv')

df = load_data()

# Streamlit Sidebar
st.sidebar.image('logo.png', use_column_width=True)  # Replace 'logo.png' with your main logo file



# Dropdown to select comparison type
comparison_type = st.selectbox("Select Comparison Type", ["None", "Single Month", "Comparative Analysis"])

if comparison_type == "Single Month":
    # Dropdown to select a month
    selected_month = st.selectbox("Select a Month", df['Month'].unique())

    # Dropdown to select a category with an option for "All"
    categories = ['All'] + df['Category'].unique().tolist()
    selected_category = st.selectbox("Select a Category", categories)

    # Filter the dataset by the selected month and category
    if selected_category == 'All':
        filtered_df = df[df['Month'] == selected_month]
    else:
        filtered_df = df[(df['Month'] == selected_month) & (df['Category'] == selected_category)]

    # Streamlit Dashboard for Single Month
    st.subheader(f"Trends for {selected_month} - {selected_category}")

    # Set the style for the plots
    sns.set(style="whitegrid")

    # Define a custom sky blue color palette
    custom_palette = sns.color_palette(["skyblue", "lightblue", "deepskyblue", "dodgerblue"])

    # Create a 2x2 grid for the plots
    fig, axes = plt.subplots(2, 2, figsize=(18, 12), constrained_layout=True)  # Make the platform wide

    # Plot 1: Count of stories per category
    category_count = filtered_df['Category'].value_counts()
    sns.barplot(x=category_count.index, y=category_count.values, ax=axes[0, 0], palette=custom_palette)
    axes[0, 0].set_xlabel('Category', fontsize=12)
    axes[0, 0].set_ylabel('Number of Stories', fontsize=12)
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].set_title('Number of Stories by Category', fontsize=14, loc='center')

    # Plot 2: Tonality distribution
    tonality_count = filtered_df['Tonality'].value_counts()
    tonality_colors = sns.color_palette("pastel")[0:len(tonality_count)]
    axes[0, 1].pie(tonality_count, labels=tonality_count.index, autopct='%1.1f%%', colors=tonality_colors, startangle=90, wedgeprops=dict(width=0.4))
    axes[0, 1].set(aspect='equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    axes[0, 1].set_title('Tonality Distribution', fontsize=14, loc='center')

    # Plot 3: Media Type Distribution
    media_type_count = filtered_df['Media Type'].value_counts()
    sns.barplot(x=media_type_count.index, y=media_type_count.values, ax=axes[1, 0], palette=custom_palette)
    axes[1, 0].set_xlabel('Media Type', fontsize=12)
    axes[1, 0].set_ylabel('Number of Stories', fontsize=12)
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].set_title('Media Type Distribution', fontsize=14, loc='center')

    # Plot 4: Top 10 Themes
    top_themes = filtered_df['Theme'].value_counts().head(10)
    sns.barplot(x=top_themes.values, y=top_themes.index, ax=axes[1, 1], palette=custom_palette)
    axes[1, 1].set_xlabel('Number of Stories', fontsize=12)
    axes[1, 1].set_ylabel('Theme', fontsize=12)
    axes[1, 1].set_title('Top 10 Themes', fontsize=14, loc='center')

    # Adjust layout and show the plots
    st.pyplot(fig)

elif comparison_type == "Comparative Analysis":
    # Dropdowns to select two months for comparison
    month1 = st.selectbox("Select First Month", df['Month'].unique())
    month2 = st.selectbox("Select Second Month", df['Month'].unique())

    # Filter the dataset by the selected months
    df_month1 = df[df['Month'] == month1]
    df_month2 = df[df['Month'] == month2]

    # Streamlit Dashboard for Comparative Analysis
    st.subheader(f"Comparing {month1} and {month2}")

    # Set the style for the plots
    sns.set(style="whitegrid")

    # Define a custom sky blue color palette
    custom_palette = sns.color_palette(["skyblue", "lightblue", "deepskyblue", "dodgerblue"])

    # Create a 2x2 grid for the plots
    fig, axes = plt.subplots(2, 2, figsize=(18, 12), constrained_layout=True)  # Make the platform wide

    # Plot 1: Count of stories per category for both months
    category_count1 = df_month1['Category'].value_counts()
    category_count2 = df_month2['Category'].value_counts()
    category_counts = pd.DataFrame({
        month1: category_count1,
        month2: category_count2
    }).fillna(0)
    category_counts.plot(kind='bar', ax=axes[0, 0], color=['skyblue', 'lightblue'])
    axes[0, 0].set_xlabel('Category', fontsize=12)
    axes[0, 0].set_ylabel('Number of Stories', fontsize=12)
    axes[0, 0].set_title('Number of Stories by Category', fontsize=14, loc='center')

    # Plot 2: Tonality distribution for both months
    tonality_count1 = df_month1['Tonality'].value_counts()
    tonality_count2 = df_month2['Tonality'].value_counts()
    tonality_counts = pd.DataFrame({
        month1: tonality_count1,
        month2: tonality_count2
    }).fillna(0)
    tonality_counts.plot(kind='bar', ax=axes[0, 1], color=['skyblue', 'lightblue'])
    axes[0, 1].set_xlabel('Tonality', fontsize=12)
    axes[0, 1].set_ylabel('Number of Stories', fontsize=12)
    axes[0, 1].set_title('Tonality Distribution', fontsize=14, loc='center')

    # Plot 3: Media Type Distribution for both months
    media_type_count1 = df_month1['Media Type'].value_counts()
    media_type_count2 = df_month2['Media Type'].value_counts()
    media_type_counts = pd.DataFrame({
        month1: media_type_count1,
        month2: media_type_count2
    }).fillna(0)
    media_type_counts.plot(kind='bar', ax=axes[1, 0], color=['skyblue', 'lightblue'])
    axes[1, 0].set_xlabel('Media Type', fontsize=12)
    axes[1, 0].set_ylabel('Number of Stories', fontsize=12)
    axes[1, 0].set_title('Media Type Distribution', fontsize=14, loc='center')

    # Plot 4: Top 10 Themes for both months
    top_themes1 = df_month1['Theme'].value_counts().head(10)
    top_themes2 = df_month2['Theme'].value_counts().head(10)
    top_themes = pd.DataFrame({
        month1: top_themes1,
        month2: top_themes2
    }).fillna(0)
    top_themes.plot(kind='barh', ax=axes[1, 1], color=['skyblue', 'lightblue'])
    axes[1, 1].set_xlabel('Number of Stories', fontsize=12)
    axes[1, 1].set_ylabel('Theme', fontsize=12)
    axes[1, 1].set_title('Top 10 Themes', fontsize=14, loc='center')

    # Adjust layout and show the plots
    st.pyplot(fig)
# Query Input
st.title("Farsight Media Analytics")
query = st.text_input("Enter your query", "")

# Process the query
if query.lower() == "highest number of stories":
    # Query: Highest number of stories
    highest_stories = df['Category'].value_counts().head(1)
    st.subheader("Category with Highest Number of Stories")
    st.write(highest_stories)

elif query.lower() == "top 10 tv stations":
    # Query: Top 10 TV Stations
    top_tv_stations = df[df['Media Type'] == 'TV']['Media Type'].value_counts().head(10)
    st.subheader("Top 10 TV Stations")
    st.write(top_tv_stations)

elif query.lower() == "top 10 radio stations":
    # Query: Top 10 Radio Stations
    top_radio_stations = df[df['Media Type'] == 'Radio']['Media Type'].value_counts().head(10)
    st.subheader("Top 10 Radio Stations")
    st.write(top_radio_stations)

elif query.lower() == "top 10 print media":
    # Query: Top 10 Print Media
    top_print_media = df[df['Media Type'] == 'Print']['Media Type'].value_counts().head(10)
    st.subheader("Top 10 Print Media")
    st.write(top_print_media)

elif query.lower() == "top 10 negative stories":
    # Query: Top 10 Negative Stories
    top_negative_stories = df[df['Tonality'] == 'Negative']['Tonality'].value_counts().head(10)
    st.subheader("Top 10 Negative Stories")
    st.write(top_negative_stories)

else:
    st.write("Please enter a valid query. For example: 'highest number of stories', 'top 10 TV stations', 'top 10 radio stations', 'top 10 print media', 'top 10 negative stories'.")


# Add the footer logo and trademark statement at the bottom
st.markdown("---")
col1, col2 = st.columns([4, 1])  # Adjust column width for footer logo and trademark statement
with col1:
    st.image('farsightlogo.png', use_column_width='auto', width=5)  # Replace 'farsightlogo.png' with your footer logo file and adjust width as needed
with col2:
    st.markdown("**A Product of Farsight Africa**", unsafe_allow_html=True)