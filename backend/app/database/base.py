# Import all models here so SQLAlchemy metadata registers them
from backend.app.database.connection import Base
from backend.app.models.user import User
from backend.app.models.resume import Resume
from backend.app.models.interview import Interview
from backend.app.models.question import Question
from backend.app.models.response import Response
from backend.app.models.report import Report
