import streamlit as st
import pandas as pd
from utils.data_loader import load_equipment, load_maintenance_log, load_users
from utils.notifications import check_for_notifications
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

def show_dashboard():
    st.title("Main Dashboard")

    # Load data
    equipment_df = load_equipment()
    users_df = load_users()
    log_df = load_maintenance_log()

    # --- Display Notifications ---
    notifications = check_for_notifications(equipment_df, users_df)
    if notifications:
        st.subheader("Notifications")
        for notification in notifications:
            if notification['type'] == 'error':
                st.error(notification['message'])
            elif notification['type'] == 'warning':
                st.warning(notification['message'])
        st.markdown("---")


    # --- KPI Cards ---
    total_equipment = len(equipment_df)

    # Calculate Overdue PMs
    # Ensure 'NextPM' is datetime
    equipment_df['NextPM'] = pd.to_datetime(equipment_df['NextPM'])
    overdue_pms = equipment_df[equipment_df['NextPM'] < datetime.now()].shape[0]

    # Calculate Upcoming PMs (next 7 days)
    upcoming_pms = equipment_df[(equipment_df['NextPM'] > datetime.now()) &
                                (equipment_df['NextPM'] <= datetime.now() + timedelta(days=7))].shape[0]

    # Calculate Total Downtime (from logs) - assuming 'Downtime' is in hours
    total_downtime = log_df['Downtime'].sum() if 'Downtime' in log_df.columns else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Equipment", value=total_equipment)
    with col2:
        st.metric(label="Overdue PMs", value=overdue_pms)
    with col3:
        st.metric(label="Upcoming PMs (7 days)", value=upcoming_pms)
    with col4:
        st.metric(label="Total Downtime (hours)", value=f"{total_downtime:.2f}")

    st.markdown("---")

    # --- Maintenance Analysis Chart ---
    st.header("Maintenance Status Analysis")

    # Determine status for the chart
    def get_status(next_pm_date):
        if next_pm_date < datetime.now():
            return "Overdue"
        elif next_pm_date <= datetime.now() + timedelta(days=7):
            return "Upcoming"
        else:
            return "Scheduled"

    equipment_df['PM_Status'] = equipment_df['NextPM'].apply(get_status)
    status_counts = equipment_df['PM_Status'].value_counts()

    st.bar_chart(status_counts)


# --- Main app logic ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to view the dashboard.")
    st.page_link("app.py", label="Go to Login", icon="🏠")
else:
    show_dashboard()