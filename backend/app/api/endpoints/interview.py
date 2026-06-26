from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from backend.app.database.connection import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.models.resume import Resume
from backend.app.models.interview import Interview
from backend.app.models.question import Question
from backend.app.models.response import Response

from ai.question_generator.generator import QuestionGenerator
from ai.rag.retriever import RAGRetriever

router = APIRouter()

# Instantiate AI engines (global instances for simplicity)
question_generator = QuestionGenerator()
rag_retriever = RAGRetriever()

class StartInterviewRequest(BaseModel):
    resume_id: str
    target_role: str
    target_company: str = "General"

class SubmitResponseRequest(BaseModel):
    answer_text: str

@router.post("/start", status_code=status.HTTP_201_CREATED)
def start_interview(
    request: StartInterviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Initializes a new interview session.
    Fetches the resume, generates the first adaptive question, and returns it.
    """
    resume = db.query(Resume).filter(Resume.id == request.resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    interview = Interview(
        user_id=current_user.id,
        resume_id=resume.id,
        target_role=request.target_role,
        target_company=request.target_company,
        status="in_progress"
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    
    # Retrieve RAG templates based on role/company
    query_str = f"Interview questions for {request.target_role} at {request.target_company}"
    templates = rag_retriever.retrieve_relevant_templates(query=query_str, limit=2)
    
    # Candidate profile context
    candidate_profile = {
        "skills": resume.extracted_skills,
        "experience": resume.extracted_experience,
        "target_role": request.target_role,
        "target_company": request.target_company
    }
    
    # Generate the first question
    first_q_text = question_generator.generate_next_question(
        candidate_profile=candidate_profile, 
        history=[], 
        rag_templates=templates
    )
    
    db_question = Question(
        interview_id=interview.id,
        question_text=first_q_text,
        order_index=1
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    return {
        "interview_id": interview.id,
        "status": interview.status,
        "first_question": {
            "id": db_question.id,
            "text": db_question.question_text
        }
    }

@router.post("/{interview_id}/respond")
def submit_response(
    interview_id: str,
    request: SubmitResponseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submits an answer to the current question and generates the next question adaptively.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id, Interview.user_id == current_user.id).first()
    if not interview or interview.status != "in_progress":
        raise HTTPException(status_code=404, detail="Active interview not found")
        
    # Find the latest unanswered question
    questions = db.query(Question).filter(Question.interview_id == interview_id).order_by(Question.order_index.asc()).all()
    if not questions:
        raise HTTPException(status_code=400, detail="No active questions found")
        
    latest_question = questions[-1]
    
    # Check if a response already exists
    existing_resp = db.query(Response).filter(Response.question_id == latest_question.id).first()
    if existing_resp:
        raise HTTPException(status_code=400, detail="Question already answered")
        
    # Save the response
    new_response = Response(
        question_id=latest_question.id,
        response_text=request.answer_text,
        audio_url=None
    )
    db.add(new_response)
    db.commit()
    
    # Check if interview is long enough to end (e.g., max 5 questions for now)
    if len(questions) >= 5:
        interview.status = "completed"
        interview.ended_at = datetime.utcnow()
        db.commit()
        return {
            "status": "completed",
            "message": "Interview completed. Ready for evaluation."
        }
        
    # Generate next question
    resume = db.query(Resume).filter(Resume.id == interview.resume_id).first()
    candidate_profile = {
        "skills": resume.extracted_skills,
        "target_role": interview.target_role
    }
    
    # Build history
    history = []
    for q in questions:
        history.append({"role": "system", "content": q.question_text})
        resp = db.query(Response).filter(Response.question_id == q.id).first()
        if resp:
            history.append({"role": "user", "content": resp.response_text})
            
    # Retrieve new template for variety
    query_str = f"Follow-up interview question for {interview.target_role} covering {resume.extracted_skills[0] if resume.extracted_skills else 'general'}"
    templates = rag_retriever.retrieve_relevant_templates(query=query_str, limit=1)
    
    next_q_text = question_generator.generate_next_question(
        candidate_profile=candidate_profile,
        history=history,
        rag_templates=templates
    )
    
    next_question = Question(
        interview_id=interview.id,
        question_text=next_q_text,
        order_index=len(questions) + 1
    )
    db.add(next_question)
    db.commit()
    db.refresh(next_question)
    
    return {
        "status": "in_progress",
        "next_question": {
            "id": next_question.id,
            "text": next_question.question_text
        }
    }

@router.post("/{interview_id}/complete")
def complete_interview(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually ends the interview session early.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id, Interview.user_id == current_user.id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
        
    if interview.status == "in_progress":
        interview.status = "completed"
        interview.ended_at = datetime.utcnow()
        db.commit()
        
    return {"status": "completed", "message": "Interview successfully ended."}

@router.get("/")
def list_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves history of interviews for the authenticated user.
    """
    interviews = db.query(Interview).filter(Interview.user_id == current_user.id).all()
    return [{
        "interview_id": i.id,
        "target_role": i.target_role,
        "target_company": i.target_company,
        "status": i.status,
        "started_at": i.started_at,
        "ended_at": i.ended_at
    } for i in interviews]
