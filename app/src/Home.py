##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('Welcome to StartUpConnect! A platform for connecting startups with Northeastern University.')
st.write('\n\n')
st.write('### Which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

# Jeff, Second Year Undergraduate student searching for a startup to join
if st.button("Act as Jeff, a Second Year searching for a startup to join", 
            type = 'primary', 
            use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'second_year_undergraduate'
    # we add the first name of the user (so it can be displayed on 
    # subsequent pages). 
    st.session_state['first_name'] = 'Jeff'
    # finally, we ask streamlit to switch to another page, in this case, the 
    # landing page for this particular user type
    logger.info("Logging in as Jeff, a Second Year Undergraduate searching for a startup to join")
    st.switch_page('pages/00_CoOp_Student_Home.py')

# Maddy, senior at NEU searching for a full-time job
if st.button('Act as Maddy, a senior at NEU searching for a full-time job', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'senior'
    st.session_state['first_name'] = 'Maddy'
    st.switch_page('pages/00_FullTime_Student_Home.py')

# David, works at Northeastern University’s Career Center
if st.button('Act as David, a Career Center staff member evaluating internship and job placement success', 
            type='primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'career_center_staff'
    st.session_state['first_name'] = 'David'
    st.switch_page('pages/00_Career_Center_Home.py')

# Alex, runs a small tech startup focused on AI-driven healthcare solutions
if st.button('Act as Alex, a startup founder looking to hire interns for AI-driven healthcare projects', 
            type='primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'startup_founder'
    st.session_state['first_name'] = 'Alex'
    st.switch_page('pages/00_Startup_Founder_Home.py')




