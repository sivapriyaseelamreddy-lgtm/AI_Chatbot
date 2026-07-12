import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database", "chatbot.db")

SYSTEM_PROMPT = """You are a helpful, knowledgeable, and friendly AI assistant. 
You provide clear, accurate, and thoughtful responses. 
You maintain context throughout the conversation and remember what was discussed earlier.
When appropriate, use markdown formatting to make your responses more readable."""
