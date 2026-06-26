import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from backend.app.database.connection import Base

UUID_TYPE = UUID(as_uuid=True)

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID_TYPE, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String, nullable=False)
    extracted_skills = Column(JSON, nullable=True)  # Fallback JSON type for cross-db support
    extracted_experience = Column(JSON, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
