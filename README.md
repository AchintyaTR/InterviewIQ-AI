# InterviewIQ AI

An AI-powered mock interview platform that simulates real technical and behavioral interviews, adapting questions dynamically to a candidate's resume, selected experience level, and previous responses.

## Overview

InterviewIQ AI helps candidates prepare for real interviews through personalized, adaptive evaluations. By parsing candidate resumes, validating job roles, conducting interactive voice-based interviews, and providing deep analytics, the platform replicates the rigor of top-tier company interviews.

## Features

- **Resume Parsing & Validation:** Automatically extracts text and technical skills from PDF and DOCX resumes. Uses LLM-based strict validation to reject invalid or junk documents.
- **Adaptive Question Generation:** Leverages the powerful Groq AI Engine (Llama 3) to tailor questions dynamically based on resume context, job role, and the candidate's active conversation history.
- **Experience Level Calibration:** Users can select their seniority (Fresher to 15+ years), and the AI automatically scales the difficulty and architectural depth of the questions.
- **Role Validation:** Strict LLM gatekeeper prevents users from entering fictional or invalid job roles (e.g., "Batman").
- **Voice-Based Mock Interviews:** Native Web Speech API integration for realistic oral interviews with real-time streaming text (Note: Voice mode requires Google Chrome or Microsoft Edge).
- **Retrieval-Augmented Generation (RAG):** Focuses questions using relevant templates stored in a local ChromaDB vector database.
- **Multi-Metric Evaluation & Feedback:** Grades responses based on technical accuracy, providing a final score, actionable feedback, and a personalized learning roadmap.
- **Modern UI/UX:** A stunning, responsive Glassmorphism design system built with Next.js and custom CSS.

## Architecture

```text
       ┌─────────────────────────┐
       │   React/Next.js Client  │
       └────────────┬────────────┘
                    │ HTTP REST API
                    ▼
       ┌─────────────────────────┐
       │     FastAPI Backend     │
       └──────┬─────┬──────┬─────┘
              │     │      │
      ┌───────┘     │      └────────┐
      ▼             ▼               ▼
┌───────────┐ ┌───────────┐  ┌──────────────┐
│  SQLite   │ │  ChromaDB  │  │  AI Engines  │
│ Database  │ │ (Vector)  │  │ (Groq LLM)   │
└───────────┘ └───────────┘  └──────────────┘
```

Detailed architecture flow:
`Frontend` ➔ `FastAPI Backend` ➔ `Authentication` ➔ `Resume Parser & Validator` ➔ `RAG (ChromaDB)` ➔ `Groq LLM` ➔ `Evaluation Engine` ➔ `SQLite`

## Tech Stack

- **Frontend:** Next.js (App Router), React, TypeScript, Vanilla CSS Modules (Glassmorphism UI)
- **Backend:** FastAPI (Python 3.11+), Uvicorn, SQLAlchemy
- **Databases:** SQLite (Relational Data), ChromaDB (Vector Embeddings)
- **AI/ML:** Groq (Llama 3), OpenAI (Fallback), PyPDF2/pdfplumber, Web Speech API (STT)
- **DevOps:** Docker, Docker Compose

## Installation

### Prerequisites
- Node.js v18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Environment Variables
Copy `.env.example` to `.env` and fill in your Groq API key:
```bash
cp .env.example .env
```

## Running Locally

### Using Docker Compose
Build and run the entire application stack:
```bash
docker-compose up --build
```

### Running Natively (Without Docker)

#### Backend:
1. Navigate to the backend directory and activate virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Start the dev server from the **root project directory**:
   ```bash
   cd ..
   uvicorn backend.app.main:app --reload
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

## Known Limitations & Troubleshooting
- **Microphone Not Working:** Brave browser aggressively blocks Google's speech-to-text servers. If your microphone turns off instantly or doesn't transcribe text, you must use **Google Chrome** or **Microsoft Edge**.
- **Session Expired:** Authentication JWTs expire after 60 minutes. You will be cleanly redirected to the login page if your session expires during setup.

## Contributors

- Achintya

## License

This project is licensed under the MIT License - see the LICENSE file for details.
