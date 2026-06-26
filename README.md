# InterviewIQ AI

An AI-powered mock interview platform that simulates real technical and HR interviews, adapting questions to a candidate's resume, skills, and previous responses.

## Overview

InterviewIQ AI helps candidates prepare for real interviews through personalized, adaptive evaluations. By parsing candidate resumes, conducting interactive voice-based interviews, evaluating coding challenges, and providing deep analytics, the platform replicates the rigor of top-tier company interviews.

## Features

- **Resume Parsing & Skill Extraction:** Automatically extracts projects, languages, and technical concepts from PDF and DOCX resumes.
- **Adaptive Question Generation:** Leverages Large Language Models (LLMs) to tailor questions dynamically based on resume context and candidate responses.
- **Voice-Based Mock Interviews:** Integrated speech-to-text (STT) and text-to-speech (TTS) pipelines for realistic oral interviews.
- **Automated Coding Assessments:** Sandbox environment to run coding challenges with automated test case evaluation.
- **Retrieval-Augmented Generation (RAG):** Focuses questions on company-specific guidelines and formats retrieved from public datasets.
- **Multi-Metric Evaluation & Feedback:** Grades responses based on technical accuracy, communication style, confidence, and answer structure.
- **Comprehensive Analytics Dashboard:** Visual tracking of mock interview performance, strengths, weaknesses, and a personalized learning roadmap.
- **Recruiter Dashboard:** Recruiter view to manage candidates, review performance records, and track readiness.

## Architecture

```text
       ┌─────────────────────────┐
       │   React/Next.js Client  │
       └────────────┬────────────┘
                    │ HTTPS / WebSockets
                    ▼
       ┌─────────────────────────┐
       │     FastAPI Backend     │
       └──────┬─────┬──────┬─────┘
              │     │      │
      ┌───────┘     │      └────────┐
      ▼             ▼               ▼
┌───────────┐ ┌───────────┐  ┌──────────────┐
│  Postgres │ │  ChromaDB  │  │  AI Engines  │
│ Database  │ │ (Vector)  │  │ (LLM/RAG/STT)│
└───────────┘ └───────────┘  └──────────────┘
```

Detailed architecture flow:
`Frontend` ➔ `FastAPI Backend` ➔ `Authentication` ➔ `Interview Engine` ➔ `Resume Parser` ➔ `RAG` ➔ `LLM` ➔ `Evaluation Engine` ➔ `PostgreSQL`

## Tech Stack

- **Frontend:** Next.js (App Router), React, CSS Modules / Tailwind (config pending)
- **Backend:** FastAPI (Python 3.11+), Uvicorn, SQLAlchemy
- **Databases:** PostgreSQL (Relational Data), pgvector / ChromaDB (Vector Embeddings)
- **AI/ML:** OpenAI GPT-4 / Anthropic Claude, LangChain, PyPDF2/pdfplumber, Whisper (Speech-to-Text), Coqui/gTTS (Text-to-Speech)
- **DevOps:** Docker, Docker Compose, GitHub Actions (CI/CD)

## Installation

### Prerequisites
- Docker & Docker Compose
- Node.js v18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Environment Variables
Copy `.env.example` to `.env` and fill in the required variables:
```bash
cp .env.example .env
```

## Running Locally

### Using Docker Compose (Recommended)
Build and run the entire application stack:
```bash
docker-compose up --build
```

### Running Components Individually

#### Backend:
1. Navigate to the backend directory and activate virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Start the dev server:
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend:
1. Navigate to frontend directory and install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the Next.js development server:
   ```bash
   npm run dev
   ```

## Screenshots

*Screenshots will be uploaded to `docs/screenshots/` and documented here once UI components are generated.*

- **Login Screen:** `docs/screenshots/login.png`
- **Candidate Dashboard:** `docs/screenshots/dashboard.png`
- **Resume Uploader:** `docs/screenshots/resume_upload.png`
- **Voice Interview Interface:** `docs/screenshots/voice_interview.png`
- **Performance Evaluation Report:** `docs/screenshots/feedback.png`

## Demo Video

*Placeholder link for the demonstration walkthrough.*

## Future Improvements

- Add peer-to-peer live mock interviews.
- Integrate system design whiteboard drawing evaluations.
- Real-time video emotion analysis during response speech.

## Contributors

- Achintya

## License

This project is licensed under the MIT License - see the LICENSE file for details.
