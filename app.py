# app.py

import streamlit as st
from components.main_menu import show_main_menu
from components.subtopics import show_subtopics
from components.dashboard import show_dashboard
from components.sos_support import show_sos_support
from components.inspiration_feed import show_inspiration_feed
from components.calendar_sync import show_calendar_sync
from components.just_chat import show_just_chat # Import the new chat page

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "selected_section" not in st.session_state:
    st.session_state.selected_section = None

st.set_page_config(page_title="DSCPL - AI Agent", layout="centered")

st.markdown("### 🙏 Welcome to DSCPL – Your Spiritual Companion")

# Routing logic
if st.session_state.page == "menu":
    show_main_menu()
elif st.session_state.page == "subtopics":
    show_subtopics(st.session_state.selected_section)
elif st.session_state.page == "dashboard":
    show_dashboard()
elif st.session_state.page == "sos_support":
    show_sos_support()
elif st.session_state.page == "inspiration_feed":
    show_inspiration_feed()
elif st.session_state.page == "calendar_sync":
    show_calendar_sync()
elif st.session_state.page == "just_chat": # Add the new route
    show_just_chat()
