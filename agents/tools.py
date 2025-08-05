# agents/tools.py

import json
from datetime import datetime, timedelta
import streamlit as st

# Imports for Google API
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Import the chains from our base agent file
from agents.base_chain import (
    get_devotional_conversation_chain,
    get_just_chat_conversation_chain,
    load_groq_llm
)
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


# --- Tool 1: Get Spiritual Guidance ---
def handle_guidance_request(topic: str, category: str = "General") -> str:
    """Generates a spiritual guidance article for a given topic."""
    chain = get_devotional_conversation_chain()
    if not chain:
        return "Error: Could not initialize the spiritual guidance generator."

    prompt = f"""
    You are a compassionate and wise Christian spiritual guide. Your task is to write a thoughtful and encouraging piece of guidance on the topic of "{topic}" within the context of "{category}".
    Please structure your response in the following format, using Markdown for formatting:
    ### A Spiritual Perspective on {topic}
    Start with a brief, empathetic introduction...
    ---
    #### Key Biblical Principles and Practices
    Present 4 to 5 practical, actionable points... Include Bible verses with references.
    ---
    #### A Final Message of Encouragement
    Conclude with a warm, uplifting message...
    """
    return chain.run(prompt)


# --- Tool 2: Get an Inspirational Post ---
def handle_inspiration_request() -> str:
    """Returns a formatted inspirational post."""
    return """
    ### A Moment of Peace
    ![Peaceful Scene](https://picsum.photos/seed/1/600/300)
    > "Do not be anxious about anything, but in every situation, by prayer and petition, 
    > with thanksgiving, present your requests to God. And the peace of God, which transcends 
    > all understanding, will guard your hearts and your minds in Christ Jesus."
    >
    > **Philippians 4:6-7**
    """


# --- Tool 3: Get SOS Support ---
def handle_sos_request() -> str:
    """Returns an immediate SOS support message."""
    return """
    ### A Prayer for You in Your Time of Need
    I am here with you. Please take a deep breath.
    > Heavenly Father, I come before you in this moment of distress. I lift up this dear soul to you. Surround them with Your peace that surpasses all understanding. Be their rock, their fortress, and their deliverer. Remind them that they are not alone, for You are with them. In Jesus' name, Amen.
    """


# --- Tool 4: Handle General Chat ---
def handle_general_chat(user_input: str, memory) -> str:
    """Handles a general, non-specific chat conversation."""
    chain = get_just_chat_conversation_chain(memory)
    if chain:
        return chain.run(user_input)
    return "I'm sorry, the chat service is currently unavailable."


# --- Tool 5: Handle Calendar Scheduling ---
def handle_scheduling_request(user_prompt: str, token: dict) -> str:
    """Parses a user's request and schedules events on their Google Calendar."""
    llm = load_groq_llm()
    if not llm:
        return "Error: The scheduling AI is unavailable."

    current_date = datetime.now().strftime("%A, %Y-%m-%d")
    template = f"""You are an expert at extracting structured data from natural language for calendar scheduling. Your task is to analyze the user's request and output a JSON object.
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
        response_str = chain.run(user_prompt=user_prompt)
        schedule_data = json.loads(response_str)

        title = schedule_data.get("title", "Untitled Event")
        start_date_str = schedule_data.get("start_date")
        time_str = schedule_data.get("time")
        days = int(schedule_data.get("days", 1))

        creds = Credentials(token=token['access_token'], refresh_token=token.get('refresh_token'),
                            token_uri="https://oauth2.googleapis.com/token",
                            client_id=st.secrets["google_credentials"]["CLIENT_ID"],
                            client_secret=st.secrets["google_credentials"]["CLIENT_SECRET"],
                            scopes=["https://www.googleapis.com/auth/calendar.events"])

        service = build('calendar', 'v3', credentials=creds)
        start_date = datetime.fromisoformat(start_date_str)

        for i in range(days):
            current_date = start_date + timedelta(days=i)
            start_datetime = datetime.fromisoformat(f"{current_date.strftime('%Y-%m-%d')}T{time_str}")
            end_datetime = start_datetime + timedelta(hours=1)
            event = {'summary': title,
                     'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'Asia/Kolkata'},
                     'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'Asia/Kolkata'}}
            service.events().insert(calendarId='primary', body=event).execute()

        return f"Success! I've scheduled '{title}' for {days} day(s), starting {start_date_str}."

    except Exception as e:
        return f"I'm sorry, I couldn't schedule that. An error occurred: {e}"

