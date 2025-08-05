# agents/base_chain.py

import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain, LLMChain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

def load_groq_llm():
    """Loads the Groq LLM from secrets."""
    try:
        groq_api_key = st.secrets["groq_credentials"]["GROQ_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error("Groq API key not found.")
        return None
    return ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

def get_devotional_conversation_chain():
    """This chain is now only used by the guidance tool."""
    llm = load_groq_llm()
    if llm:
        return ConversationChain(llm=llm, memory=ConversationBufferMemory(), verbose=True)
    return None

def get_just_chat_conversation_chain(memory):
    """This chain is for general chat and now accepts a memory object."""
    llm = load_groq_llm()
    if llm:
        template = """You are a compassionate, wise, and kind Christian spiritual companion named DSCPL. 
        Your purpose is to provide comfort, encouragement, and guidance based on Christian principles. 
        You are not a therapist, but a supportive friend. Listen carefully to the user, respond with empathy, 
        and gently offer a spiritual perspective or a relevant Bible verse if it feels appropriate. 
        Keep your responses conversational and not overly preachy.

        Current conversation:
        {history}
        Human: {input}
        AI:"""
        PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
        return ConversationChain(llm=llm, memory=memory, prompt=PROMPT, verbose=True)
    return None

def get_router_chain():
    """
    This is the new master agent. It classifies the user's intent and
    returns a JSON object indicating which tool to use.
    """
    llm = load_groq_llm()
    if llm:
        template = """
You are a master routing agent. Your job is to analyze the user's request and determine which tool is most appropriate to handle it.
You must respond with ONLY a JSON object with two keys: "tool" and "input".

Here are the available tools and when to use them:
- "guidance": Use when the user asks for help, advice, or a devotional on a specific spiritual or life topic (e.g., "help me with stress", "tell me about forgiveness"). The "input" should be the topic.
- "scheduling": Use when the user wants to set a reminder or schedule something on their calendar. The "input" should be the user's full request.
- "inspiration": Use for requests for an inspirational quote, image, or message. The "input" should be "None".
- "sos": Use for urgent requests for help, prayer, or support (e.g., "I need help now", "SOS"). The "input" should be "None".
- "chat": Use for general conversation, greetings, or any request that doesn't fit the other tools. The "input" should be the user's full request.

User Request: {user_prompt}
JSON Response:
"""
        PROMPT = PromptTemplate(input_variables=["user_prompt"], template=template)
        return LLMChain(llm=llm, prompt=PROMPT, verbose=True)
    return None
