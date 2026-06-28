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

## Architecture & Workflow

```mermaid
graph TD
    %% User and Frontend
    User([Candidate]) -->|Interacts via Voice/Text| NextJS[Next.js Frontend]
    
    %% API Requests
    NextJS -->|HTTP REST (JSON)| FastAPI[FastAPI Backend]
    
    %% FastAPI Modules
    subgraph FastAPI Application Logic
        FastAPI --> Auth{JWT Auth Middleware}
        
        %% 1. Resume Flow
        Auth -->|/resumes| ResumeApp[Resume Processing Module]
        ResumeApp -->|Extracts Text| PyPDF[PDF/DOCX Parser]
        PyPDF -->|Raw Text| Validator[LLM Role Gatekeeper]
        
        %% 2. Interview Flow
        Auth -->|/interviews| InterviewApp[Interview Session Engine]
        InterviewApp -->|Search Templates| RAG[RAG Retrieval System]
        InterviewApp -->|Context + History| AI_Prompt[Prompt Builder]
        
        %% 3. Report Flow
        Auth -->|/reports| ReportApp[Evaluation Module]
    end

    %% External AI
    Validator -->|Validate Profile| GroqCloud((Groq Llama 3 API))
    AI_Prompt -->|Generate Question| GroqCloud
    ReportApp -->|Calculate Metrics| GroqCloud

    %% Databases
    subgraph Data Persistence
        RAG -->|Similarity Search| ChromaDB[(ChromaDB Vector Store)]
        ResumeApp -->|Store Profile| Postgres[(PostgreSQL Relational DB)]
        InterviewApp -->|Save Q&A| Postgres
        ReportApp -->|Fetch History| Postgres
    end
```

### Process Breakdown:
1. **Frontend (Next.js)** captures the user's
 microphone using the Native Web Speech API, converts voice to text locally, and sends REST API calls to the backend.
2. **Authentication (FastAPI)** intercepts all requests to ensure the user has a valid JSON Web Token (JWT).
3. **Resume Processing:** When a user uploads a resume, FastAPI uses `pdfplumber` to extract text. It then asks the Groq LLM to act as a "Gatekeeper" to ensure the resume and requested job role are legitimate (blocking fake inputs like "Batman").
4. **Interview Session (RAG + AI):** During the interview, FastAPI queries **ChromaDB** to find relevant technical templates based on the job role. It combines this template, the user's resume, and the chat history into a massive prompt and sends it to **Groq**.
5. **Evaluation Engine:** Once the interview is complete, FastAPI feeds the entire transcript back into the LLM to grade technical accuracy, communication skills, and generates a personalized improvement roadmap.
6. **Data Storage:** All unstructured vector data is handled by **ChromaDB**, while all relational data (users, transcripts, grades) is permanently stored in **PostgreSQL**.

## Tech Stack

- **Frontend:** Next.js (App Router), React, TypeScript, Vanilla CSS Modules (Glassmorphism UI)
- **Backend:** FastAPI (Python 3.11+), Uvicorn, SQLAlchemy
- **Databases:** PostgreSQL (Docker) / SQLite (Local fallback), ChromaDB (Vector Embeddings)
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
