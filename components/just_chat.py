# components/just_chat.py

import streamlit as st
from agents.base_chain import get_just_chat_conversation_chain

def show_just_chat():
    """
    Creates a dedicated chat page for spiritual conversation.
    """
    st.markdown("## 🙏 Just Chat")
    st.markdown("_Your personal space to talk, reflect, and find encouragement._")

    # Initialize the conversation chain and chat history in session state
    if 'just_chat_chain' not in st.session_state:
        st.session_state.just_chat_chain = get_just_chat_conversation_chain()
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display previous chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user input
    if prompt := st.chat_input("What is on your mind?"):
        # Add user message to chat history
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chain = st.session_state.just_chat_chain
                if chain is not None:
                    response = chain.run(prompt)
                    st.markdown(response)
                    # Add AI response to chat history
                    st.session_state.chat_messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Chat functionality is currently unavailable. Please check API key setup.")

    # --- Back to Home Button ---
    st.markdown("---")
    if st.button("🔙 Back to Home"):
        st.session_state.page = "menu"
        st.rerun()

