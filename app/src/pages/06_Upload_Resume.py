import requests
import streamlit as st

def upload_resume():
    st.title("Upload Resume")

    # Upload file input
    resume_file = st.file_uploader("Upload your resume (PDF or DOCX only):", type=["pdf", "docx"])

    # Collect additional details if necessary (optional)
    user_id = st.text_input("Enter your User ID:", "")
    additional_notes = st.text_area("Additional notes (optional):")

    # Submit button
    if st.button("Submit"):
        # Validate input
        if not resume_file:
            st.error("Please upload a file before submitting.")
            return

        if not user_id.strip():
            st.error("User ID is required.")
            return

        # Prepare the request payload
        files = {"resume": resume_file.getvalue()}
        data = {"user_id": user_id, "notes": additional_notes}

        # Make POST request to backend
        url = "http://localhost:4000/api/upload_resume"
        try:
            response = requests.post(url, files={"file": resume_file}, data=data, timeout=10)
            if response.status_code == 201:
                st.success("Resume uploaded successfully!")
            else:
                st.error(f"Failed to upload resume. Server responded with: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    upload_resume()