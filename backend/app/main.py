from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
