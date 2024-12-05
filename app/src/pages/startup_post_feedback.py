import streamlit as st
import requests
import pandas as pd

# Set up the page
st.set_page_config(layout="wide")
st.title("Coop Feedback Management")

# Tabs for different functionalities
tab1, tab2 = st.tabs(["Post Feedback", "Manage Feedback"])

# --- Tab 1: Post Feedback ---
with tab1:
    st.header("Post Feedback")

    # Post feedback for a specific job
    st.subheader("Post Feedback for a Job")
    with st.form(key="post_feedback_form"):
        job_id = st.number_input("Job ID", min_value=1, step=1)
        ratings = st.slider("Ratings (1-5)", min_value=1, max_value=5)
        comments = st.text_area("Comments")
        submitted_by = st.text_input("Submitted By")
        submitted_for = st.text_input("Submitted For")
        submit_job_feedback = st.form_submit_button("Submit Feedback")

    if submit_job_feedback:
        if not (job_id and ratings and submitted_by and submitted_for):
            st.error("Please complete all required fields.")
        else:
            feedback_data = {
                "Ratings": ratings,
                "Comments": comments,
                "SubmittedBy": submitted_by,
                "SubmittedFor": submitted_for,
                "JobID": job_id
            }
            try:
                response = requests.post("http://api:4000/feedback", json=feedback_data)
                if response.status_code == 201:
                    st.success("Feedback submitted successfully!")
                else:
                    st.error(f"Failed to submit feedback. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")

    st.markdown("---")

    # Post feedback for a specific student
    st.subheader("Post Feedback for a Student")
    with st.form(key="post_feedback_student_form"):
        ratings = st.slider("Ratings (1-5)", min_value=1, max_value=5)
        comments = st.text_area("Comments")
        submitted_by = st.text_input("Submitted By")
        submitted_for = st.text_input("Submitted For (Student ID)")
        submit_student_feedback = st.form_submit_button("Submit Feedback")

    if submit_student_feedback:
        if not (ratings and submitted_by and submitted_for):
            st.error("Please complete all required fields.")
        else:
            feedback_data = {
                "Ratings": ratings,
                "Comments": comments,
                "SubmittedBy": submitted_by,
                "SubmittedFor": submitted_for
            }
            try:
                response = requests.post(
                    "http://api:4000/feedback/student", json=feedback_data
                )
                if response.status_code == 201:
                    st.success("Feedback submitted successfully!")
                else:
                    st.error(f"Failed to submit feedback. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")

# --- Tab 2: Manage Feedback ---
with tab2:
    st.header("Manage Feedback")

    # Select an action
    action = st.selectbox(
        "Select an action:",
        [
            "View Feedback by Job ID",
            "View Feedback by Student ID",
            "Edit Feedback",
            "Delete Feedback"
        ]
    )

    # View feedback by Job ID
    if action == "View Feedback by Job ID":
        job_id = st.number_input("Enter Job ID:", min_value=1, step=1)
        if st.button("Fetch Feedback"):
            try:
                response = requests.get(f"http://api:4000/feedback/{job_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        df = pd.DataFrame(data, columns=["Ratings", "Comments", "SubmittedBy", "SubmittedFor", "JobID", "FeedbackID"])
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No feedback found for this Job ID.")
                else:
                    st.error(f"Failed to fetch feedback. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data: {e}")

    # View feedback by Student ID
    if action == "View Feedback by Student ID":
        student_id = st.text_input("Enter Student ID:")
        if st.button("Fetch Feedback for Student"):
            try:
                response = requests.get(f"http://api:4000/feedback/student/{student_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        df = pd.DataFrame(data, columns=["Ratings", "Comments", "SubmittedBy", "SubmittedFor", "JobID", "FeedbackID"])
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No feedback found for this student.")
                else:
                    st.error(f"Failed to fetch feedback. Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data: {e}")

    # Edit feedback
    if action == "Edit Feedback":
        job_id = st.number_input("Enter Job ID to edit feedback:", min_value=1, step=1)
        new_ratings = st.slider("New Ratings (1-5)", min_value=1, max_value=5, value=None)
        new_comments = st.text_area("New Comments", value="")
        if st.button("Update Feedback"):
            if not (job_id and (new_ratings or new_comments)):
                st.error("Provide the Job ID and at least one field to update.")
            else:
                feedback_update = {
                    "Ratings": new_ratings if new_ratings else None,
                    "Comments": new_comments if new_comments else None
                }
                try:
                    response = requests.put(f"http://api:4000/feedback/{job_id}", json=feedback_update)
                    if response.status_code == 200:
                        st.success("Feedback updated successfully!")
                    else:
                        st.error(f"Failed to update feedback. Error: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error updating feedback: {e}")

    # Delete feedback
    if action == "Delete Feedback":
        feedback_id = st.number_input("Enter Feedback ID to delete:", min_value=1, step=1)
        if st.button("Delete Feedback"):
            if not feedback_id:
                st.error("Provide a Feedback ID to delete.")
            else:
                try:
                    response = requests.delete(f"http://api:4000/feedback/{feedback_id}")
                    if response.status_code == 200:
                        st.success("Feedback deleted successfully!")
                    else:
                        st.error(f"Failed to delete feedback. Error: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error deleting feedback: {e}")
