# components/just_chat.py

import streamlit as st
import json
from langchain.memory import ConversationBufferMemory

# Import the router and the tool handlers
from agents.base_chain import get_router_chain
from agents.tools import (
    handle_guidance_request,
    handle_scheduling_request,
    handle_inspiration_request,
    handle_sos_request,
    handle_general_chat
)

# Import the OAuth component for calendar login
from streamlit_oauth import OAuth2Component


def show_just_chat():
    """
    A multi-purpose chat page with a context-aware Google Calendar login button.
    """
    st.markdown("## Just Chat")
    st.markdown("_Your personal space to talk, reflect, schedule, and find encouragement._")

    # --- Initialize Session State ---
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [{"role": "assistant",
                                           "content": "Hello! How can I support you today? You can ask for guidance, schedule a reminder, or just talk."}]
    if "chat_memory" not in st.session_state:
        st.session_state.chat_memory = ConversationBufferMemory(human_prefix="Human", ai_prefix="AI")
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'show_calendar_login' not in st.session_state:
        st.session_state.show_calendar_login = False

    # --- Sidebar for Actions ---
    with st.sidebar:
        st.header("Actions")

        def clear_chat_history():
            """Resets the chat history, memory, and related states."""
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "Chat cleared! How can I help you next?"}]
            st.session_state.chat_memory = ConversationBufferMemory(human_prefix="Human", ai_prefix="AI")
            st.session_state.show_calendar_login = False

        st.button("Clear Chat", on_click=clear_chat_history, use_container_width=True, key="clear_chat_button")

        st.markdown("---")

        if st.button("🔙 Back to Home", key="chat_back_home", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()

    # --- Display Chat History ---
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Main Chat Input Logic ---
    if prompt := st.chat_input("Ask for guidance, schedule a reminder, or just talk..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                router_chain = get_router_chain()
                if not router_chain:
                    st.error("The main agent is unavailable. Please check API key setup.")
                else:
                    try:
                        response_str = router_chain.run(user_prompt=prompt)
                        router_result = json.loads(response_str)
                        tool = router_result.get("tool")
                        tool_input = router_result.get("input")

                        ai_response = ""

                        if tool == "scheduling":
                            if not st.session_state.token:
                                ai_response = "To schedule reminders, you first need to connect your Google Calendar. Please use the button below to log in."
                                st.session_state.show_calendar_login = True
                            else:
                                ai_response = handle_scheduling_request(user_prompt=tool_input,
                                                                        token=st.session_state.token)
                        else:
                            st.session_state.show_calendar_login = False
                            if tool == "guidance":
                                ai_response = handle_guidance_request(topic=tool_input)
                            elif tool == "inspiration":
                                ai_response = handle_inspiration_request()
                            elif tool == "sos":
                                ai_response = handle_sos_request()
                            else:
                                ai_response = handle_general_chat(user_input=tool_input,
                                                                  memory=st.session_state.chat_memory)

                        if ai_response:
                            st.markdown(ai_response)
                            st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})

                    except Exception as e:
                        error_message = f"I'm sorry, I encountered an error: {e}"
                        st.error(error_message)
                        st.session_state.chat_messages.append({"role": "assistant", "content": error_message})

        st.rerun()

    # --- Google Calendar Login/Logout Button (conditional display) ---
    st.markdown("---")
    if st.session_state.token:
        if st.button("Disconnect Google Calendar", key="disconnect_chat_cal"):
            st.session_state.token = None
            st.session_state.show_calendar_login = False
            st.rerun()
    elif st.session_state.get('show_calendar_login', False):
        try:
            CLIENT_ID = st.secrets["google_credentials"]["CLIENT_ID"]
            CLIENT_SECRET = st.secrets["google_credentials"]["CLIENT_SECRET"]
            # **CORRECTED**: Use a redirect URI from secrets for deployment flexibility
            REDIRECT_URI = st.secrets["google_credentials"]["REDIRECT_URI"]

            oauth2 = OAuth2Component(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                     authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
                                     token_endpoint="https://oauth2.googleapis.com/token")

            result = oauth2.authorize_button(name="Connect Google Calendar", icon="https://www.google.com/favicon.ico",
                                             redirect_uri=REDIRECT_URI,  # <-- THIS IS THE FIX
                                             scope="https://www.googleapis.com/auth/calendar.events",
                                             use_container_width=True, pkce='S256', key="connect_chat_cal")
            if result and "token" in result:
                st.session_state.token = result['token']
                st.session_state.show_calendar_login = False
                st.rerun()
        except (KeyError, FileNotFoundError) as e:
            st.error(
                f"Google Calendar connection is not configured correctly. Please check your secrets. Missing key: {e}")

