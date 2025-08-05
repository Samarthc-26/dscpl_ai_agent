# components/subtopics.py

import streamlit as st
# Import the new function from the agent
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

    if section in topics_map:
        st.markdown("### 📚 Choose a topic:")
        cols = st.columns(2)
        for i, topic in enumerate(topics_map[section]):
            if cols[i % 2].button(topic, key=f"topic_{i}"):
                st.session_state["selected_topic"] = topic
                if "guidance" in st.session_state:
                    del st.session_state["guidance"]

    st.markdown("### ✍️ Or enter a custom topic:")
    custom_topic = st.text_input("Your custom topic", key="custom_input", label_visibility="collapsed")

    st.markdown("---")

    _, col2, _ = st.columns([2, 3, 2])
    with col2:
        # Update the button text for clarity
        if st.button("🕊️ Get Spiritual Guidance", use_container_width=True):
            final_topic = custom_topic.strip() or st.session_state.get("selected_topic", "")

            if not final_topic:
                st.warning("Please select or enter a topic.")
            else:
                st.info(f"Generating spiritual guidance for: **{final_topic}**")
                with st.spinner("Talking to your spiritual assistant..."):
                    # Call the new function and store the result
                    st.session_state.guidance = generate_spiritual_guidance(final_topic, section)
                st.rerun()

    # --- Display the generated article ---
    if "guidance" in st.session_state and st.session_state.guidance:
        st.success("✅ Here is your spiritual guidance:")
        # Use st.markdown to render the formatted text beautifully
        st.markdown(st.session_state.guidance, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔙 Back to Home"):
        for key in ["guidance", "selected_topic", "selected_section"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.page = "menu"
        st.rerun()
