import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Startup Founder, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Post Job Opportunities', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/startup_manage_jobs.py')

if st.button('Accept and Receive Candidate Applications', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/startup_manage_applications.py')

if st.button('Post Feedback for Co-ops', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/startup_post_feedback.py')
