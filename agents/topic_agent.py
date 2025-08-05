# agents/topic_agent.py

# We import the conversation chain from the base agent
from agents.base_chain import get_devotional_conversation_chain

def generate_spiritual_guidance(topic, category):
    """
    Generates a well-structured spiritual guidance article on a given topic.
    """
    chain = get_devotional_conversation_chain()
    if not chain:
        return "Error: Could not initialize the spiritual guidance generator."

    # This is the new, detailed prompt that asks for an article, not a plan.
    prompt = f"""
    You are a compassionate and wise Christian spiritual guide. Your task is to write a thoughtful and encouraging piece of guidance on the topic of "{topic}" within the context of "{category}".

    Please structure your response in the following format, using Markdown for formatting. Keep the entire response concise and to the point.

    ### A Spiritual Perspective on {topic}

    Start with a brief, empathetic introduction that acknowledges the user's interest or struggle with this topic.

    ---

    #### Key Biblical Principles and Practices

    Present 2 to 3 concise, actionable points based on Biblical teachings. For each point:
    - Use a bolded heading (e.g., "**1. Embrace Prayer**").
    - Explain the principle clearly and compassionately in a brief paragraph.
    - Include one relevant Bible verse to support the point, quoting it and providing the reference (e.g., "Philippians 4:6").

    ---

    #### A Final Message of Encouragement

    Conclude with a warm, uplifting message that leaves the user with a sense of hope and peace.

    Ensure the entire response is well-written, spiritually sound, and easy to read.
    """

    response = chain.run(prompt)
    return response
