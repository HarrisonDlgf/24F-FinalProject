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
            }
    except Exception as e:
        st.error(f"Error loading filter options: {str(e)}")
        return {
            "Location": [],
            "Industry": [],
            "PositionType": [],
            "ExperienceRequired": [],
            "Skills": [],
            "SalaryRange": [],
        }

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
    }

def load_positions(filters=None):
    try:
        # Create params dict for the request
        params = {}
        if filters:
            for key, value in filters.items():
                if value and value.strip():  # Only add non-empty values
                    params[key] = value.strip()
        
        response = requests.get(f"{API_BASE_URL}/positions", params=params)
            
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error loading positions: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")
        return []

# Load initial positions or filtered positions
active_filters = {k: v for k, v in filters.items() if v and v.strip()}  # Only keep non-empty filters

if st.sidebar.button("Apply Filters"):
    # Load filtered positions
    positions = load_positions(active_filters)
    
    # Display filtered positions
    if positions:
        matching_positions = [p for p in positions if all(p[k].lower() == v.lower() for k, v in active_filters.items())]
        st.header(f"Available Positions ({len(matching_positions)} matches)")
        for position in positions:
            # Only display positions that match ALL filters
            should_display = True
            for filter_key, filter_value in active_filters.items():
                if position[filter_key].lower() != filter_value.lower():
                    should_display = False
                    break
            
            if should_display:
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(
                        f"📋 {position['PositionTitle']}\n"
                        f"📍 {position['Location']}",
                        key=f"pos_{position['JobID']}"
                    ):
                        st.session_state.selected_position_id = position['JobID']
                        st.switch_page("pages/02_Position_Detail.py")
                
                with col2:
                    try:
                        posted_date = datetime.strptime(position['StartDate'], '%a, %d %b %Y %H:%M:%S GMT')
                        st.write(f"Posted: {posted_date.strftime('%Y-%m-%d')}")
                    except Exception as e:
                        st.write("Date not available")
                st.markdown("---")
    else:
        st.header("Available Positions")
        st.info("No positions found matching your criteria.")
else:
    # Show all positions when no filters are applied
    positions = load_positions()
    st.header("Available Positions")
    if positions:
        for position in positions:
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(
                    f"📋 {position['PositionTitle']}\n"
                    f"📍 {position['Location']}",
                    key=f"pos_{position['JobID']}"
                ):
                    st.session_state.selected_position_id = position['JobID']
                    st.switch_page("pages/02_Position_Detail.py")
            
            with col2:
                try:
                    posted_date = datetime.strptime(position['StartDate'], '%a, %d %b %Y %H:%M:%S GMT')
                    st.write(f"Posted: {posted_date.strftime('%Y-%m-%d')}")
                except Exception as e:
                    st.write("Date not available")
            st.markdown("---")