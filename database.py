import os
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Text, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Check if we should use Neon.tech PostgreSQL or fallback to SQLite
USE_NEON = os.getenv("USE_NEON", "false").lower() == "true"
NEON_DB_URL = os.getenv("NEON_DB_URL")

Base = declarative_base()

class Reply(Base):
    __tablename__ = "replies"
    
    id = Column(Integer, primary_key=True)
    platform = Column(String(50))
    post_text = Column(Text)
    generated_reply = Column(Text)
    timestamp = Column(String(50))

def get_engine():
    if USE_NEON and NEON_DB_URL:
        # Use Neon.tech PostgreSQL
        return create_engine(NEON_DB_URL)
    else:
        # Fallback to SQLite
        return create_engine("sqlite:///replies.db")

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    
    # For backward compatibility, also initialize SQLite directly
    if not USE_NEON:
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

def save_reply(platform: str, post_text: str, generated_reply: str, timestamp: str):
    if USE_NEON and NEON_DB_URL:
        # Use SQLAlchemy with Neon.tech
        engine = get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        
        new_reply = Reply(
            platform=platform,
            post_text=post_text,
            generated_reply=generated_reply,
            timestamp=timestamp
        )
        
        session.add(new_reply)
        session.commit()
        session.close()
    else:
        # Fallback to SQLite
        conn = sqlite3.connect("replies.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO replies (platform, post_text, generated_reply, timestamp) VALUES (?, ?, ?, ?)",
            (platform, post_text, generated_reply, timestamp)
        )
        conn.commit()
        conn.close()