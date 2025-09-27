import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------
# Load / prepare data
# -----------------
df = pd.read_csv("data/pageviews_year_percapita_continent.csv")

# Split country and year
df[['country', 'year']] = df['country_year'].str.rsplit(' ', n=1, expand=True)
df['year'] = df['year'].astype(int)

# Normalized metric
df['pageviews_per_1000'] = df['total_pageviews'] / (df['population'] / 1000)

# -----------------
# Streamlit layout
# -----------------
st.title("🌍 Animated Pageviews Time Map")

st.write("""
This interactive map lets you explore:
- **Population**
- **Total pageviews**
- **Pageviews per 1,000 people**
""")

# User controls
metric = st.selectbox(
    "Choose a metric:", 
    ["population", "total_pageviews", "pageviews_per_1000"]
)
regions = st.multiselect(
    "Filter by region:", 
    df["region"].unique(), 
    default=df["region"].unique()
)

filtered_df = df[df["region"].isin(regions)]

# -----------------
# Plotly animated map
# -----------------
fig = px.scatter_geo(
    filtered_df,
    locations="country",
    locationmode="country names",
    size=metric,
    color="region",
    animation_frame="year",
    hover_name="country",
    projection="natural earth",
    title=f"Animated Time Map of {metric.replace('_', ' ').title()}",
    height=700, width=1000
)

# Show borders + background
fig.update_geos(
    showcountries=True, countrycolor="black",
    showcoastlines=True, coastlinecolor="gray",
    showland=True, landcolor="lightgray"
)

st.plotly_chart(fig, use_container_width=True)
