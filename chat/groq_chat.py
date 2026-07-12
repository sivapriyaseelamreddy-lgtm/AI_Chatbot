from groq import Groq, APIStatusError, AuthenticationError
from config import GROQ_API_KEY, GROQ_MODEL, SYSTEM_PROMPT


def get_groq_client():
    """Initialize and return the Groq client."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Please check your .env file.")
    return Groq(api_key=GROQ_API_KEY)


def build_messages(conversation_history, user_message):
    """
    Build the messages list for the Groq API call.
    Includes system prompt and full conversation history for context.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for entry in conversation_history:
        role = entry["role"]
        if role in ("user", "assistant"):
            messages.append({"role": role, "content": entry["message"]})

    messages.append({"role": "user", "content": user_message})
    return messages


def chat_with_groq(conversation_history, user_message):
    """
    Send a message to the Groq API and return the AI response.
    
    Args:
        conversation_history: List of previous messages for context
        user_message: The current user message
    
    Returns:
        str: The AI's response text
    """
    client = get_groq_client()
    messages = build_messages(conversation_history, user_message)

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
        )
        return completion.choices[0].message.content
    except AuthenticationError:
        raise ValueError(
            "Invalid or expired Groq API Key. Please update your .env file with a valid key from https://console.groq.com/keys"
        )
    except APIStatusError as e:
        raise ValueError(f"Groq API error: {e.message}")


def generate_title(user_message):
    """
    Generate a short, descriptive title for a conversation based on the first message.
    
    Args:
        user_message: The first user message in the conversation
    
    Returns:
        str: A short title for the conversation
    """
    client = get_groq_client()
    prompt = f"""Generate a very short title (3-6 words max) for a conversation that starts with this message: "{user_message}"
    
    Rules:
    - Maximum 6 words
    - No quotes or punctuation at the end
    - Be descriptive and concise
    - Capitalize the first letter of each important word
    
    Return ONLY the title, nothing else."""

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=20,
    )

    title = completion.choices[0].message.content.strip().strip('"').strip("'")
    return title[:60] if title else "New Conversation"
