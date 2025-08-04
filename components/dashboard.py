# components/dashboard.py

import streamlit as st
from datetime import datetime


def show_dashboard():
    # --- Custom CSS to style the dashboard like the screenshot ---
    st.markdown("""
    <style>
        /* Main container for the dashboard */
        .dashboard-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }
        /* Day boxes */
        .day-box {
            background-color: #F0E6D2; /* Tan background */
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            width: 80px;
            height: 80px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            font-size: 1.1em;
        }
        .day-box.completed {
            background-color: #A3D9A5; /* Green for completed */
            color: #333;
        }
        .day-box .icon {
            font-size: 2em;
            line-height: 1;
        }
        /* Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            background-color: #6c8d6d;
            color: white;
            border: none;
            padding: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Initialize Session State ---
    # This dictionary will store the completion status for each day of the week (0=Mon, 6=Sun)
    if 'progress' not in st.session_state:
        st.session_state.progress = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
    if 'paused' not in st.session_state:
        st.session_state.paused = False

    # --- Dashboard Title and Status ---
    st.markdown("<h2 style='text-align: center;'>📊 Your Spiritual Progress Dashboard</h2>", unsafe_allow_html=True)

    status_text = "✅ Active" if not st.session_state.paused else "⏸️ Paused"
    st.markdown(f"<p style='text-align: center;'><b>Status:</b> {status_text}</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- 7-Day Progress View ---
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    today_index = datetime.now().weekday()  # Monday is 0, Sunday is 6

    cols = st.columns(7)
    for i, day in enumerate(days_of_week):
        is_completed = st.session_state.progress[i]

        with cols[i]:
            # Determine icon and class for styling
            if is_completed:
                icon = "✔️"  # Checkmark for completed
                box_class = "completed"
            else:
                icon = "❌"  # Cross for not completed
                box_class = ""

            st.markdown(f"""
            <div class="day-box {box_class}">
                {day}
                <div class="icon">{icon}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- Control Buttons ---
    btn_cols = st.columns(3)

    # Mark Today Complete Button
    if btn_cols[0].button("✅ Mark Today Complete"):
        st.session_state.progress[today_index] = True
        st.rerun()

    # Pause/Resume Program Button
    pause_text = "⏸️ Pause Program" if not st.session_state.paused else "▶️ Resume Program"
    if btn_cols[1].button(pause_text):
        st.session_state.paused = not st.session_state.paused
        st.rerun()

    # Reset Program Button
    if btn_cols[2].button("🔄 Reset Program"):
        # Reset progress for all days
        st.session_state.progress = {day: False for day in range(7)}
        st.session_state.paused = False
        st.rerun()

    st.markdown("---")
    if st.button("🔙 Back to Home"):
        st.session_state.page = "menu"