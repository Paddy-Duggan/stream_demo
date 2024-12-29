#######################
# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
#######################



#######################
# Load data
df = pd.read_csv('streamlit.csv')

st.title('Organic Farming EU')
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
st.plotly_chart(fig)
