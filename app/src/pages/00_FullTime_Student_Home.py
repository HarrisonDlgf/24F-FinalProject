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
if st.button('View Available Positions', type='primary', use_container_width=True):
    st.switch_page('pages/01_Available_Positions.py')

if st.button('Track Application Status', type='primary', use_container_width=True):
    st.switch_page('pages/02_Application_Status.py')

if st.button('Access Career Resources', type='primary', use_container_width=True):
    st.switch_page('pages/03_Career_Resources.py')

