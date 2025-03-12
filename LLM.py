import os

from groq import Groq

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

groq_llm = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "An AI assistant optimized for summarizing news content in short and efficiently."
        }
    ],
    model="llama-3.3-70b-versatile",
)

