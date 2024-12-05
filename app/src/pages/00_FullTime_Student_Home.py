import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()


# Page Layout
st.title("Available Positions")

# Filters Section
st.sidebar.header("Filter Positions")

# Filter inputs
with st.sidebar:
    location = st.text_input("Location")
    industry = st.text_input("Industry")
    position_type = st.selectbox(
        "Position Type",
        options=["", "Full-time", "Part-time", "Internship"],
    )
    experience = st.text_input("Experience Required")
    skills = st.text_input("Skills")
    
    # Apply filters button
    if st.button("Apply Filters"):
        filters = {
            "Location": location,
            "Industry": industry,
            "PositionType": position_type,
            "ExperienceRequired": experience,
            "Skills": skills
        }
        positions = load_positions(filters)
    else:
        positions = load_positions()

# Main content area
if positions:
    for position in positions:
        with st.expander(f"{position['PositionTitle']} at {position['StartUpName']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Location:** {position['Location']}")
                st.write(f"**Industry:** {position['Industry']}")
                st.write(f"**Position Type:** {position['PositionType']}")
                st.write(f"**Experience Required:** {position['ExperienceRequired']}")
                st.write(f"**Skills Required:** {position['Skills']}")
                st.write(f"**Salary Range:** {position['SalaryRange']}")
                
            with col2:
                st.write(f"**Start Date:** {position['StartDate']}")
                if st.button("Apply Now", key=f"apply_{position['JobID']}"):
                    # Here you would implement the application logic
                    st.write("Application functionality to be implemented")
                    
                st.write(f"**Contact:** {position['ContactEmail']}")
else:
    st.info("No positions found matching your criteria.")

# Optional: Add a refresh button
if st.button("Refresh Positions"):
    st.experimental_rerun()

