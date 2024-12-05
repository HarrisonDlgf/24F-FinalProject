import streamlit as st
import requests
from datetime import datetime

# Configuration
st.set_page_config(layout="wide", page_title="Position Details")

# Check if position ID is in session state
if 'selected_position_id' not in st.session_state:
    st.error("No position selected. Please select a position from the list.")
    st.stop()

def load_position_details(job_id):
    try:
        response = requests.get(f"{API_BASE_URL}/positions/{job_id}")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error loading position details: {str(e)}")
        return None

def submit_application(job_id, student_id, file_content):
    try:
        files = {'resume': file_content}
        data = {
            'job_id': job_id,
            'student_id': student_id,
            'application_date': datetime.now().isoformat()
        }
        response = requests.post(f"{API_BASE_URL}/applications", data=data, files=files)
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
    st.subheader(position['StartUpName'])
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Position Details")
        st.write(f"**Industry:** {position['Industry']}")
        st.write(f"**Location:** {position['Location']}")
        st.write(f"**Position Type:** {position['PositionType']}")
        st.write(f"**Experience Required:** {position['ExperienceRequired']}")
        st.write(f"**Skills Required:** {position['Skills']}")
        st.write(f"**Salary Range:** {position['SalaryRange']}")
        
        st.markdown("### Position Description")
        st.write(position.get('Description', 'No description available.'))
        
        st.markdown("### Required Qualifications")
        st.write(position.get('Qualifications', 'No qualifications listed.'))
    
    with col2:
        st.markdown("### Application")
        st.write(f"**Start Date:** {position['StartDate']}")
        st.write(f"**Contact:** {position['ContactEmail']}")
        
        # Application form
        with st.form("application_form"):
            uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
            student_id = st.text_input("Student ID")
            
            submitted = st.form_submit_button("Submit Application")
            if submitted and uploaded_file and student_id:
                success = submit_application(
                    position['JobID'],
                    student_id,
                    uploaded_file
                )
                if success:
                    st.success("Application submitted successfully!")
                    # Optional: redirect back to position list
                    # st.switch_page("pages/01_Position_List.py")
        
        # Company info
        st.markdown("### Company Information")
        st.write(position.get('CompanyDescription', 'No company description available.'))
else:
    st.error("Position not found.") 