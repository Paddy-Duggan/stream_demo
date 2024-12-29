# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Organic Agriculture in Ireland and the EU",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}
</style>
""", unsafe_allow_html=True)

# Load data with error handling
@st.cache
def load_data(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        st.error("File not found. Please make sure 'streamlit.csv' is in the app directory.")
        return pd.DataFrame()

df = load_data('streamlit.csv')

if not df.empty:
    # Sidebar
    with st.sidebar:
        st.title('Select Year')

        year_list = sorted(df['Year'].unique())
        selected_year = st.selectbox('Select a year', year_list)
        df_selected_year = df[df['Year'] == selected_year]

        color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

    # Main content
    st.title("Organic Agriculture Analysis")

    # Heatmap
    ire_df = df[df['Country'] == 'Ireland']

    # Trendline chart
    variable = st.selectbox("Select a variable for trendline", ire_df.columns[2:])
    if variable:
        fig_trendline = px.line(
            ire_df,
            x="Year",
            y=variable,
            title=f"{variable} in Ireland from 2013-2022",
            labels={"Year": "Year", variable: variable},
            height=600
        )
        fig_trendline.update_traces(mode="lines+markers")
        st.plotly_chart(fig_trendline)

    # Choropleth map
    st.subheader("Choropleth Map of Organic Farming in Europe")
    fig_map = px.choropleth(
        df,
        locations='Country',
        locationmode='country names',
        color='%_area_under_organic_farming',
        hover_name='Country',
        animation_frame="Year",
        title='Cluster Distribution of Organic Farming Indices (2022)',
        color_continuous_scale=selected_color_theme
    )
    fig_map.update_layout(geo_scope="europe")
    st.plotly_chart(fig_map)
