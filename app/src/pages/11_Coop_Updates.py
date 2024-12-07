import requests
import streamlit as st

def coop_updates():
    st.title("Update Your Co-op Information")


    coop_id = st.text_input("Enter your Co-op ID:", "")
    new_position_title = st.text_input("Enter a new Position Title (optional):", "")
    new_company_name = st.text_input("Enter a new Company Name (optional):", "")
    new_start_date = st.date_input("Enter a new Start Date (optional):")
    new_end_date = st.date_input("Enter a new End Date (optional):")

    # Submit button
    if st.button("Update Co-op"):

        if not coop_id.strip():
            st.error("Co-op ID is required.")
            return

        # Prepare the request payload
        updates = {}
        if new_position_title.strip():
            updates["PositionTitle"] = new_position_title
        if new_company_name.strip():
            updates["CompanyName"] = new_company_name
        if new_start_date:
            updates["StartDate"] = new_start_date.strftime("%Y-%m-%d")
        if new_end_date:
            updates["EndDate"] = new_end_date.strftime("%Y-%m-%d")

        # Make PUT request to the Flask API
        url = f"http://api:4000/api/WorkExperiences/{coop_id}"
        try:
            response = requests.put(url, json=updates, timeout=10)
            if response.status_code == 200:
                st.success("Co-op information updated successfully!")
            elif response.status_code == 404:
                st.error("Co-op ID not found.")
            else:
                st.error(f"Failed to update. Server responded with: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    coop_updates()