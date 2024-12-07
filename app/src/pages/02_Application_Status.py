import streamlit as st
import requests
from datetime import datetime

API_BASE_URL = "http://api:4000"

st.title("Application Status")

STUDENT_ID = 7  # Maddy's student ID

def get_student_applications(student_id):
    try:
        response = requests.get(f"{API_BASE_URL}/applications/student/{student_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error loading applications: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")
        return []

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')
        return date_obj.strftime('%Y-%m-%d')
    except:
        return date_str

# Get Maddy's applications
applications = get_student_applications(STUDENT_ID)

if applications:
    for app in applications:
        with st.expander(f"Application for: {app['PositionTitle']}"):
            col1, col2 = st.columns([2,1])
            with col1:
                st.write(f"**Application ID:** {app['ApplicationID']}")
                st.write(f"**Job ID:** {app['JobID']}")
                st.write(f"**Position Type:** {app['PositionType']}")
                st.write(f"**Location:** {app['Location']}")
                st.write(f"**Submission Date:** {format_date(app['SubmissionDate'])}")
            with col2:
                if st.button("View Position Details", key=f"view_{app['ApplicationID']}"):
                    st.session_state.selected_position_id = app['JobID']
                    st.switch_page("pages/02_Position_Detail.py")
else:
    st.info("No applications found for your account.")

# Back button to home page
if st.button("← Back to Home"):
    st.switch_page("Home.py") 