import os
import pandas as pd
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
from database import init_db, save_reply
import asyncio

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI"))

# System Prompt (same as in app.py)
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

async def generate_reply(platform: str, post_text: str) -> str:
    """Generate a reply using Gemini AI."""
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    prompt = f"{SYSTEM_PROMPT}\n\nPlatform: {platform}\nPost: {post_text}\nReply:"
    response = model.generate_content(prompt)
    return response.text.strip()

async def process_post(platform, post_text):
    """Process a single post and save to database."""
    try:
        # Generate reply
        generated_reply = await generate_reply(platform, post_text)
        
        # Create timestamp
        timestamp = datetime.utcnow().isoformat()
        
        # Save to database
        save_reply(platform, post_text, generated_reply, timestamp)
        
        print(f"Processed post: {post_text[:50]}...")
        print(f"Generated reply: {generated_reply[:50]}...")
        print("-" * 50)
        
        return True
    except Exception as e:
        print(f"Error processing post: {str(e)}")
        return False

async def process_csv(csv_path, limit=None):
    """Process posts from a CSV file and save replies to the database."""
    try:
        # Initialize database
        init_db()
        
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Check if required columns exist
        if 'platform' not in df.columns or 'post_text' not in df.columns:
            # Try to infer columns
            if len(df.columns) >= 2:
                df.columns = ['platform', 'post_text'] + list(df.columns[2:])
            else:
                raise ValueError("CSV file must have at least 'platform' and 'post_text' columns")
        
        # Limit the number of posts to process if specified
        if limit and limit > 0:
            df = df.head(limit)
        
        # Process each post
        success_count = 0
        for index, row in df.iterrows():
            platform = row['platform']
            post_text = row['post_text']
            
            # Skip empty posts
            if pd.isna(platform) or pd.isna(post_text) or not platform or not post_text:
                continue
                
            success = await process_post(platform, post_text)
            if success:
                success_count += 1
        
        print(f"Successfully processed {success_count} out of {len(df)} posts.")
        
    except Exception as e:
        print(f"Error processing CSV: {str(e)}")

if __name__ == "__main__":
    import sys
    
    # Default CSV path
    csv_path = "posts.csv"
    
    # Default limit (process all posts)
    limit = None
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    
    if len(sys.argv) > 2:
        try:
            limit = int(sys.argv[2])
        except ValueError:
            print(f"Invalid limit: {sys.argv[2]}. Using all posts.")
    
    print(f"Processing CSV file: {csv_path}")
    if limit:
        print(f"Processing up to {limit} posts")
    
    # Run the async function
    asyncio.run(process_csv(csv_path, limit))