import pandas as pd
import plotly.express as px
import streamlit as st

# Streamlit page config (must be the first Streamlit call)
st.set_page_config(
    page_title="Spatial Visualization",
    layout="wide",  # <- This makes it use full width
    initial_sidebar_state="expanded"
)

# -----------------
# Load / prepare data
# -----------------
# Option 1: Load from repo
try:
    df = pd.read_csv("data/pageviews_year_percapita_continent.csv")
except FileNotFoundError:
    st.warning("Default CSV not found. Please upload your own file.")
    uploaded_file = st.file_uploader("Upload your CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.stop()

# Split country and year
df[['country', 'year']] = df['country_year'].str.rsplit(' ', n=1, expand=True)
df['year'] = df['year'].astype(int)

# Normalized metric
df['pageviews_per_1000'] = df['total_pageviews'] / (df['population'] / 1000)

# -----------------
# Streamlit layout
# -----------------
st.title("🌍 Choropleth Map of Pageviews & Population")
st.write("""
This map shows countries shaded by the selected metric, animated across years.
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
# Plotly choropleth
# -----------------

# --- NEW CODE START ---
global_max = (int(global_max / 100) + 1) * 100
# --- NEW CODE END ---


fig = px.choropleth(
    filtered_df,
    locations="country",
    locationmode="country names",
    color=metric,
    range_color=[0, global_max],
    animation_frame="year",
    hover_name="country",
    color_continuous_scale="Viridis",
    title=f"Choropleth Map of {metric.replace('_', ' ').title()}",
    height=700, width=1000
)

# Show borders
fig.update_geos(
    showcountries=True, countrycolor="black",
    showcoastlines=True, coastlinecolor="gray",
    showland=True, landcolor="lightgray"
)

st.plotly_chart(fig, use_container_width=True)
