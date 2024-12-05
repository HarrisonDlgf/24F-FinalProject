import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Northeastern Career Center Staff, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Career Center Analytics', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_Career_Center_Analytics.py')

if st.button('Student Communications Dashboard', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_Career_Center_Comms.py')

if st.button('Job Placement Tracking', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_Job_Placement.py')