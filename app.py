from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
import google.generativeai as genai
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI(title="Social Media Reply Generator")

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI"))

# System Prompt
SYSTEM_PROMPT = """
You are a highly skilled social media expert tasked with generating authentic, human-like replies to social media posts. Follow these steps:

1. **Tone Detection**: Analyze the post's tone (e.g., casual, professional, excited, serious) and match it in the reply.
2. **Intent Understanding**: Identify the post's intent (e.g., sharing news, asking a question, expressing emotion) and tailor the reply to engage appropriately.
3. **Platform Adaptation**: Adjust the reply's style to suit the platform:
   - Twitter: Concise (up to 280 characters), conversational, may include hashtags or emojis.
   - LinkedIn: Professional, thoughtful, often encouraging or insightful.
   - Instagram: Friendly, visual-oriented, casual with emojis.
4. **Human-like Nuances**: Use natural language, avoid repetitive phrases, and incorporate platform-specific slang or trends. Avoid excessive formality or generic responses.
5. **Contextual Relevance**: Ensure the reply directly addresses the post's content, adding value (e.g., a relevant comment, question, or compliment).

Example:
Post (Twitter): "Just launched my new app! 🚀 So excited! #Tech"
Reply: "Congrats on the launch! 🎉 What's the app about? #TechLife"

Generate a reply that feels like it was written by a real person, staying concise and engaging.
"""

# Pydantic Models
class PostRequest(BaseModel):
    platform: Literal["Twitter", "LinkedIn", "Instagram"]
    post_text: str

class PostResponse(BaseModel):
    platform: str
    post_text: str
    generated_reply: str
    timestamp: str

# Database Setup
def init_db():
    conn = sqlite3.connect("replies.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            post_text TEXT,
            generated_reply TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Generate Reply
async def generate_reply(platform: str, post_text: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    prompt = f"{SYSTEM_PROMPT}\n\nPlatform: {platform}\nPost: {post_text}\nReply:"
    response = model.generate_content(prompt)
    return response.text.strip()

# Save to Database
def save_reply(platform: str, post_text: str, generated_reply: str):
    conn = sqlite3.connect("replies.db")
    c = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    c.execute(
        "INSERT INTO replies (platform, post_text, generated_reply, timestamp) VALUES (?, ?, ?, ?)",
        (platform, post_text, generated_reply, timestamp)
    )
    conn.commit()
    conn.close()
    return timestamp

# API Endpoint
@app.post("/reply", response_model=PostResponse)
async def create_reply(post: PostRequest):
    try:
        # Generate reply
        generated_reply = await generate_reply(post.platform, post.post_text)
        
        # Save to database
        timestamp = save_reply(post.platform, post.post_text, generated_reply)
        
        # Return response
        return PostResponse(
            platform=post.platform,
            post_text=post.post_text,
            generated_reply=generated_reply,
            timestamp=timestamp
        )
    except Exception as e:
        import traceback
        print(f"Error in create_reply: {str(e)}")
        print(traceback.format_exc()) # This will print the full traceback
        raise HTTPException(status_code=500, detail=f"Error generating reply: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "Social Media Reply Generator is running. Use the /reply endpoint to generate replies."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)