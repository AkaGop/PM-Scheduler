import streamlit as st
import pandas as pd
import hashlib
from utils.data_loader import load_users, load_roles
from utils.ui_helpers import load_css

st.set_page_config(
    page_title="Semiconductor Maintenance Scheduler",
    page_icon="🛠️",
    layout="wide"
)

# Load custom CSS
load_css("style.css")

def login():
    """Displays the login page and handles user authentication."""
    st.title("Login")

    users_df = load_users()
    roles_df = load_roles()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Hash the entered password for comparison
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = users_df[(users_df['Username'] == username) & (users_df['PasswordHash'] == password_hash)]

        if not user.empty:
            st.session_state['logged_in'] = True
            st.session_state['user_info'] = user.iloc[0].to_dict()

            # Load role and permissions
            role_id = user.iloc[0]['RoleID']
            role_info = roles_df[roles_df['RoleID'] == role_id].iloc[0]
            st.session_state['user_info']['RoleName'] = role_info['RoleName']
            st.session_state['user_info']['Permissions'] = role_info['Permissions'].split(',')

            st.rerun()
        else:
            st.error("Invalid username or password")

def show_welcome_page():
    """The main application after a user has logged in."""
    st.sidebar.title(f"Welcome, {st.session_state['user_info']['Username']}")
    st.sidebar.write(f"Role: {st.session_state['user_info']['RoleName']}")

    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # Redirect to the main dashboard page
    st.switch_page("pages/1_Dashboard.py")


if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login()
else:
    show_welcome_page()