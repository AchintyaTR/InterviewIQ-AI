import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from backend.app.database.connection import Base

UUID_TYPE = UUID(as_uuid=True)

class Response(Base):
    __tablename__ = "responses"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4, index=True)
    question_id = Column(UUID_TYPE, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    response_text = Column(Text, nullable=False)
    audio_path = Column(String, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
