import streamlit as st
import requests
from datetime import datetime

# Configuration
API_BASE_URL = "http://api:3306"
st.set_page_config(layout="wide", page_title="Available Positions")

# Custom CSS for the position cards
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        text-align: left;
        height: auto;
        padding: 15px;
        background-color: white;
        margin: 5px 0;
    }
    div.stButton > button:hover {
        background-color: #f0f2f6;
        border-color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# Get unique values for each filter field
def get_filter_options():
    try:
        response = requests.get(f"{API_BASE_URL}/positions")
        if response.status_code == 200:
            positions = response.json()
            return {
                "Location": sorted(list(set(p["Location"] for p in positions))),
                "Industry": sorted(list(set(p["Industry"] for p in positions))),
                "PositionType": sorted(list(set(p["PositionType"] for p in positions))),
                "ExperienceRequired": sorted(list(set(p["ExperienceRequired"] for p in positions))),
                "Skills": sorted(list(set(p["Skills"] for p in positions))),
                "SalaryRange": sorted(list(set(p["SalaryRange"] for p in positions))),
                "StartUpName": sorted(list(set(p["StartUpName"] for p in positions)))
            }
    except Exception as e:
        st.error(f"Error loading filter options: {str(e)}")
        return {}

# Get filter options
filter_options = get_filter_options()

# Sidebar filters with dropdowns
with st.sidebar:
    st.header("Filter Positions")
    filters = {
        "Location": st.selectbox(
            "Location",
            options=[""] + filter_options.get("Location", []),
            key="location_filter"
        ),
        "Industry": st.selectbox(
            "Industry",
            options=[""] + filter_options.get("Industry", []),
            key="industry_filter"
        ),
        "PositionType": st.selectbox(
            "Position Type",
            options=[""] + filter_options.get("PositionType", []),
            key="position_type_filter"
        ),
        "ExperienceRequired": st.selectbox(
            "Experience Required",
            options=[""] + filter_options.get("ExperienceRequired", []),
            key="experience_filter"
        ),
        "Skills": st.selectbox(
            "Skills",
            options=[""] + filter_options.get("Skills", []),
            key="skills_filter"
        ),
        "SalaryRange": st.selectbox(
            "Salary Range",
            options=[""] + filter_options.get("SalaryRange", []),
            key="salary_filter"
        ),
        "StartUpName": st.selectbox(
            "StartUp Name",
            options=[""] + filter_options.get("StartUpName", []),
            key="startup_filter"
        )
    }

def load_positions(filters=None):
    try:
        response = requests.get(f"{API_BASE_URL}/positions", params=filters)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error loading positions: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")
        return []

# Load initial positions or filtered positions
if st.sidebar.button("Apply Filters"):
    positions = load_positions(filters)
else:
    positions = load_positions()

# Main content area
st.title("Available Positions")

# Display positions as clickable cards
if positions:
    for position in positions:
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(
                f"📋 {position['PositionTitle']}\n"
                f"🏢 {position['StartUpName']}\n"
                f"📍 {position['Location']}",
                key=f"pos_{position['JobID']}"
            ):
                st.session_state.selected_position_id = position['JobID']
                st.switch_page("pages/02_Position_Detail.py")
        
        with col2:
            st.write(f"Posted: {position['StartDate']}")
        st.markdown("---")
else:
    st.info("No positions found matching your criteria.") 