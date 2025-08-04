# agents/topic_agent.py

from agents.base_chain import get_conversation_chain

def generate_daily_program(topic, category):
    chain = get_conversation_chain()

    prompt = f"""
    You're a Christian spiritual assistant. Create a 7-day devotional plan for the category: {category} and topic: {topic}.
    Each day should include:
    - A short Bible verse (with reference)
    - A one-line prayer
    - A faith declaration
    - A brief theme title

    Keep each day short and powerful.
    """

    response = chain.run(prompt)
    return response
