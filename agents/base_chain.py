# agents/base_chain.py

import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq

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

def get_conversation_chain():
    llm = load_groq_llm()
    # Ensure the LLM was loaded successfully before creating the chain
    if llm:
        memory = ConversationBufferMemory()
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        return chain
    return None