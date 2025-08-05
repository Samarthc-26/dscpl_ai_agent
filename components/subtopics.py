# components/subtopics.py

import streamlit as st
from agents.topic_agent import generate_spiritual_guidance

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

    # --- Section for Predefined Topics (Now with instant response) ---
    if section in topics_map:
        st.markdown("### 📚 Choose a topic for instant guidance:")
        cols = st.columns(2)
        for i, topic in enumerate(topics_map[section]):
            if cols[i % 2].button(topic, key=f"topic_{i}"):
                # When a button is clicked, generate guidance immediately
                with st.spinner(f"Generating guidance for '{topic}'..."):
                    st.session_state.guidance = generate_spiritual_guidance(topic, section)
                st.rerun()  # Rerun to display the new content

    st.markdown("---")

    # --- Section for Custom Topics ---
    st.markdown("### ✍️ Or enter a custom topic:")
    custom_topic = st.text_input("Your custom topic", key="custom_input", label_visibility="collapsed")

    # This button is now only for the custom topic
    if st.button("🕊️ Get Guidance for Custom Topic", use_container_width=True):
        final_topic = custom_topic.strip()
        if not final_topic:
            st.warning("Please enter a topic in the text box above.")
        else:
            st.info(f"Generating spiritual guidance for: **{final_topic}**")
            with st.spinner("Talking to your spiritual assistant..."):
                st.session_state.guidance = generate_spiritual_guidance(final_topic, section)
            st.rerun()

    # --- Display Area (shows guidance from either method) ---
    if "guidance" in st.session_state and st.session_state.guidance:
        st.success("✅ Here is your spiritual guidance:")
        st.markdown(st.session_state.guidance, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔙 Back to Home"):
        for key in ["guidance", "selected_topic", "selected_section"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.page = "menu"
        st.rerun()
