# agents/topic_agent.py

# We now import the specific chain for devotionals
from agents.base_chain import get_devotional_conversation_chain

def generate_daily_program(topic, category):
    # Use the devotional chain
    chain = get_devotional_conversation_chain()
    if not chain:
        return "Error: Could not initialize the devotional plan generator."

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
