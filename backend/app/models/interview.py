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
    role_target = Column(String, nullable=False)
    company_target = Column(String, nullable=False)
    status = Column(String, default="scheduled")  # scheduled, in_progress, completed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
