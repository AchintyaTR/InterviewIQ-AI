from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from backend.app.database.connection import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.models.interview import Interview
from backend.app.models.question import Question
from backend.app.models.response import Response
from backend.app.models.report import Report

from ai.evaluation_engine.evaluator import InterviewEvaluator

router = APIRouter()

evaluator = InterviewEvaluator()

@router.get("/{interview_id}/report")
def get_interview_report(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves the evaluation report for an interview.
    If the interview is completed but no report exists, it generates one.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id, Interview.user_id == current_user.id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
        
    if interview.status != "completed":
        raise HTTPException(status_code=400, detail="Interview must be completed before generating a report")
        
    # Check if report already exists
    existing_report = db.query(Report).filter(Report.interview_id == interview_id).first()
    if existing_report:
        return {
            "report_id": existing_report.id,
            "score_overall": existing_report.score_overall,
            "score_metrics": existing_report.score_metrics,
            "feedback": existing_report.feedback,
            "learning_roadmap": existing_report.learning_roadmap,
            "created_at": existing_report.created_at
        }
        
    # If not, generate the report
    questions = db.query(Question).filter(Question.interview_id == interview_id).order_by(Question.order_index.asc()).all()
    
    history = []
    for q in questions:
        history.append({"role": "system", "content": q.question_text})
        resp = db.query(Response).filter(Response.question_id == q.id).first()
        if resp:
            history.append({"role": "user", "content": resp.response_text})
            
    # Evaluate using the LLM engine
    evaluation = evaluator.evaluate_interview_session(history=history)
    
    new_report = Report(
        interview_id=interview_id,
        score_overall=evaluation.get("score_overall", 0.0),
        score_metrics=evaluation.get("score_metrics", {}),
        feedback=evaluation.get("feedback", "No feedback provided."),
        learning_roadmap=evaluation.get("learning_roadmap", [])
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return {
        "report_id": new_report.id,
        "score_overall": new_report.score_overall,
        "score_metrics": new_report.score_metrics,
        "feedback": new_report.feedback,
        "learning_roadmap": new_report.learning_roadmap,
        "created_at": new_report.created_at
    }
