# components/calendar_sync.py

import streamlit as st
import asyncio
from datetime import datetime

# New imports for Google API
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from streamlit_oauth import OAuth2Component


def show_calendar_sync():
    """
    Handles Google Calendar OAuth and displays upcoming events.
    This version includes the fix for the Credentials TypeError.
    """
    st.markdown("## 🗓️ Sync with Your Google Calendar")
    st.markdown("Connect your Google Calendar to automatically schedule your spiritual plan.")
    st.markdown("---")

    try:
        CLIENT_ID = st.secrets["google_credentials"]["CLIENT_ID"]
        CLIENT_SECRET = st.secrets["google_credentials"]["CLIENT_SECRET"]
    except (KeyError, FileNotFoundError):
        st.error(
            "Google credentials not found. Please ensure you have a .streamlit/secrets.toml file with your credentials.")
        return

    AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    SCOPE = "https://www.googleapis.com/auth/calendar.events"

    oauth2 = OAuth2Component(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        authorize_endpoint=AUTHORIZE_ENDPOINT,
        token_endpoint=TOKEN_ENDPOINT,
    )

    if 'token' not in st.session_state:
        st.session_state.token = None

    if st.session_state.token:
        st.success("Your Google Calendar is successfully connected!")

        try:
            # ** FINAL FIX IS HERE **
            # Manually create the Credentials object from the token dictionary
            token_info = st.session_state.token
            creds = Credentials(
                token=token_info['access_token'],
                refresh_token=token_info.get('refresh_token'),
                token_uri=TOKEN_ENDPOINT,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                scopes=[SCOPE]
            )

            service = build('calendar', 'v3', credentials=creds)

            st.markdown("### Your Next 5 Upcoming Events:")
            with st.spinner("Fetching events from your calendar..."):
                now = datetime.utcnow().isoformat() + 'Z'
                events_result = service.events().list(
                    calendarId='primary', timeMin=now,
                    maxResults=5, singleEvents=True,
                    orderBy='startTime'
                ).execute()
                events = events_result.get('items', [])

            if not events:
                st.write("No upcoming events found.")
            else:
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    start_formatted = datetime.fromisoformat(start.replace('Z', '+00:00')).strftime(
                        '%a, %b %d at %I:%M %p')
                    st.write(f"- **{event['summary']}** on {start_formatted}")

        except HttpError as error:
            st.error(f"An error occurred: {error}")
            st.write("Your token may have expired. Please disconnect and reconnect.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

        st.markdown("---")
        if st.button("Disconnect Calendar"):
            st.session_state.token = None
            st.rerun()

    else:
        st.info("Connect your account to get started.")
        result = oauth2.authorize_button(
            name="Connect to Google Calendar",
            icon="https://www.google.com/favicon.ico",
            redirect_uri="http://localhost:8501",
            scope=SCOPE,
            use_container_width=True,
            pkce='S256'
        )

        if result and "token" in result:
            st.session_state.token = result['token']
            st.rerun()

    st.markdown("---")
    if st.button("🔙 Back to Home"):
        st.session_state.page = "menu"
        st.rerun()