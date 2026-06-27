import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Float, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from backend.app.database.connection import Base

UUID_TYPE = UUID(as_uuid=True)

class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4, index=True)
    interview_id = Column(UUID_TYPE, ForeignKey("interviews.id", ondelete="CASCADE"), unique=True, nullable=False)
    score_overall = Column(Float, nullable=False)
    score_metrics = Column(JSON, nullable=True)  # Breakdown scores
    feedback_text = Column(Text, nullable=False)
    learning_roadmap = Column(JSON, nullable=True)  # Personalized learning path
    question_evaluations = Column(JSON, nullable=True) # Question by question breakdown
    created_at = Column(DateTime, default=datetime.utcnow)
