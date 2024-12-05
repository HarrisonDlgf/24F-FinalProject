import requests
import streamlit as st

def search_coop_opportunities():
    st.title("Search for Co-op Opportunities")
    keyword = st.text_input("Enter a keyword:")
    location = st.text_input("Enter a location:")

    if st.button("Search"):
        params = {"keyword": keyword, "location": location}
        response = requests.get("http://localhost:5000/api/search_coop_opportunities", params=params)
        if response.status_code == 200:
            results = response.json()
            st.write("### Results:")
            for result in results:
                st.write(f"- {result['title']} at {result['company']}, {result['location']}")
        else:
            st.error("Error fetching results. Please try again.")

if __name__ == "__main__":
    search_coop_opportunities()