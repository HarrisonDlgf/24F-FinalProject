import streamlit as st
from modules.nav import SideBarLinks
import requests

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

if student_id:
    if message_type != "All":
        # Use the specific message type endpoint
        response = requests.get(f'http://localhost:4000/communicationHistory/{student_id}/type/{message_type}')
    else:
        # Get all messages for student
        response = requests.get(f'http://localhost:4000/communicationHistory/{student_id}')
    
    if response.status_code == 200:
        messages = response.json()
        
        # displays messages in sections
        for msg in messages:
            with st.expander(f"{msg['MessageType']} - {msg['Timestamp']}"):
                st.write(f"**Content:** {msg['MessageContent']}")
                
                # Option to delete message
                if st.button("Delete Message", key=f"delete_{msg['MessageID']}"):
                    delete_response = requests.delete(
                        f'http://localhost:4000/communicationHistory/{student_id}',
                        params={'message_id': msg['MessageID']}
                    )
                    if delete_response.status_code == 200:
                        st.success("Message deleted successfully")
                        st.rerun()

# Send new message section
st.divider()
st.subheader("Send New Message")

new_student_id = st.text_input("Student ID")
new_message_type = st.selectbox(
    "Message Type",
    ["Follow-up", "Inquiry", "Response", "Notification", "Feedback"]
)
message_content = st.text_area("Message Content")

if st.button("Send Message"):
    if new_student_id and message_content:
        response = requests.post(
            f'http://localhost:4000/communicationHistory/{new_student_id}',
            json={
                'message_type': new_message_type,
                'message_content': message_content
            }
        )
        if response.status_code == 201:
            st.success("Message sent successfully!")
            st.rerun()