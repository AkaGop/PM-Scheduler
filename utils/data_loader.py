import pandas as pd
import streamlit as st
import os

DATA_DIR = "data"

def load_users():
    """Loads users from the excel file."""
    return pd.read_excel(os.path.join(DATA_DIR, "users.xlsx"))

def load_roles():
    """Loads roles from the excel file."""
    return pd.read_excel(os.path.join(DATA_DIR, "roles.xlsx"))

def load_equipment():
    """Loads equipment from the excel file."""
    return pd.read_excel(os.path.join(DATA_DIR, "equipment.xlsx"))

def load_maintenance_log():
    """Loads maintenance log from the excel file."""
    return pd.read_excel(os.path.join(DATA_DIR, "maintenance_log.xlsx"))

def load_frequencies():
    """Loads frequencies from the excel file."""
    return pd.read_excel(os.path.join(DATA_DIR, "frequencies.xlsx"))

def save_equipment(df):
    """Saves the equipment dataframe to the excel file."""
    df.to_excel(os.path.join(DATA_DIR, "equipment.xlsx"), index=False)

def save_maintenance_log(df):
    """Saves the maintenance log dataframe to the excel file."""
    df.to_excel(os.path.join(DATA_DIR, "maintenance_log.xlsx"), index=False)

def save_frequencies(df):
    """Saves the frequencies dataframe to the excel file."""
    df.to_excel(os.path.join(DATA_DIR, "frequencies.xlsx"), index=False)