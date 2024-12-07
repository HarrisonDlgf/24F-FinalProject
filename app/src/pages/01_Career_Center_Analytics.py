import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Student Placement Analytics")

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["Placement Rates", "Industry Distribution", "Salary Trends"])

with tab1:
    st.header("Placement Success Rates")
    # Fetch placement data from API
    placement_data = {
        "Full-time": 85,
        "Co-op": 92,
        "Part-time": 78
    }
    
    # Create bar chart
    fig = px.bar(
        x=list(placement_data.keys()),
        y=list(placement_data.values()),
        labels={'x': 'Position Type', 'y': 'Placement Rate (%)'}
    )
    st.plotly_chart(fig)

with tab2:
    st.header("Industry Distribution")
    # Fetch industry data
    try:
        response = requests.get('http://api:4000/positions')
        positions = response.json()
        
        # Process data for visualization
        df = pd.DataFrame(positions)
        industry_counts = df['Industry'].value_counts()
        
        # Create pie chart
        fig = px.pie(values=industry_counts.values, names=industry_counts.index)
        st.plotly_chart(fig)
    except:
        # st.error("Unable to fetch industry data")
        st.error(response.json())

with tab3:
    st.header("Salary Range Distribution")
    # Add salary trend visualization
    salary_ranges = {
        "$40-60k": 25,
        "$60-80k": 40,
        "$80-100k": 20,
        "$100k+": 15
    }
    fig = px.bar(
        x=list(salary_ranges.keys()),
        y=list(salary_ranges.values()),
        labels={'x': 'Salary Range', 'y': 'Number of Positions'}
    )
    st.plotly_chart(fig)