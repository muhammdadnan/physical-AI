from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from .database import Base


class ChatLog(Base):
    """
    Database model for storing chat logs in Neon Postgres
    """
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # User identifier
    query = Column(Text)  # User query
    answer = Column(Text)  # System response
    timestamp = Column(DateTime, default=func.now())  # When the interaction occurred
    query_type = Column(String, default="general")  # Type of query (general, selected_text_only, etc.)
    session_id = Column(String, index=True)  # Session identifier
    latency = Column(Float)  # Response time in seconds
    metadata_json = Column(Text)  # Additional metadata as JSON string