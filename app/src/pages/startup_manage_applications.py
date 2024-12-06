import streamlit as st
import requests
import pandas as pd

# Set up the page
st.set_page_config(layout="wide")
st.title("Candidate Applications Management")

# Tabs for different functionalities
tab1, tab2 = st.tabs(["Submit Applications", "Manage Applications"])

# --- Tab 1: Submit Applications ---
with tab1:
    st.header("Submit Applications")
    with st.form(key="submit_application_form"):
        job_id = st.number_input("Job ID", min_value=1, step=1)
        student_id = st.text_input("Student ID", placeholder="Enter the student ID")
        submission_date = st.date_input("Submission Date")
        submit_button = st.form_submit_button(label="Submit Application")

    if submit_button:
        if not job_id or not student_id or not submission_date:
            st.error("Please fill in all required fields.")
        else:
            application_data = {
                "student_id": student_id,
                "submission_date": str(submission_date)
            }
            try:
                response = requests.post(
                    f"http://localhost:4000/applications/{job_id}", json=application_data
                )
                if response.status_code == 200:
                    st.success(f"Application for Job ID {job_id} submitted successfully!")
                else:
                    st.error(f"Failed to submit application. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")

# --- Tab 2: Manage Applications ---
with tab2:
    st.header("Manage Applications")

    # Choose an action
    action = st.selectbox(
        "Select an action:",
        [
            "View Applications by Job ID",
            "Delete an Application",
            "View Under Review Applications",
            "View Applications by Status",
            "Update Application Status",
            "Reject an Application"
        ]
    )

    # View applications by Job ID
    if action == "View Applications by Job ID":
        job_id = st.number_input("Enter Job ID:", min_value=1, step=1)
        if st.button("Fetch Applications"):
            try:
                response = requests.get(f"http://localhost:4000/applications/{job_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        df = pd.DataFrame(data)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No applications found for this Job ID.")
                else:
                    st.error(f"Failed to fetch applications. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data: {e}")

    # Delete an application
    if action == "Delete an Application":
        job_id = st.number_input("Enter Job ID:", min_value=1, step=1)
        student_id = st.text_input("Enter Student ID:")
        if st.button("Delete Application"):
            if not job_id or not student_id:
                st.error("Please provide both Job ID and Student ID.")
            else:
                try:
                    response = requests.delete(
                        f"http://localhost:4000/applications/{job_id}",
                        json={"student_id": student_id}
                    )
                    if response.status_code == 200:
                        st.success(f"Application for Job ID {job_id} deleted successfully.")
                    else:
                        st.error(f"Failed to delete application. Error: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")

    # View under review applications
    if action == "View Under Review Applications":
        if st.button("Fetch Under Review Applications"):
            try:
                response = requests.get("http://localhost:4000/applications/under_review")
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        df = pd.DataFrame(data)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No applications are currently under review.")
                else:
                    st.error(f"Failed to fetch applications. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data: {e}")

    # View applications by status
    if action == "View Applications by Status":
        status = st.selectbox("Select Status:", ["UNDER REVIEW", "ACCEPTED", "REJECTED"])
        if st.button("Fetch Applications by Status"):
            try:
                response = requests.get(f"http://localhost:4000/applications/{status}")
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        df = pd.DataFrame(data)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info(f"No applications with status '{status}' found.")
                else:
                    st.error(f"Failed to fetch applications. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data: {e}")

    # Update application status
    if action == "Update Application Status":
        application_id = st.number_input("Application ID", min_value=1, step=1)
        status = st.selectbox("New Status:", ["UNDER REVIEW", "ACCEPTED", "REJECTED"])
        if st.button("Update Status"):
            if not application_id or not status:
                st.error("Please provide both Application ID and new status.")
            else:
                try:
                    response = requests.post(
                        f"http://localhost:4000/applications/{status}",
                        json={"application_id": application_id}
                    )
                    if response.status_code == 200:
                        st.success(f"Application {application_id} status updated to '{status}'.")
                    else:
                        st.error(f"Failed to update status. Error: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")

    # Reject an application
    if action == "Reject an Application":
        application_id = st.number_input("Enter Application ID to reject:", min_value=1, step=1)
        if st.button("Reject Application"):
            if not application_id:
                st.error("Please provide an Application ID.")
            else:
                try:
                    response = requests.put(f"http://localhost:4000/applications/reject/{application_id}")
                    if response.status_code == 200:
                        st.success(f"Application {application_id} has been rejected.")
                    else:
                        st.error(f"Failed to reject application. Error: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
