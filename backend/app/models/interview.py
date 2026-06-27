import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from backend.app.database.connection import Base

UUID_TYPE = UUID(as_uuid=True)

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID_TYPE, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resume_id = Column(UUID_TYPE, ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True)
    target_role = Column(String, nullable=False)
    target_company = Column(String, nullable=False)
    interview_mode = Column(String, default="voice") # voice or text
    status = Column(String, default="scheduled")  # scheduled, in_progress, completed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
