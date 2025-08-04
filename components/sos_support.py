# components/sos_support.py

import streamlit as st
import time

def show_sos_support():
    st.markdown("## 🆘 SOS Support")
    st.markdown("In moments of crisis, find immediate spiritual support here.")

    if st.button("🙏 I need immediate prayer and support"):
        with st.spinner("Connecting you with an emergency spiritual resource..."):
            time.sleep(3) # Simulate loading
        st.success("Connected!")
        st.markdown("### A Prayer for You in Your Time of Need:")
        st.text_area(
            "Prayer",
            "Heavenly Father, I come before you in this moment of distress. I lift up this dear soul to you. Surround them with Your peace that surpasses all understanding. Be their rock, their fortress, and their deliverer. In Jesus' name, Amen.",
            height=150
        )

    if st.button("🔙 Back to Home"):
        st.session_state.page = "menu"
        st.session_state.selected_section = None