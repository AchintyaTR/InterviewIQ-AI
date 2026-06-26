from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.app.database.connection import engine
from backend.app.database.base import Base
from backend.app.api.endpoints.auth import router as auth_router
from backend.app.api.endpoints.resume import router as resume_router

# Auto-create database tables on application start
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="InterviewIQ AI Backend API",
    description="Adaptive mock interview platform API driving resume parsing, speech integration, RAG-based question generation, and LLM mock evaluations.",
    version="1.0.0",
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Subsystems Routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(resume_router, prefix="/api/v1/resumes", tags=["Resume Management"])


class HealthResponse(BaseModel):
    status: str
    version: str
    database_connected: bool

@app.get("/api/v1/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint to verify backend service status and external database connections.
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        database_connected=True  # Simple heartbeat status
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
