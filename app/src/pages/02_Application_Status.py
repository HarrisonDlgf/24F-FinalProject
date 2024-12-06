import streamlit as st
import requests

API_BASE_URL = "http://localhost:4000"

st.title("Application Status")

STUDENT_ID = "7"  # Maddy's student ID

def get_student_applications(student_id):
    try:
        # Using the GET /applications endpoint with student_id filter
        response = requests.get(f"{API_BASE_URL}/applications/student/{student_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print(response.json())
            st.error(f"Error loading applications: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")
        return []

# Get Maddy's applications
applications = get_student_applications(STUDENT_ID)

if applications:
    for app in applications:
        with st.expander(f"{app['PositionTitle']} at {app['StartUpName']}"):
            col1, col2 = st.columns([2,1])
            with col1:
                st.write(f"**Application Date:** {app['ApplicationDate']}")
                st.write(f"**Position Type:** {app['PositionType']}")
                st.write(f"**Location:** {app['Location']}")
                st.write(f"**Status:** {app['Status']}")
            with col2:
                st.write(f"**Contact:** {app['ContactEmail']}")
                
                # Add a button to withdraw application if needed
                if st.button("Withdraw Application", key=f"withdraw_{app['ApplicationID']}"):
                    # Add withdrawal logic here if needed
                    pass
else:
    st.info("No applications found.")

# Add a back button
if st.button("← Back to Home"):
    st.switch_page("pages/00_FullTime_Student_Home.py") 