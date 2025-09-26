import streamlit as st
import pandas as pd
from utils.data_loader import load_frequencies, save_frequencies

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

def show_settings_page():
    st.title("Settings")

    # --- Frequency Management ---
    st.header("Manage Maintenance Frequencies")

    frequencies_df = load_frequencies()

    st.write("Current Frequencies:")

    # Display frequencies with delete buttons
    for index, row in frequencies_df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(row['FrequencyName'])
        with col2:
            if st.button("Delete", key=f"delete_freq_{index}"):
                frequencies_df = frequencies_df.drop(index)
                save_frequencies(frequencies_df)
                st.rerun()

    # Add new frequency
    with st.form("new_frequency_form"):
        new_freq_name = st.text_input("New Frequency Name")
        submitted = st.form_submit_button("Add Frequency")

        if submitted and new_freq_name:
            new_freq_df = pd.DataFrame({'FrequencyName': [new_freq_name]})
            frequencies_df = pd.concat([frequencies_df, new_freq_df], ignore_index=True)
            save_frequencies(frequencies_df)
            st.success(f"Added frequency: {new_freq_name}")
            st.rerun()

# --- Main app logic ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to view settings.")
    st.page_link("app.py", label="Go to Login", icon="🏠")
elif 'manage_users' not in st.session_state['user_info']['Permissions']: # Using 'manage_users' as admin proxy
    st.error("You do not have permission to view this page.")
else:
    show_settings_page()