import requests
import streamlit as st


def search_coop_opportunities():
    st.title("Search for Co-op Opportunities")

    # Input fields for user query
    keyword = st.text_input("Enter a keyword (e.g., 'Data Analyst')", "")
    location = st.text_input("Enter a location (e.g., 'Boston')", "")

    # Search button
    if st.button("Search"):
        # URL for the Flask API
        url = "http://localhost:4000/positions"

        # Query parameters
        params = {}
        if keyword:
            params["PositionTitle"] = keyword
        if location:
            params["Location"] = location

        # Make the GET request
        try:
            response = requests.get(url, params=params, timeout=10)  # 10-second timeout
            response.raise_for_status()  # Raise exception for HTTP errors

            # Parse and display results
            results = response.json()
            if results:
                st.write("### Results:")
                for result in results:
                    st.write(f"**Title:** {result.get('PositionTitle', 'N/A')}")
                    st.write(f"**Location:** {result.get('Location', 'N/A')}")
                    st.write(f"**Salary Range:** {result.get('SalaryRange', 'N/A')}")
                    st.write(f"**Type:** {result.get('PositionType', 'N/A')}")
                    st.write("---")
            else:
                st.warning("No results found. Please try with different filters.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except ValueError:
            st.error("Error parsing the response. Please check the server output.")


if __name__ == "__main__":
    search_coop_opportunities()