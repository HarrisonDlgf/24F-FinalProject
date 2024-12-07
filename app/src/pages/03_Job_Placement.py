import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Job Application Dashboard')

# Add a test button and response display
if st.button("Test API Connection"):
    try:
        response = requests.get('http://api:4000/positions')
        if response.status_code == 200:
            st.success("API Connection Successful!")
            st.json(response.json())
        else:
            st.error(f"API returned status code: {response.status_code}")
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")

# Move positions fetching outside of columns to make it accessible throughout
try:
    response = requests.get('http://api:4000/positions')
    if response.status_code == 200:
        positions = response.json()
    else:
        st.error(f"Failed to fetch positions data. Status code: {response.status_code}")
        positions = []
except Exception as e:
    st.error(f"Error accessing API: {str(e)}")
    positions = []

col1, col2 = st.columns(2)

with col1:
    position_types = set(pos.get('PositionType', '') for pos in positions if pos.get('PositionType'))
    selected_type = st.selectbox('Filter by Position Type', ['All Types'] + list(position_types))
    
    st.subheader("Available Positions")
    filtered_positions = positions
    if selected_type != 'All Types':
        filtered_positions = [pos for pos in positions if pos.get('PositionType') == selected_type]
    
    if filtered_positions:
        df = pd.DataFrame(filtered_positions)
        display_columns = ['PositionTitle', 'Location', 'SalaryRange', 'PositionType']
        st.dataframe(df[display_columns], use_container_width=True)
    else:
        st.info("No positions found matching the selected criteria.")

with col2:
    st.subheader("Search Applications by Job ID")
    
    # Add a search box for JobID
    job_id_search = st.text_input("Enter Job ID", key="job_id_search")
    
    if job_id_search:  
        try:
            response = requests.get(f'http://api:4000/applications/job/{job_id_search}')
            if response.status_code == 200:
                applications = response.json()
                if applications:
                    df = pd.DataFrame(applications)
                    st.dataframe(df, use_container_width=True)
                    
                    # Add delete button for this application
                    if st.button("Delete All Applications For This Job", key=f"delete_{job_id_search}"):
                        delete_response = requests.delete(f'http://api:4000/applications/job/{job_id_search}')
                        if delete_response.status_code == 200:
                            st.success("Application deleted successfully!")
                            st.rerun()  # Refresh the page
                        else:
                            st.error(f"Failed to delete application. Status code: {delete_response.status_code}")
                else:
                    st.info(f"No applications found for Job ID: {job_id_search}")
            else:
                st.error(f"Failed to fetch applications. Status code: {response.status_code}")
                
        except Exception as e:
            st.error(f"Error fetching application data: {str(e)}")
            logger.error(f"Error getting data from API: {str(e)}")
