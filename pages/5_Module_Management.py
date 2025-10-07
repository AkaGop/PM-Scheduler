import streamlit as st
import pandas as pd
from utils.data_loader import load_equipment, load_modules, save_modules

st.set_page_config(
    page_title="Module Management",
    page_icon="🧩",
    layout="wide"
)

def show_module_management_page():
    st.title("Module Management")

    equipment_df = load_equipment()
    modules_df = load_modules()

    # --- Add New Module Form ---
    st.header("Add New Module")
    with st.form("new_module_form", clear_on_submit=True):
        # Dropdown to select equipment
        equipment_list = equipment_df['EquipmentName'].tolist()
        selected_equipment_name = st.selectbox("Select Equipment", equipment_list)

        module_name = st.text_input("New Module Name")

        submitted = st.form_submit_button("Add Module")

        if submitted:
            if selected_equipment_name and module_name:
                # Find the EquipmentID for the selected name
                equipment_id = equipment_df[equipment_df['EquipmentName'] == selected_equipment_name].iloc[0]['EquipmentID']

                # Create new module entry
                new_module = pd.DataFrame({
                    'ModuleID': [modules_df['ModuleID'].max() + 1 if not modules_df.empty else 501], # Ensure unique ID
                    'ModuleName': [module_name],
                    'EquipmentID': [equipment_id]
                })

                # Append and save
                updated_modules = pd.concat([modules_df, new_module], ignore_index=True)
                save_modules(updated_modules)
                st.success(f"Module '{module_name}' added to '{selected_equipment_name}'.")
                st.rerun()
            else:
                st.warning("Please select equipment and enter a module name.")

    st.markdown("---")

    # --- Display Existing Modules ---
    st.header("Existing Modules")

    # Merge with equipment to show equipment names
    if not modules_df.empty:
        full_modules_df = pd.merge(modules_df, equipment_df[['EquipmentID', 'EquipmentName']], on='EquipmentID', how='left')

        # Display modules with delete buttons
        for index, row in full_modules_df.iterrows():
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(row['ModuleName'])
            with col2:
                st.write(f"*{row['EquipmentName']}*")
            with col3:
                if st.button("Delete", key=f"delete_module_{row['ModuleID']}"):
                    modules_df = modules_df[modules_df['ModuleID'] != row['ModuleID']]
                    save_modules(modules_df)
                    st.rerun()
    else:
        st.info("No modules have been added yet.")


# --- Main app logic ---
# Ensure user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to access this page.")
    st.page_link("app.py", label="Go to Login", icon="🏠")
# Ensure user has permission (e.g., admins or managers with 'manage_settings')
elif 'manage_settings' not in st.session_state['user_info']['Permissions']:
    st.error("You do not have permission to view this page.")
else:
    show_module_management_page()