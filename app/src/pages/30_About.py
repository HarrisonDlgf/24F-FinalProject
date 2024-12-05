import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About StartUpConnect")

st.markdown (
    """
    ### Welcome to StartUpConnect!

    StartUpConnect is a platform designed to connect students and startups. Our platform serves multiple user groups:

    #### For Students
    - Browse exciting startup opportunities and full-time positions
    - Track your application status in real-time
    - Access career resources and guidance
    - Connect directly with startup founders

    #### For Startup Founders
    - Post job openings and internship opportunities
    - Review and manage applications
    - Connect with promising student talent
    - Build your startup team efficiently
    - Provide feedback on student applications

    #### For Career Center Staff
    - Monitor student placement metrics
    - Track internship and job placement success
    - Generate insights on employment trends
    - Support both students and startups in their hiring journey

    ### How It Works
    1. Students create profiles and browse opportunities
    2. Startups post positions and review applications
    3. Career Center staff provide oversight and support and analyze real time data

    Start exploring StartUpConnect today to be part of this exciting journey in startup recruitment and career development!
    """
        )
