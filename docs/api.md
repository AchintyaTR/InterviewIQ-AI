# API Reference

This document maps the REST endpoints exposed by the **InterviewIQ AI** backend service.

## API Base URL
```
http://localhost:8000/api/v1
```

## Authentication

### POST `/auth/register`
Creates a new candidate account.
- **Request Body:**
  ```json
  {
    "email": "candidate@example.com",
    "password": "strongpassword123",
    "full_name": "Jane Doe"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": "e30e14db-99e5-4a57-8ba7-fa74421b44c0",
    "email": "candidate@example.com",
    "full_name": "Jane Doe",
    "created_at": "2026-06-26T10:00:00Z"
  }
  ```

### POST `/auth/token`
Generates a JWT access token.
- **Request Form Data:**
  - `username`: email
  - `password`: password
- **Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer"
  }
  ```

---

## Resume Management

### POST `/resumes/upload`
Uploads a candidate resume file for processing.
- **Headers:** `Authorization: Bearer <token>`
- **Request Form Data:**
  - `file`: PDF or DOCX file object
- **Response (202 Accepted):**
  ```json
  {
    "resume_id": "55122f30-80a5-4f40-84cf-cf5847e923e1",
    "status": "processing",
    "message": "Resume uploaded successfully and added to parser queue."
  }
  ```

### GET `/resumes/{resume_id}`
Retrieves extracted metadata for a specific resume.
- **Headers:** `Authorization: Bearer <token>`
- **Response (200 OK):**
  ```json
  {
    "resume_id": "55122f30-80a5-4f40-84cf-cf5847e923e1",
    "extracted_skills": ["Python", "Next.js", "SQL", "Machine Learning"],
    "extracted_experience": [
      {
        "company": "Tech Solutions Inc",
        "role": "Frontend Developer",
        "duration": "2 years"
      }
    ],
    "uploaded_at": "2026-06-26T10:05:00Z"
  }
  ```

---

## Interview Engine

### POST `/interviews/start`
Starts a mock interview session.
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "role_target": "Full Stack Engineer",
    "company_target": "Google"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "interview_id": "a62886f4-bca5-48ef-be8f-51820468e826",
    "status": "in_progress",
    "first_question": {
      "question_id": "c6218c8e-5bca-4e50-bb82-f542180a4ed0",
      "text": "Hi Jane, I see you have experience with Next.js in your projects. Can you explain the difference between Server and Client Components?"
    }
  }
  ```

### POST `/interviews/{interview_id}/respond`
Submits a response transcript to a question and fetches the next question.
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "question_id": "c6218c8e-5bca-4e50-bb82-f542180a4ed0",
    "response_text": "Server components run on the server and are non-interactive, while Client components are rendered on client-side and support interactivity."
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "received": true,
    "next_question": {
      "question_id": "d7488f7a-80ac-4bca-bc74-ea9b61d782ac",
      "text": "Great. Following up on Next.js, how does state hydration work for these components?"
    }
  }
  ```

### POST `/interviews/{interview_id}/complete`
Finishes the interview session and triggers metrics generation.
- **Headers:** `Authorization: Bearer <token>`
- **Response (200 OK):**
  ```json
  {
    "interview_id": "a62886f4-bca5-48ef-be8f-51820468e826",
    "status": "completed",
    "message": "Interview closed. Processing evaluation engine..."
  }
  ```

---

## Analytics and Reports

### GET `/interviews/{interview_id}/report`
Retrieves evaluation reports and analytics for a completed interview.
- **Headers:** `Authorization: Bearer <token>`
- **Response (200 OK):**
  ```json
  {
    "interview_id": "a62886f4-bca5-48ef-be8f-51820468e826",
    "score_overall": 84.5,
    "score_metrics": {
      "technical_accuracy": 88.0,
      "communication_skills": 80.0,
      "problem_solving": 85.0,
      "confidence": 85.0
    },
    "feedback": "Overall strong technical knowledge. Communication was concise but could be structured better using the STAR method.",
    "learning_roadmap": [
      {
        "topic": "React State Hydration",
        "suggestion": "Read Next.js hydration specs and practice rendering lifecycles."
      }
    ]
  }
  ```
