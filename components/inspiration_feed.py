# components/inspiration_feed.py

import streamlit as st

def show_inspiration_feed():
    st.markdown("## ✨ Inspiration Feed")
    st.markdown("_A curated feed of uplifting content to brighten your day._")
    st.info("This feature is under development. The content below is for demonstration.")
    st.markdown("---")

    # --- Post 1: Quote ---
    st.subheader("A Moment of Peace")
    # Using a reliable service for placeholder images. The number at the end makes it a unique image.
    st.image("https://picsum.photos/seed/1/600/300", caption="Photo by Picsum")
    st.markdown(
        """
        > "Do not be anxious about anything, but in every situation, by prayer and petition, 
        > with thanksgiving, present your requests to God. And the peace of God, which transcends 
        > all understanding, will guard your hearts and your minds in Christ Jesus."
        >
        > **Philippians 4:6-7**
        """
    )
    st.markdown("---")

    # --- Post 2: Thought ---
    st.subheader("Strength for the Journey")
    st.image("https://picsum.photos/seed/2/600/300", caption="Photo by Picsum")
    st.markdown(
        """
        <p style='text-align: justify;'>
        Remember that every step, no matter how small, is progress. Your journey is unique, 
        and your strength comes from a source greater than yourself. Embrace the challenges 
        of today, for they are shaping the person you are becoming tomorrow. You are not alone.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # --- Post 3: Short encouragement ---
    st.subheader("A Simple Reminder")
    st.image("https://picsum.photos/seed/3/600/300", caption="Photo by Picsum")
    st.success(
        """
        **Declaration:** I can do all things through Christ who strengthens me.
        """
    )

    # --- Back to Home Button ---
    st.markdown("---")
    if st.button("🔙 Back to Home"):
        st.session_state.page = "menu"
        st.rerun()