import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from backend.app.database.connection import Base

UUID_TYPE = UUID(as_uuid=True)

class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4, index=True)
    interview_id = Column(UUID_TYPE, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    audio_path = Column(String, nullable=True)
    order_index = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
