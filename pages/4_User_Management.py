import streamlit as st
import pandas as pd
import hashlib
from utils.data_loader import load_users, save_users, load_roles

st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide"
)

def show_user_management_page():
    st.title("User Management")

    # --- Add New User Form ---
    st.header("Add New User")

    roles_df = load_roles()
    role_options = roles_df['RoleName'].tolist()

    with st.form("new_user_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Temporary Password", type="password")
        role = st.selectbox("Role", role_options)
        submitted = st.form_submit_button("Create User")

        if submitted:
            if username and password and role:
                users_df = load_users()
                if username in users_df['Username'].values:
                    st.error(f"Username '{username}' already exists.")
                else:
                    # Hash the password for security
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    role_id = roles_df[roles_df['RoleName'] == role].iloc[0]['RoleID']

                    new_user = pd.DataFrame({
                        'UserID': [len(users_df) + 1],
                        'Username': [username],
                        'PasswordHash': [password_hash],
                        'RoleID': [role_id]
                    })

                    updated_users = pd.concat([users_df, new_user], ignore_index=True)
                    save_users(updated_users)
                    st.success(f"User '{username}' created successfully!")
            else:
                st.warning("Please fill out all fields.")

    st.markdown("---")

    # --- Display Existing Users ---
    st.header("Existing Users")

    users_df = load_users()
    # Merge with roles to show role names
    full_users_df = pd.merge(users_df, roles_df, on='RoleID')

    st.dataframe(full_users_df[['Username', 'RoleName']], use_container_width=True)


# --- Main app logic ---
# Ensure user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to access this page.")
    st.page_link("app.py", label="Go to Login", icon="🏠")
# Ensure user is an admin (assuming 'manage_users' permission is for admins)
elif 'manage_users' not in st.session_state['user_info']['Permissions']:
    st.error("You do not have permission to view this page.")
else:
    show_user_management_page()