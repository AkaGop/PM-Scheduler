import streamlit as st
import pandas as pd
from utils.data_loader import load_equipment, load_maintenance_log, load_users
from utils.notifications import check_for_notifications
from utils.ui_helpers import kpi_card
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
    notifications = check_for_notifications(equipment_df)
    if notifications:
        st.subheader("Actionable Alerts")
        for notification in notifications:
            if notification['type'] == 'error':
                st.error(notification['message'], icon="🔥")
            elif notification['type'] == 'warning':
                st.warning(notification['message'], icon="⚠️")
        st.markdown("---")


    # --- KPI Cards ---
    st.subheader("Key Performance Indicators")
    total_equipment = len(equipment_df)

    # Calculate Overdue PMs
    equipment_df['NextPM'] = pd.to_datetime(equipment_df['NextPM'])
    overdue_pms = equipment_df[equipment_df['NextPM'] < datetime.now()].shape[0]

    # Calculate Upcoming PMs (next 7 days)
    upcoming_pms = equipment_df[(equipment_df['NextPM'] > datetime.now()) &
                                (equipment_df['NextPM'] <= datetime.now() + timedelta(days=7))].shape[0]

    # Calculate Total Downtime (from logs)
    total_downtime = log_df['Downtime'].sum() if 'Downtime' in log_df.columns else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("Total Equipment", total_equipment, icon="⚙️")
    with col2:
        kpi_card("Overdue PMs", overdue_pms, icon="🔥")
    with col3:
        kpi_card("Upcoming PMs (7d)", upcoming_pms, icon="📅")
    with col4:
        kpi_card("Total Downtime (hrs)", f"{total_downtime:.2f}", icon="⏱️")

    st.markdown("<br>", unsafe_allow_html=True) # Add some space

    # --- Maintenance Analysis Chart ---
    st.header("Maintenance Status Overview")

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

    st.bar_chart(status_counts, color="#2563EB")


# --- Main app logic ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to view the dashboard.")
    st.page_link("app.py", label="Go to Login", icon="🏠")
else:
    show_dashboard()