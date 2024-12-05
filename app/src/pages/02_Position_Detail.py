import streamlit as st
import requests
from datetime import datetime

# Configuration
API_BASE_URL = "http://api:4000"
st.set_page_config(layout="wide", page_title="Position Details")

# Check if position ID is in session state
if 'selected_position_id' not in st.session_state:
    st.error("No position selected. Please select a position from the list.")
    if st.button("Return to Position List"):
        st.switch_page("pages/01_Position_List.py")
    st.stop()

def load_position_details(job_id):
    try:
        response = requests.get(f"{API_BASE_URL}/positions/{job_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error loading position details: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")
        return None

def submit_application(job_id, student_id, resume_file):
    try:
        response = requests.post(
            f"{API_BASE_URL}/applications",
            data={
                'job_id': job_id,
                'student_id': student_id,
                'application_date': datetime.now().isoformat()
            },
            files={'resume': resume_file}
        )
        return response.status_code == 201
    except Exception as e:
        st.error(f"Error submitting application: {str(e)}")
        return False

# Load position details
position = load_position_details(st.session_state.selected_position_id)

if position:
    # Back button
    if st.button("← Back to Positions"):
        st.switch_page("pages/01_Position_List.py")
    
    # Position header
    st.title(position['PositionTitle'])
    st.subheader(f"{position['StartUpName']} • {position['Location']}")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Position Details")
        st.write(f"**Industry:** {position['Industry']}")
        st.write(f"**Position Type:** {position['PositionType']}")
        st.write(f"**Experience Required:** {position['ExperienceRequired']}")
        st.write(f"**Skills Required:** {position['Skills']}")
        st.write(f"**Salary Range:** {position['SalaryRange']}")
        st.write(f"**Start Date:** {position['StartDate']}")
        
        st.markdown("### Position Description")
        st.write(position.get('Description', 'No description available.'))
        
        st.markdown("### Required Qualifications")
        st.write(position.get('Qualifications', 'No qualifications listed.'))
    
    with col2:
        st.markdown("### Contact Information")
        st.write(f"**Email:** {position['ContactEmail']}")
        
        # Application form
        with st.form("application_form"):
            student_id = st.text_input("Student ID")
            uploaded_file = st.file_uploader(
                "Upload Resume (PDF)", 
                type=['pdf']
            )
            
            submitted = st.form_submit_button("Submit Application")
            if submitted:
                if not student_id or not uploaded_file:
                    st.error("Please fill in all required fields")
                else:
                    success = submit_application(
                        position['JobID'],
                        student_id,
                        uploaded_file
                    )
                    if success:
                        st.success("Application submitted successfully!")
        
        # Company info
        st.markdown("### Company Information")
        st.write(position.get('CompanyDescription', 'No company description available.'))
else:
    st.error("Position not found.")
    if st.button("Return to Position List"):
        st.switch_page("pages/01_Position_List.py") 