import streamlit as st
import requests
from datetime import datetime

# Configuration
API_BASE_URL = "http://api:4000"
st.set_page_config(layout="wide", page_title="Student Feedback")

def submit_feedback(feedback_data):
    try:
        response = requests.post(f"{API_BASE_URL}/feedback/feedback", json=feedback_data)
        return response.status_code == 201  # API returns 201 on success
    except Exception as e:
        st.error(f"Error submitting feedback: {str(e)}")
        return False

# Page header
st.header("Submit Feedback")

# Feedback form
with st.form("feedback_form"):
    # Hidden fields
    student_id = 7  # Maddy's StudentID
    
    # User input fields
    job_id = st.number_input("Job ID", min_value=1, help="Enter the Job ID for the position")
    rating = st.slider("Rating", min_value=1, max_value=5, value=3, help="Rate your experience (1-5)")
    comments = st.text_area("Comments", help="Share your feedback about the position")
    
    # Submit button
    submitted = st.form_submit_button("Submit Feedback")
    
    if submitted:
        if not comments:
            st.error("Please provide comments")
        else:
            feedback_data = {
                "Ratings": rating,  # Changed to match API expectation
                "Comments": comments,
                "SubmittedBy": str(student_id),  # Maddy's ID
                "SubmittedFor": "Company",  # Can be updated if needed
                "JobID": job_id
            }
            
            if submit_feedback(feedback_data):
                st.success("Feedback submitted successfully!")
            else:
                st.error("Failed to submit feedback. Please try again.") 