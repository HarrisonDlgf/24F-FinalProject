import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Northeastern Co-op Student, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Upload Resume', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/06_Upload_Resume.py')

if st.button('Search for Co-op Opportunities', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/08_Search_Coop_Opportunities.py')

if st.button('Co-op Updates', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Coop_Updates.py')