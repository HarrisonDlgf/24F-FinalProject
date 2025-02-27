import streamlit as st
from modules.nav import SideBarLinks
import requests
import time 

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Student Communications Dashboard")

# filters by message type and lets user select
message_type = st.selectbox(
    "Filter by Message Type",
    ["All", "Follow-up", "Inquiry", "Response", "Notification", "Feedback"]
)

# searching by id and input
student_id = st.text_input("Search by Student ID")
student_id_int = int(student_id) if student_id else None

if student_id:
    if message_type != "All":
        # Updated URL format
        response = requests.get(f'http://api:4000/communication-history/{student_id}/type/{message_type}')
    else:
        # Updated URL format
        response = requests.get(f'http://api:4000/communication-history/{student_id}')
    
    if response.status_code == 200:
        messages = response.json()
        
        # displays messages in sections
        for msg in messages:
            with st.expander(f"{msg['MessageType']} - {msg['Timestamp']}"):
                st.write(f"**Content:** {msg['MessageContent']}")
                
                # Option to delete message
                if st.button("Delete Message", key=f"delete_{msg['MessageID']}"):
                    # Updated URL format
                    delete_response = requests.delete(
                        f'http://api:4000/communication-history/{student_id}',
                        params={'message_id': msg['MessageID']}
                    )
                    if delete_response.status_code == 200:
                        st.success("Message deleted successfully")
                        st.rerun()

# Send new message section
st.divider()
st.subheader("Send New Message")

new_student_id = st.text_input("Student ID")
new_student_id_int = int(new_student_id) if new_student_id else None
new_message_type = st.selectbox(
    "Message Type",
    ["Follow-up", "Inquiry", "Response", "Notification", "Feedback"]
)
message_content = st.text_area("Message Content")

if st.button("Send Message"):
    if new_student_id_int and message_content:
        response = requests.post(
            f'http://api:4000/communication-history/{new_student_id_int}/send',
            json={
                'message_type': new_message_type,
                'message_content': message_content
            }
        )
        
        if response.status_code == 201:
            success_message = st.success(f"Message sent successfully to Student {new_student_id_int}!")
            # Clear the form
            st.text_input("Student ID", value="", key="clear_id")
            st.text_area("Message Content", value="", key="clear_content")
            time.sleep(2) 
            st.rerun()
        else:
            st.error(f"Failed to send message: {response.json().get('message', 'Unknown error')}")
    else:
        st.warning("Please enter both Student ID and Message Content")

# Add this temporarily to test the connection
if st.button("Test API Connection"):
    try:
        response = requests.get('http://api:4000/communication-history')
        st.write(f"Status: {response.status_code}")
        if response.status_code == 200:
            st.success("API Connection Successful!")
            st.json(response.json())
        else:
            st.error(f"API returned status code: {response.status_code}")
            st.write(f"Response Text: {response.text}")
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")