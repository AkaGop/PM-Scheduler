import streamlit as st

def load_css(file_name):
    """Loads a CSS file and injects it into the Streamlit app."""
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")

def kpi_card(title, value, icon=""):
    """Displays a KPI card with a title, value, and optional icon."""
    st.markdown(f"""
    <div class="kpi-card">
        <h3>{icon} {title}</h3>
        <p>{value}</p>
    </div>
    """, unsafe_allow_html=True)