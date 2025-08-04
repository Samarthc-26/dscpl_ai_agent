# components/subtopics.py

import streamlit as st
from agents.topic_agent import generate_daily_program

# Predefined subtopics per section
topics_map = {
    "Daily Devotion": [
        "Dealing with Stress", "Overcoming Fear", "Conquering Depression",
        "Relationships", "Healing", "Purpose & Calling", "Anxiety"
    ],
    "Daily Prayer": [
        "Personal Growth", "Healing", "Family/Friends", "Forgiveness",
        "Finances", "Work/Career"
    ],
    "Daily Meditation": [
        "Peace", "God's Presence", "Strength", "Wisdom", "Faith"
    ],
    "Daily Accountability": [
        "Pornography", "Alcohol", "Drugs", "Sex", "Addiction", "Laziness"
    ]
}


def show_subtopics(section):
    st.markdown(f"## ✝️ You selected: **{section}**")

    # --- Topic selection UI ---
    if section in topics_map:
        st.markdown("### 📚 Choose a topic:")
        cols = st.columns(2)
        for i, topic in enumerate(topics_map[section]):
            if cols[i % 2].button(topic, key=f"topic_{i}"):
                st.session_state["selected_topic"] = topic
                if "plan" in st.session_state:
                    del st.session_state["plan"]

    st.markdown("### ✍️ Or enter a custom topic:")
    # The label is hidden because we have a markdown title right above it.
    custom_topic = st.text_input("Your custom topic", key="custom_input", label_visibility="collapsed")

    st.markdown("---")  # Visual separator

    # --- Program generation button (NEW, CENTRAL LOCATION) ---
    # We use columns to center the button on the page
    _, col2, _ = st.columns([2, 3, 2])
    with col2:
        if st.button("🚀 Start Program", use_container_width=True):
            final_topic = custom_topic.strip() or st.session_state.get("selected_topic", "")

            if not final_topic:
                st.warning("Please select or enter a topic.")
            else:
                st.info(f"Generating your 7-day spiritual plan for: **{final_topic}**")
                with st.spinner("Talking to your spiritual assistant..."):
                    st.session_state.plan = generate_daily_program(final_topic, section)
                st.rerun()

    # --- Plan display area ---
    if "plan" in st.session_state and st.session_state.plan:
        st.success("✅ Here’s your 7-day plan:")
        st.text_area("Spiritual Program", value=st.session_state.plan, height=400)

    # --- Always-visible Back Button ---
    st.markdown("---")
    if st.button("🔙 Back to Home"):
        for key in ["plan", "selected_topic", "selected_section"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.page = "menu"
        st.rerun()