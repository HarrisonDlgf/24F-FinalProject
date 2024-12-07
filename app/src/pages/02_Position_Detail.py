import streamlit as st
import requests
from datetime import datetime

# Configuration
API_BASE_URL = "http://api:4000"
st.set_page_config(layout="wide", page_title="Position Details")

# Custom CSS for better styling
st.markdown("""
    <style>
    .position-header {
        margin-bottom: 2rem;
    }
    .section-header {
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Check if position ID is in session state
if 'selected_position_id' not in st.session_state:
    st.error("No position selected. Please select a position from the list.")
    if st.button("Return to Position List"):
        st.switch_page("pages/01_Position_List.py")
    st.stop()

def load_position_details(job_id):
    try:
        # First get the position details
        response = requests.get(f"{API_BASE_URL}/positions?JobID={job_id}")
        if response.status_code == 200:
            positions = response.json()
            if positions and len(positions) > 0:
                position = positions[0]
                
                # Then get the startup name using StartUpID
                startup_response = requests.get(f"{API_BASE_URL}/startups/{position['StartUpID']}")
                if startup_response.status_code == 200:
                    startup = startup_response.json()
                    position['CompanyName'] = startup.get('Name', 'Company')
                return position
            return None
        else:
            st.error(f"Error loading position details: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")
        return None

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')
        return date_obj.strftime('%Y-%m-%d')
    except:
        return date

# Load position details
position = load_position_details(st.session_state.selected_position_id)

if position:
    # Back button
    if st.button("← Back to Positions"):
        st.switch_page("pages/01_Position_List.py")
    
    # Position header with better styling
    st.markdown(f"""
        <div class="position-header">
            <h1>{position['PositionTitle']}</h1>
            <h3>{position['Location']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Position Details")
        # Clean up salary range before displaying
        salary_range = position['SalaryRange'].replace(',000', 'K')
        
        details = {
            "Industry": position['Industry'],
            "Position Type": position['PositionType'],
            "Experience Required": position['ExperienceRequired'],
            "Skills Required": position['Skills'],
            "Salary Range": salary_range,
            "Start Date": format_date(position['StartDate'])
        }
        
        for key, value in details.items():
            st.write(f"**{key}:** {value}")
    
    with col2:
        st.markdown("### 📧 Contact Information")
        st.write(f"**Email:** {position['ContactEmail']}")
        
        # Application form
        st.markdown("### 📤 Submit Application")
        with st.form("application_form"):
            student_id = st.text_input("Student ID")
            uploaded_file = st.file_uploader(
                "Upload Resume (PDF)", 
                type=['pdf'],
                help="Please upload your resume in PDF format"
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
else:
    st.error("Position not found.")
    if st.button("Return to Position List"):
        st.switch_page("pages/01_Position_List.py") 