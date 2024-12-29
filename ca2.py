#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################



#######################
# Load data
df = pd.read_csv('streamlit.csv')

st.title('Organic Farming EU')
