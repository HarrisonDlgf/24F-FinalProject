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

# Create filters
col1, col2 = st.columns(2)

with col1:
    try:
        response = requests.get('http://api:4000/positions')
        
        if response.status_code == 200:
            positions = response.json()
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
        else:
            st.error(f"Failed to fetch positions data. Status code: {response.status_code}")
            st.write("Response content:", response.text)
    except Exception as e:
        st.error(f"Error accessing API: {str(e)}")
        st.write("Full error details:", e.__class__.__name__)

with col2:
    status_options = ['UNDER REVIEW', 'ACCEPTED', 'REJECTED']
    selected_status = st.selectbox('Filter by Status', status_options)

try:
    if selected_status == 'UNDER REVIEW':
        response = requests.get('http://api:4000/applications/under_review')
        applications = response.json() if response.status_code == 200 else []
    elif selected_status != 'All Statuses':
        response = requests.get(f'http://api:4000/applications/{selected_status}')
        applications = response.json() if response.status_code == 200 else []
    else:
        applications = []
        for position in positions:
            response = requests.get(f'http://api:4000/applications/{position["JobID"]}')
            if response.status_code == 200:
                applications.extend(response.json())

    if applications:
        df = pd.DataFrame(applications)
        
        if selected_type != 'All Types':
            position_ids = [pos['JobID'] for pos in positions if pos.get('PositionType') == selected_type]
            df = df[df['JobID'].isin(position_ids)]

        metric1, metric2, metric3 = st.columns(3)
        with metric1:
            st.metric("Total Applications", len(df))
        with metric2:
            status_counts = df['Status'].value_counts()
            under_review = status_counts.get('UNDER REVIEW', 0)
            st.metric("Under Review", under_review)
        with metric3:
            accepted = status_counts.get('ACCEPTED', 0)
            st.metric("Accepted", accepted)

        st.subheader("Application Status Distribution")
        st.bar_chart(df['Status'].value_counts())

        st.subheader("Application Details")
        st.dataframe(
            df[['ApplicationID', 'StudentID', 'JobID', 'SubmissionDate', 'Status']],
            use_container_width=True
        )

        if st.button("Update Selected to ACCEPTED"):
            selected_rows = st.multiselect("Select Applications", df['ApplicationID'].tolist())
            for app_id in selected_rows:
                response = requests.post(
                    f'http://api:4000/applications/ACCEPTED',
                    json={'application_id': app_id}
                )
                if response.status_code == 200:
                    st.success(f"Application {app_id} updated successfully!")
                else:
                    st.error(f"Failed to update application {app_id}")

        if st.button("Reject Selected Applications"):
            selected_rows = st.multiselect("Select Applications to Reject", df['ApplicationID'].tolist())
            for app_id in selected_rows:
                response = requests.put(f'http://api:4000/applications/REJECTED/{app_id}')
                if response.status_code == 200:
                    st.success(f"Application {app_id} rejected successfully!")
                else:
                    st.error(f"Failed to reject application {app_id}")

except Exception as e:
    st.error(f"Error fetching application data: {str(e)}")
    logger.error("Error getting data from API")
