import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Full-Time Student, {st.session_state['first_name']}.")

st.write('### What would you like to do today?')

# PAGES ARE TO BE MADE - JUST PLACEHOLDERS FOR NOW
if st.button('Track Application Status', type='primary', use_container_width=True):
    st.switch_page('pages/02_Application_Status.py')

if st.button('View Full-Time Job Opportunities', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_Position_List.py')

if st.button('Provide Feedback on Startups', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_Student_Feedback.py')

