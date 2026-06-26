# Database Design and Schema

This document outlines the database schema and relationships for **InterviewIQ AI** built with PostgreSQL.

## Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS {
        uuid id PK
        string email UK
        string hashed_password
        string full_name
        timestamp created_at
        timestamp updated_at
    }

    RESUMES {
        uuid id PK
        uuid user_id FK
        string file_path
        jsonb extracted_skills
        jsonb extracted_experience
        timestamp uploaded_at
    }

    INTERVIEWS {
        uuid id PK
        uuid user_id FK
        string role_target
        string company_target
        string status
        timestamp started_at
        timestamp completed_at
    }

    QUESTIONS {
        uuid id PK
        uuid interview_id FK
        string question_text
        string audio_path
        integer order_index
        timestamp created_at
    }

    RESPONSES {
        uuid id PK
        uuid question_id FK
        string response_text
        string audio_path
        integer duration_seconds
        timestamp created_at
    }

    REPORTS {
        uuid id PK
        uuid interview_id FK
        float score_overall
        jsonb score_metrics
        string feedback_text
        jsonb learning_roadmap
        timestamp created_at
    }

    USERS ||--o{ RESUMES : uploads
    USERS ||--o{ INTERVIEWS : conducts
    INTERVIEWS ||--|{ QUESTIONS : contains
    QUESTIONS ||--o| RESPONSES : receives
    INTERVIEWS ||--o| REPORTS : generates
```

## Schema Definitions

### Users Table (`users`)
- `id` (UUID, Primary Key): Unique identifier.
- `email` (VARCHAR, Unique, Indexed): User email address.
- `hashed_password` (VARCHAR): Secure password hash.
- `full_name` (VARCHAR): User name.
- `created_at` (TIMESTAMP): Creation date.

### Resumes Table (`resumes`)
- `id` (UUID, Primary Key): Unique identifier.
- `user_id` (UUID, Foreign Key ➔ `users.id`): Associated candidate.
- `file_path` (VARCHAR): Location of raw document on disk/storage bucket.
- `extracted_skills` (JSONB): Parsed skills list.
- `extracted_experience` (JSONB): Structured job history.
- `uploaded_at` (TIMESTAMP): Upload timestamp.

### Interviews Table (`interviews`)
- `id` (UUID, Primary Key): Unique identifier.
- `user_id` (UUID, Foreign Key ➔ `users.id`): Candidate undergoing the mock interview.
- `role_target` (VARCHAR): Target role title (e.g., "Software Engineer").
- `company_target` (VARCHAR): Target company (e.g., "Google").
- `status` (VARCHAR): Current state (`scheduled`, `in_progress`, `completed`, `failed`).
- `started_at` (TIMESTAMP): Start timestamp.

### Questions Table (`questions`)
- `id` (UUID, Primary Key): Unique identifier.
- `interview_id` (UUID, Foreign Key ➔ `interviews.id`): Associated interview.
- `question_text` (TEXT): The generated query text.
- `audio_path` (VARCHAR, Optional): Path to generated TTS speech asset.
- `order_index` (INTEGER): Sequence ranking.

### Responses Table (`responses`)
- `id` (UUID, Primary Key): Unique identifier.
- `question_id` (UUID, Foreign Key ➔ `questions.id`): Associated question.
- `response_text` (TEXT): Transcript of candidate response.
- `audio_path` (VARCHAR, Optional): Path to saved user audio response.
- `duration_seconds` (INTEGER): Time taken to answer.

### Reports Table (`reports`)
- `id` (UUID, Primary Key): Unique identifier.
- `interview_id` (UUID, Foreign Key ➔ `interviews.id`, Unique): Associated interview session.
- `score_overall` (FLOAT): Overall score (0.0 to 100.0).
- `score_metrics` (JSONB): Breakdown of sub-scores (Accuracy, Style, Structure, Confidence).
- `feedback_text` (TEXT): High-level feedback and critiques.
- `learning_roadmap` (JSONB): Adaptive study roadmap mapping suggestions to weak spots.
