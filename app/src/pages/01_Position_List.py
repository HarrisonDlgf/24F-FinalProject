import streamlit as st
import requests
from datetime import datetime

# Configuration
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
    location = st.text_input("Location")
    industry = st.text_input("Industry")
    position_type = st.selectbox(
        "Position Type",
        options=["", "Full-time", "Part-time", "Internship"],
    )
    experience = st.text_input("Experience Required")
    skills = st.text_input("Skills")
    
    if st.button("Apply Filters"):
        filters = {
            "Location": location,
            "Industry": industry,
            "PositionType": position_type,
            "ExperienceRequired": experience,
            "Skills": skills
        }
        st.session_state.positions = load_positions(filters)

# Main content area
st.title("Available Positions")

def load_positions(filters=None):
    try:
        response = requests.get(f"{API_BASE_URL}/positions", params=filters)
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        st.error(f"Error loading positions: {str(e)}")
        return []

# Display positions as clickable cards
positions = load_positions()
for position in positions:
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button(
            f"📋 {position['PositionTitle']}\n"
            f"🏢 {position['StartUpName']}\n"
            f"📍 {position['Location']}",
            key=f"pos_{position['JobID']}"
        ):
            # Store position ID in session state and redirect
            st.session_state.selected_position_id = position['JobID']
            st.switch_page("pages/02_Position_Detail.py")
    
    with col2:
        st.write(f"Posted: {position['StartDate']}")
    st.markdown("---") 