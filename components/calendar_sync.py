# components/calendar_sync.py

import streamlit as st
from datetime import datetime, timedelta
import json

# Imports for Google API
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import the necessary components from LangChain and our agents
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from agents.base_chain import load_groq_llm
from streamlit_oauth import OAuth2Component


def schedule_events_on_calendar(title, start_date_str, time_str, days):
    """Helper function to connect to Google Calendar and create events."""
    try:
        # This function correctly uses the token from session_state
        token_info = st.session_state.token
        CLIENT_ID = st.secrets["google_credentials"]["CLIENT_ID"]
        CLIENT_SECRET = st.secrets["google_credentials"]["CLIENT_SECRET"]
        TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
        SCOPE = "https://www.googleapis.com/auth/calendar.events"

        creds = Credentials(
            token=token_info['access_token'],
            refresh_token=token_info.get('refresh_token'),
            token_uri=TOKEN_ENDPOINT,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scopes=[SCOPE]
        )
        service = build('calendar', 'v3', credentials=creds)
        start_date = datetime.fromisoformat(start_date_str)

        for i in range(days):
            current_date = start_date + timedelta(days=i)
            start_datetime_str = f"{current_date.strftime('%Y-%m-%d')}T{time_str}"
            start_datetime = datetime.fromisoformat(start_datetime_str)
            end_datetime = start_datetime + timedelta(hours=1)

            event = {
                'summary': title,
                'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'Asia/Kolkata'},
                'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'Asia/Kolkata'},
            }
            service.events().insert(calendarId='primary', body=event).execute()

        success_message = f"Done! I've scheduled '{title}' for {days} day(s)."
        st.success(success_message)
        st.balloons()
        st.session_state.calendar_chat_messages.append({"role": "assistant", "content": success_message})

    except Exception as e:
        error_message = f"An error occurred during scheduling: {e}"
        st.error(error_message)
        st.session_state.calendar_chat_messages.append({"role": "assistant", "content": error_message})


def show_calendar_sync():
    st.markdown("## 🗓️ AI-Powered Scheduling")
    st.markdown("Connect your calendar and simply tell me what you want to schedule.")
    st.markdown("---")

    try:
        CLIENT_ID = st.secrets["google_credentials"]["CLIENT_ID"]
        CLIENT_SECRET = st.secrets["google_credentials"]["CLIENT_SECRET"]
        # **CORRECTED**: Load the redirect URI from secrets here as well
        REDIRECT_URI = st.secrets["google_credentials"]["REDIRECT_URI"]
    except (KeyError, FileNotFoundError) as e:
        st.error(f"Google credentials not found in secrets. Please check your configuration. Missing key: {e}")
        return

    oauth2 = OAuth2Component(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                             authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
                             token_endpoint="https://oauth2.googleapis.com/token")

    if 'token' not in st.session_state:
        st.session_state.token = None
    if "calendar_chat_messages" not in st.session_state:
        st.session_state.calendar_chat_messages = []

    if st.session_state.token:
        st.success("Your Google Calendar is successfully connected!")

        for message in st.session_state.calendar_chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("e.g., 'Schedule prayer for 5 days from tomorrow at 8am'"):
            st.session_state.calendar_chat_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing your request..."):
                    llm = load_groq_llm()
                    if llm:
                        current_date = datetime.now().strftime("%A, %Y-%m-%d")
                        template = f"""You are an expert at extracting structured data from natural language. Your task is to analyze the user's request to schedule a reminder and output a JSON object.
Current date is: {current_date}. Use this as a reference for terms like 'today', 'tomorrow', or day names like 'next Monday'.
You MUST extract the following fields:
- "title": The title of the event.
- "start_date": The starting date in "YYYY-MM-DD" format.
- "time": The time of the event in "HH:MM:SS" (24-hour) format. If no time is mentioned, default to "09:00:00".
- "days": The total number of days the event should be scheduled for. If not mentioned, default to 1.
Your response MUST be ONLY the JSON object and nothing else. Do not add any explanatory text.
User request: {{user_prompt}}
JSON output:
"""
                        PROMPT = PromptTemplate(input_variables=["user_prompt"], template=template)
                        chain = LLMChain(llm=llm, prompt=PROMPT, verbose=True)

                        try:
                            response_str = chain.run(user_prompt=prompt)
                            schedule_data = json.loads(response_str)

                            title = schedule_data.get("title", "Untitled Event")
                            start_date_str = schedule_data.get("start_date")
                            time_str = schedule_data.get("time")
                            days = int(schedule_data.get("days", 1))

                            info_message = f"Okay, scheduling **'{title}'** for **{days} day(s)**, starting **{start_date_str}** at **{time_str}**."
                            st.info(info_message)
                            st.session_state.calendar_chat_messages.append(
                                {"role": "assistant", "content": info_message})

                            schedule_events_on_calendar(title, start_date_str, time_str, days)

                        except json.JSONDecodeError:
                            err_msg = "I'm sorry, I couldn't understand that. Could you please try rephrasing?"
                            st.error(err_msg)
                            st.session_state.calendar_chat_messages.append({"role": "assistant", "content": err_msg})
                        except Exception as e:
                            err_msg = f"An unexpected error occurred: {e}"
                            st.error(err_msg)
                            st.session_state.calendar_chat_messages.append({"role": "assistant", "content": err_msg})
                    else:
                        st.error("The scheduling agent is currently unavailable.")

        st.markdown("---")
        if st.button("Disconnect Calendar"):
            st.session_state.token = None
            st.rerun()
    else:
        st.info("Connect your account to get started.")
        # **CORRECTED**: The button now uses the REDIRECT_URI from your secrets
        result = oauth2.authorize_button(name="Connect to Google Calendar", icon="https://www.google.com/favicon.ico",
                                         redirect_uri=REDIRECT_URI,
                                         scope="https://www.googleapis.com/auth/calendar.events",
                                         use_container_width=True, pkce='S256')
        if result and "token" in result:
            st.session_state.token = result['token']
            st.rerun()

    st.markdown("---")
    if st.button("🔙 Back to Home"):
        st.session_state.page = "menu"
        st.rerun()
