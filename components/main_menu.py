# components/main_menu.py

import streamlit as st
from streamlit_js_eval import streamlit_js_eval


def show_main_menu():
    """
    Displays the main menu. This version includes the final corrected
    function call for the "Test Reminder Notification" button.
    """
    st.markdown("## What do you need today?")

    subtopic_buttons = [
        "Daily Devotion", "Daily Prayer", "Daily Meditation", "Daily Accountability"
    ]
    dedicated_page_buttons = {
        "Dashboard": "dashboard",
        "SOS Support": "sos_support",
        "Inspiration Feed": "inspiration_feed",
        "Calendar Sync": "calendar_sync",
        "Just Chat": "just_chat"
    }

    st.markdown("### Daily Practices")
    cols = st.columns(2)
    for i, btn in enumerate(subtopic_buttons):
        if cols[i % 2].button(btn, key=f"subtopic_{i}"):
            st.session_state.selected_section = btn
            st.session_state.page = "subtopics"
            st.rerun()

    st.markdown("### Tools & Support")
    cols2 = st.columns(2)

    if cols2[0].button("📊 Dashboard", key="dashboard_btn"):
        st.session_state.page = dedicated_page_buttons["Dashboard"]
        st.rerun()

    if cols2[1].button("🆘 SOS Support", key="sos_btn"):
        st.session_state.page = dedicated_page_buttons["SOS Support"]
        st.rerun()

    if cols2[0].button("🗓️ Calendar Sync", key="calendar_btn"):
        st.session_state.page = dedicated_page_buttons["Calendar Sync"]
        st.rerun()

    if cols2[1].button("✨ Inspiration Feed", key="inspiration_btn"):
        st.session_state.page = dedicated_page_buttons["Inspiration Feed"]
        st.rerun()

    st.markdown("---")
    if st.button("💬 Just Chat", key="chat_btn", use_container_width=True):
        st.session_state.page = dedicated_page_buttons["Just Chat"]
        st.rerun()

    # --- Functional Notification Button ---
    if st.button("🔔 Test Reminder Notification", help="Click to test browser notifications", key="reminder_btn"):
        js_code = """
        const showNotification = () => {
            if (!("Notification" in window)) {
                alert("This browser does not support desktop notification");
                return;
            }
            if (Notification.permission === "granted") {
                new Notification("DSCPL Reminder!", {
                    body: "This is how your daily reminders would look. For real reminders, use the Calendar Sync feature!",
                    icon: "https://i.imgur.com/vQkJOQ1.png"
                });
            } 
            else if (Notification.permission !== "denied") {
                Notification.requestPermission().then(function (permission) {
                    if (permission === "granted") {
                        new Notification("DSCPL Reminder!", {
                            body: "Great! Notifications are enabled.",
                            icon: "https://i.imgur.com/vQkJOQ1.png"
                        });
                    }
                });
            }
        }
        showNotification();
        """
        # FIX: The JavaScript code must be passed as a keyword argument.
        streamlit_js_eval(js_expressions=js_code)
        st.success("Notification test sent! Check your browser and system notifications.")

