# components/main_menu.py

import streamlit as st


def show_main_menu():
    """
    Displays the main menu. This version includes st.rerun() for instant
    page navigation, providing a single-click experience.
    """
    st.markdown("## What do you need today?")

    subtopic_buttons = [
        "Daily Devotion", "Daily Prayer", "Daily Meditation", "Daily Accountability"
    ]
    dedicated_page_buttons = {
        "Dashboard": "dashboard",
        "SOS Support": "sos_support",
        "Inspiration Feed": "inspiration_feed",
        "Calendar Sync": "calendar_sync"
    }

    st.markdown("### Daily Practices")
    cols = st.columns(2)
    for i, btn in enumerate(subtopic_buttons):
        # Adding a unique key to each button is good practice
        if cols[i % 2].button(btn, key=f"subtopic_{i}"):
            st.session_state.selected_section = btn
            st.session_state.page = "subtopics"
            st.rerun()  # FIX: Force an immediate rerun

    st.markdown("### Tools & Support")
    cols2 = st.columns(2)

    if cols2[0].button("📊 Dashboard", key="dashboard_btn"):
        st.session_state.page = dedicated_page_buttons["Dashboard"]
        st.rerun()  # FIX: Force an immediate rerun

    if cols2[1].button("🆘 SOS Support", key="sos_btn"):
        st.session_state.page = dedicated_page_buttons["SOS Support"]
        st.rerun()  # FIX: Force an immediate rerun

    if cols2[0].button("🗓️ Calendar Sync", key="calendar_btn"):
        st.session_state.page = dedicated_page_buttons["Calendar Sync"]
        st.rerun()  # FIX: Force an immediate rerun

    if cols2[1].button("✨ Inspiration Feed", key="inspiration_btn"):
        st.session_state.page = dedicated_page_buttons["Inspiration Feed"]
        st.rerun()  # FIX: Force an immediate rerun

    st.markdown("---")
    if st.button("Just Chat", key="chat_btn"):
        st.info("The 'Just Chat' feature is under development.")

    st.button("🔔 Test Reminder Notification", help="Simulates a reminder (coming soon!)", key="reminder_btn")
