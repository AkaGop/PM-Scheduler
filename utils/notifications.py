import streamlit as st
import pandas as pd
from datetime import datetime

def check_for_notifications(equipment_df, users_df):
    """
    Checks for overdue and upcoming PMs and returns notification messages.
    In a real app, this would trigger emails.
    """
    notifications = []

    # Check for overdue PMs
    overdue_pms = equipment_df[equipment_df['NextPM'] < datetime.now()]
    if not overdue_pms.empty:
        for index, row in overdue_pms.iterrows():
            msg = f"**Overdue PM Alert:** {row['EquipmentName']} was due on {row['NextPM'].strftime('%Y-%m-%d')}."
            notifications.append({'type': 'error', 'message': msg})

    # Check for upcoming PMs
    upcoming_pms = equipment_df[(equipment_df['NextPM'] > datetime.now()) &
                                (equipment_df['NextPM'] <= datetime.now() + pd.Timedelta(days=7))]
    if not upcoming_pms.empty:
        for index, row in upcoming_pms.iterrows():
            msg = f"**Upcoming PM Reminder:** {row['EquipmentName']} is due on {row['NextPM'].strftime('%Y-%m-%d')}."
            notifications.append({'type': 'warning', 'message': msg})

    return notifications