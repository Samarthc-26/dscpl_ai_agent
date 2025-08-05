# agents/base_chain.py

import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate


def load_groq_llm():
    """
    Loads the Groq LLM, fetching the API key from Streamlit's secrets.
    """
    try:
        groq_api_key = st.secrets["groq_credentials"]["GROQ_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error("Groq API key not found. Please add it to your .streamlit/secrets.toml file.")
        return None

    return ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama3-70b-8192"
    )


def get_devotional_conversation_chain():
    """
    This chain is specifically for generating the 7-day devotional plans.
    """
    llm = load_groq_llm()
    if llm:
        memory = ConversationBufferMemory()
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        return chain
    return None


def get_just_chat_conversation_chain():
    """
    This is the chain for the "Just Chat" feature.
    """
    llm = load_groq_llm()
    if llm:
        template = """
        You are a compassionate, wise, and kind Christian spiritual companion named DSCPL. 
        Your purpose is to provide comfort, encouragement, and guidance based on Christian principles. 
        You are not a therapist, but a supportive friend. Listen carefully to the user, respond with empathy, 
        and gently offer a spiritual perspective or a relevant Bible verse if it feels appropriate. 
        Keep your responses conversational and not overly preachy.

        Current conversation:
        {history}
        Human: {input}
        AI:"""

        PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

        memory = ConversationBufferMemory(human_prefix="Human", ai_prefix="AI")
        chain = ConversationChain(llm=llm, memory=memory, prompt=PROMPT, verbose=True)
        return chain
    return None
