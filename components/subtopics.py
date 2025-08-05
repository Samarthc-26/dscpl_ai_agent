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


def render_subtopic_detail_page(section):
    """
    Renders the dedicated page for a single subtopic's content.
    """
    topic_title = st.session_state.get("current_subtopic_title", "Guidance")
    content = st.session_state.get("viewing_subtopic_content", "No content available.")

    st.header(f"✝️ {topic_title}")
    st.markdown("---")
    st.markdown(content, unsafe_allow_html=True)
    st.markdown("---")

    if st.button(f"⬅️ Back to {section} Topics"):
        st.session_state.viewing_subtopic_content = None
        st.session_state.current_subtopic_title = None
        st.rerun()


def show_subtopics(section):
    """
    Acts as a router. Shows either the list of subtopics or the detail page for one subtopic.
    """
    # Initialize session state keys for this component if they don't exist
    if "viewing_subtopic_content" not in st.session_state:
        st.session_state.viewing_subtopic_content = None
    if "current_subtopic_title" not in st.session_state:
        st.session_state.current_subtopic_title = None

    # --- ROUTER LOGIC ---
    if st.session_state.get("viewing_subtopic_content"):
        render_subtopic_detail_page(section)
        return

    # --- SUBTOPIC LIST PAGE ---
    st.markdown(f"## ✝️ You selected: **{section}**")

    # Section for Predefined Topics
    if section in topics_map:
        st.markdown("### 📚 Choose a topic for instant guidance:")
        cols = st.columns(2)
        for i, topic in enumerate(topics_map[section]):
            if cols[i % 2].button(topic, key=f"topic_{i}"):
                # **CORRECTED**: Using a more natural loading message
                with st.spinner(f"Let's reflect on '{topic}'..."):
                    content = generate_spiritual_guidance(topic, section)
                    st.session_state.viewing_subtopic_content = content
                    st.session_state.current_subtopic_title = topic
                st.rerun()

    st.markdown("---")

    # Section for Custom Topics
    st.markdown("### ✍️ Or enter a custom topic:")
    custom_topic = st.text_input("Your custom topic", key="custom_input", label_visibility="collapsed")

    if st.button("🕊️ Get Guidance for Custom Topic", use_container_width=True):
        final_topic = custom_topic.strip()
        if not final_topic:
            st.warning("Please enter a topic in the text box above.")
        else:
            # **CORRECTED**: Using a more natural loading message
            with st.spinner(f"Thinking about '{final_topic}' for you..."):
                content = generate_spiritual_guidance(final_topic, section)
                st.session_state.viewing_subtopic_content = content
                st.session_state.current_subtopic_title = final_topic
            st.rerun()

    st.markdown("---")
    if st.button("🔙 Back to Home"):
        for key in ["viewing_subtopic_content", "current_subtopic_title", "selected_section"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.page = "menu"
        st.rerun()

