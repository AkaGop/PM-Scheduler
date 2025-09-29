import streamlit as st
import pandas as pd
from utils.data_loader import load_equipment, save_equipment, load_maintenance_log, save_maintenance_log, load_modules
from utils.exporters import to_excel, to_csv
from datetime import datetime

st.set_page_config(
    page_title="Maintenance Schedule",
    page_icon="📅",
    layout="wide"
)

def show_maintenance_schedule():
    st.title("Maintenance Schedule")

    equipment_df = load_equipment().copy()
    modules_df = load_modules()
    equipment_df['NextPM'] = pd.to_datetime(equipment_df['NextPM'])

    # Determine Status
    def get_status(row):
        if 'In PM' in st.session_state and st.session_state['In PM'] == row['EquipmentID']:
            return "In Progress"
        if row['NextPM'] < datetime.now():
            return "Overdue"
        elif row['NextPM'] <= datetime.now() + pd.Timedelta(days=7):
            return "Upcoming"
        else:
            return "Scheduled"

    equipment_df['Status'] = equipment_df.apply(get_status, axis=1)

    # Search and Filter
    st.sidebar.header("Filters")
    search_term = st.sidebar.text_input("Search by Equipment Name")
    status_options = ["All", "Overdue", "Upcoming", "Scheduled", "In Progress"]
    selected_status = st.sidebar.selectbox("Filter by Status", status_options)

    # Apply Filters
    filtered_df = equipment_df
    if search_term:
        filtered_df = filtered_df[filtered_df['EquipmentName'].str.contains(search_term, case=False)]
    if selected_status != "All":
        filtered_df = filtered_df[filtered_df['Status'] == selected_status]

    # --- Export options ---
    st.sidebar.header("Export Options")

    # Use the filtered dataframe for exporting
    if not filtered_df.empty:
        st.sidebar.download_button(
            label="Export to Excel",
            data=to_excel(filtered_df),
            file_name=f"maintenance_schedule_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        st.sidebar.download_button(
            label="Export to CSV",
            data=to_csv(filtered_df),
            file_name=f"maintenance_schedule_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

    # Display Tasks
    for index, row in filtered_df.iterrows():
        expander = st.expander(f"{row['EquipmentName']} - {row['Department']} (Status: {row['Status']})")
        with expander:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Last PM:** {row['LastPM'].strftime('%Y-%m-%d')}")
                st.write(f"**Frequency:** {row['Frequency']}")
                st.write(f"**Next PM:** {row['NextPM'].strftime('%Y-%m-%d')}")
            with col2:
                st.write(f"**Criticality:** {row['Criticality']}")

            # Display Modules associated with the equipment
            st.markdown("---")
            st.write("**Associated Modules:**")
            equipment_modules = modules_df[modules_df['EquipmentID'] == row['EquipmentID']]
            if not equipment_modules.empty:
                st.dataframe(
                    equipment_modules[['ModuleName']],
                    hide_index=True,
                    use_container_width=True,
                    height=(len(equipment_modules) + 1) * 35 # Dynamically adjust height
                )
            else:
                st.info("No modules associated with this equipment.")

            with col3:
                if 'complete_tasks' in st.session_state['user_info']['Permissions']:
                    if st.session_state.get('In PM') == row['EquipmentID']:
                        if st.button("Complete Task", key=f"complete_{row['EquipmentID']}"):
                            st.session_state['task_to_complete'] = row['EquipmentID']
                            st.rerun()
                    else:
                        if st.button("Start PM Activity", key=f"start_{row['EquipmentID']}", disabled=(st.session_state.get('In PM') is not None)):
                            st.session_state['In PM'] = row['EquipmentID']
                            st.session_state['PM_Start_Time'] = datetime.now()
                            st.rerun()

    # --- Task Completion Form ---
    if 'task_to_complete' in st.session_state:
        equipment_id = st.session_state['task_to_complete']
        equipment_details = equipment_df[equipment_df['EquipmentID'] == equipment_id].iloc[0]

        with st.form("completion_form"):
            st.subheader(f"Completing PM for: {equipment_details['EquipmentName']}")
            notes = st.text_area("Notes/Comments")
            parts_used = st.text_input("Parts Used")
            pre_cal_data = st.text_input("Pre-Maintenance Calibration Data")
            post_cal_data = st.text_input("Post-Maintenance Calibration Data")
            env_readings = st.text_input("Environmental Readings")
            tool_status_before = st.selectbox("Tool Status Before", ["In Production", "Scheduled Down", "Unscheduled Down"])
            tool_status_after = st.selectbox("Tool Status After", ["In Production", "Scheduled Down", "Unscheduled Down"])
            lot_id = st.text_input("Associated Lot/Batch ID")
            submitted = st.form_submit_button("Submit Completion")

            if submitted:
                end_time = datetime.now()
                start_time = st.session_state['PM_Start_Time']
                downtime = (end_time - start_time).total_seconds() / 3600 # in hours
                log_df = load_maintenance_log()
                new_log_entry = pd.DataFrame([{
                    'LogID': len(log_df) + 1,
                    'EquipmentID': equipment_id,
                    'TechnicianID': st.session_state['user_info']['UserID'],
                    'StartTime': start_time,
                    'EndTime': end_time,
                    'Downtime': downtime,
                    'Notes': notes,
                    'PartsUsed': parts_used,
                    'PreMaintenanceData': pre_cal_data,
                    'PostMaintenanceData': post_cal_data,
                    'EnvironmentalReadings': env_readings,
                    'ToolStatusBefore': tool_status_before,
                    'ToolStatusAfter': tool_status_after,
                    'LotID': lot_id,
                    'QASignOff': None
                }])
                log_df = pd.concat([log_df, new_log_entry], ignore_index=True)
                save_maintenance_log(log_df)
                current_equipment = load_equipment()
                idx = current_equipment[current_equipment['EquipmentID'] == equipment_id].index
                current_equipment.loc[idx, 'LastPM'] = end_time.date()
                freq_map = {'Weekly': 7, 'Monthly': 30, 'Semi-Annually': 180}
                days_to_add = freq_map.get(equipment_details['Frequency'], 30)
                current_equipment.loc[idx, 'NextPM'] = end_time.date() + pd.Timedelta(days=days_to_add)
                save_equipment(current_equipment)
                del st.session_state['In PM']
                del st.session_state['PM_Start_Time']
                del st.session_state['task_to_complete']
                st.success("PM Task Completed and Logged!")
                st.rerun()

# --- Main app logic ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to view the maintenance schedule.")
    st.page_link("app.py", label="Go to Login", icon="🏠")
else:
    show_maintenance_schedule()