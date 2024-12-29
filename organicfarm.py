#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from ipywidgets import interact

#######################
# Page configuration
st.set_page_config(
    page_title="Organic Agriculture in Ireland and the EU",
    
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


#######################
# Load data
df= pd.read_csv('streamlit.csv')


#######################
# Sidebar
with st.sidebar:
    st.title('Select Year')
    
    year_list = list(df['Year'].unique())
    
    selected_year = st.selectbox('Select a year', year_list)
    df_selected_year = df[df['Year'] == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################
# Plots

# Heatmap
ire_df = df[df['Country']=='Ireland']

# Function to plot trendline chart for the selected variable
def plot_trendline(variable):
    # Create the trendline chart
    fig = px.line(
        ire_df,
        x="Year",
        y=variable,
        title=f"{variable} in Ireland from 2013-2022",
        labels={"Year": "Year", variable: variable},
        height=600
    )
    
    fig.update_traces(mode="lines+markers")  # Add markers to the lines for clarity
    fig.show()

# Interactive widget to select the variable
interact(
    plot_trendline,
    variable=[col for col in ire_df.columns[2:]]);


# Create a choropleth map
fig = px.choropleth(
    df,
    locations='Country', 
    animation_frame="Year",
    locationmode='country names',
    color='%_area_under_organic_farming',
    hover_name='Country',
    title='Cluster Distribution of Organic Farming Indices (2022)',
    color_continuous_scale='viridis'
)
fig.update_layout(
    title_text="% UAA under organic agriculture 2013-2022",
    geo_scope="europe")
fig.show()


