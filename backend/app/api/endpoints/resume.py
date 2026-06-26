import os
import shutil
import uuid
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.models.resume import Resume
from ai.resume_parser.parser import ResumeParser

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Uploads a candidate resume file for processing.
    """
    allowed_extensions = [".pdf", ".docx", ".doc"]
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
        )

    # Save file
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext.lower()}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Process file
    parser = ResumeParser()
    parsed_data = parser.parse_file(file_path)

    if parsed_data.get("parsed_status") != "success":
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=parsed_data.get("message", "Failed to parse resume")
        )

    # Create DB entry
    db_resume = Resume(
        user_id=current_user.id,
        file_path=file_path,
        extracted_skills=parsed_data.get("skills", []),
        extracted_experience=parsed_data.get("experience", [])
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)

    return {
        "resume_id": db_resume.id,
        "status": "processing_complete",
        "message": "Resume uploaded and parsed successfully."
    }

@router.get("/{resume_id}")
def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves extracted metadata for a specific resume.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    return {
        "resume_id": resume.id,
        "extracted_skills": resume.extracted_skills,
        "extracted_experience": resume.extracted_experience,
        "uploaded_at": resume.uploaded_at
    }

@router.get("/")
def list_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all resumes for the authenticated user.
    """
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return [{"resume_id": r.id, "uploaded_at": r.uploaded_at} for r in resumes]
