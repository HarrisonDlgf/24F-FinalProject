# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    if st.sidebar.button("🏠 Home"):
        st.switch_page("Home")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ----------------------------- STARTUP ROLES -----------------------------

## START CREATING PAGES FOR STARTUP ROLES
def CareerCenterHomeNav():
    st.sidebar.page_link(
        "pages/00_Career_Center_Home.py", label="Career Center Home", icon="🎓"
    )

def FullTimeStudentHomeNav():
    st.sidebar.page_link(
        "pages/00_FullTime_Student_Home.py", label="Full Time Student Home", icon="🧑‍🎓👩‍🎓"
    )

def CoOpStudentHomeNav():
    st.sidebar.page_link(
        "pages/00_CoOp_Student_Home.py", label="Co-Op Student Home", icon="🌐"
    )

def StartupFounderHomeNav():
    st.sidebar.page_link(
        "pages/00_Startup_Founder_Home.py", label="Startup Founder Home", icon="🚀"
    )

## ------------------------ Examples for Role of usaid_worker ------------------------
def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )


def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/startupConnectLogo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()
    else:
        HomeNav()
    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:
        
        # Career Center role
        if st.session_state["role"] == "career_center":
            CareerCenterHomeNav()

        # Full Time Student role
        if st.session_state["role"] == "fulltime_student":
            FullTimeStudentHomeNav()

        # Co-Op Student role
        if st.session_state["role"] == "coop_student":
            CoOpStudentHomeNav()

        # Startup Founder role
        if st.session_state["role"] == "startup_founder":
            StartupFounderHomeNav()

        # Administrator role (keeping this one)
        if st.session_state["role"] == "administrator":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
