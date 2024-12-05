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
  st.switch_page('pages/01_Post_Job_Opportunities.py')

if st.button('Accept and Receive Candidate Applications', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Candidate_Applications.py')

if st.button('Post Feedback for Co-ops', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_Post_Feedback_Coops.py')