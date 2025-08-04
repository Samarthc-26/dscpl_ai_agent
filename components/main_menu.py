# components/main_menu.py

import streamlit as st


def show_main_menu():
    st.markdown("## What do you need today?")

    # Define which buttons go to subtopics and which have dedicated pages
    subtopic_buttons = [
        "Daily Devotion", "Daily Prayer", "Daily Meditation", "Daily Accountability"
    ]
    dedicated_page_buttons = {
        "Dashboard": "dashboard",
        "SOS Support": "sos_support",
        "Calendar Sync": "calendar_sync",
        "Inspiration Feed": "inspiration_feed"
    }
    chat_button = "Just Chat"

    # Display buttons that lead to subtopics
    cols = st.columns(2)
    for i, btn in enumerate(subtopic_buttons):
        if cols[i % 2].button(btn):
            st.session_state.selected_section = btn
            st.session_state.page = "subtopics"

    # Display buttons for dedicated pages
    st.markdown("---")
    cols2 = st.columns(2)

    # Dashboard and SOS Support
    if cols2[0].button("Dashboard"):
        st.session_state.page = dedicated_page_buttons["Dashboard"]
    if cols2[1].button("SOS Support"):
        st.session_state.page = dedicated_page_buttons["SOS Support"]

    # Calendar Sync and Inspiration Feed
    if cols2[0].button("Calendar Sync"):
        st.session_state.page = dedicated_page_buttons["Calendar Sync"]
    if cols2[1].button("Inspiration Feed"):
        st.session_state.page = dedicated_page_buttons["Inspiration Feed"]

    # Just Chat and Test Reminder
    st.markdown("---")
    if st.button(chat_button):
        # Add logic for "Just Chat" if it's different from subtopics
        st.info("The 'Just Chat' feature is under development.")

    st.button("🔔 Test Reminder Notification", help="Simulates a reminder (coming soon!)")