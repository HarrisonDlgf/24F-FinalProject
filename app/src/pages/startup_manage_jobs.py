import streamlit as st
import requests
import pandas as pd

# Set up the page
st.set_page_config(layout='wide')
st.title("Manage Job Opportunities and Work Experiences")

# Tabs for different functionalities
tab1, tab2 = st.tabs(["Post Job Opportunities", "Manage Work Experiences"])

# --- Tab 1: Post Job Opportunities ---
with tab1:
    st.header("Post Job Opportunities")
    with st.form(key='job_form'):
        # Job posting form
        job_title = st.text_input("Job Title", placeholder="Enter the job title", max_chars=100)
        company_name = st.text_input("Company Name", placeholder="Enter the company name")
        location = st.text_input("Location", placeholder="e.g., Boston, MA")
        industry = st.selectbox("Industry", options=[
            "Technology", "Healthcare", "Finance", "Education", "Retail", "Other"
        ])
        employment_type = st.selectbox("Employment Type", options=["Full-time", "Part-time", "Co-op", "Internship"])
        salary_range = st.text_input("Salary Range", placeholder="e.g., $50k-$70k")
        job_description = st.text_area("Job Description", placeholder="Provide a detailed job description")
        application_deadline = st.date_input("Application Deadline")
        submit_button = st.form_submit_button(label="Post Job")

    if submit_button:
        # Validate inputs
        if not job_title or not company_name or not location or not job_description:
            st.error("Please fill in all required fields.")
        else:
            # Prepare payload for API
            job_data = {
                "JobTitle": job_title,
                "CompanyName": company_name,
                "Location": location,
                "Industry": industry,
                "EmploymentType": employment_type,
                "SalaryRange": salary_range,
                "JobDescription": job_description,
                "ApplicationDeadline": str(application_deadline),
            }

            # Send POST request to API
            try:
                response = requests.post("http://api:4000/jobs", json=job_data)
                if response.status_code == 201:
                    st.success("Job opportunity posted successfully!")
                else:
                    st.error(f"Failed to post job. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while posting the job: {e}")

# --- Tab 2: Manage Work Experiences ---
with tab2:
    st.header("Manage Work Experiences")

    # Action options for work experiences
    action = st.selectbox(
        "Select an action:",
        ["View Work Experiences", "Add Work Experience", "Update Work Experience", "Delete Work Experience", "View Latest Work Experience"]
    )

    # View work experiences by StudentID
    if action == "View Work Experiences":
        student_id = st.text_input("Enter Student ID to view experiences:")
        if st.button("Fetch Work Experiences"):
            try:
                response = requests.get(f"http://api:4000/workexperiences/{student_id}")
                if response.status_code == 200:
                    data = response.json()
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data: {e}")

    # Add a new work experience
    if action == "Add Work Experience":
        with st.form(key='add_work_form'):
            student_id = st.text_input("Student ID", placeholder="Enter Student ID")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            job_id = st.text_input("Job ID", placeholder="Enter Job ID")
            feedback = st.text_area("Feedback (optional)")
            submit_button = st.form_submit_button(label="Add Work Experience")

        if submit_button:
            work_data = {
                "StudentID": student_id,
                "StartDate": str(start_date),
                "EndDate": str(end_date),
                "JobID": job_id,
                "Feedback": feedback
            }
            try:
                response = requests.post("http://api:4000/workexperiences", json=work_data)
                if response.status_code == 201:
                    st.success("Work experience added successfully!")
                else:
                    st.error(f"Failed to add work experience. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")

    # Update an existing work experience
    if action == "Update Work Experience":
        job_id = st.text_input("Enter Job ID to update:")
        start_date = st.date_input("New Start Date (leave blank to skip)")
        end_date = st.date_input("New End Date (leave blank to skip)")
        feedback = st.text_area("New Feedback (leave blank to skip)")
        if st.button("Update Work Experience"):
            work_data = {
                "StartDate": str(start_date) if start_date else None,
                "EndDate": str(end_date) if end_date else None,
                "Feedback": feedback if feedback else None,
            }
            try:
                response = requests.put(f"http://api:4000/workexperiences/{job_id}", json=work_data)
                if response.status_code == 200:
                    st.success(f"Work experience {job_id} updated successfully!")
                else:
                    st.error(f"Failed to update work experience. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")

    # Delete a work experience
    if action == "Delete Work Experience":
        job_id = st.text_input("Enter Job ID to delete:")
        if st.button("Delete Work Experience"):
            try:
                response = requests.delete(f"http://api:4000/workexperiences/{job_id}")
                if response.status_code == 200:
                    st.success(f"Work experience {job_id} deleted successfully!")
                else:
                    st.error(f"Failed to delete work experience. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")

    # View the latest work experience for a StudentID
    if action == "View Latest Work Experience":
        student_id = st.text_input("Enter Student ID to fetch the latest experience:")
        if st.button("Fetch Latest Experience"):
            try:
                response = requests.get(f"http://api:4000/workexperiences/{student_id}/latest")
                if response.status_code == 200:
                    data = response.json()
                    st.json(data)
                else:
                    st.error(f"No recent experiences found for Student ID {student_id}.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data: {e}")
