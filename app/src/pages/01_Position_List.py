import streamlit as st
import requests
from datetime import datetime

# Configuration
API_BASE_URL = "http://api:4000"
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

# Sidebar filters
with st.sidebar:
    st.header("Filter Positions")
    filters = {
        "PositionTitle": st.text_input("Position Title"),
        "StartUpName": st.text_input("StartUp Name"),
        "Location": st.text_input("Location"),
        "Industry": st.text_input("Industry"),
        "PositionType": st.selectbox(
            "Position Type",
            options=["", "Full-time", "Part-time", "Internship"]
        ),
        "ExperienceRequired": st.text_input("Experience Required"),
        "Skills": st.text_input("Skills"),
        "SalaryRange": st.text_input("Salary Range")
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