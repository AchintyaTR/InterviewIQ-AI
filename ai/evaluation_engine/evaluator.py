import os
import json
from openai import OpenAI

class InterviewEvaluator:
    """
    Evaluates mock interview transcript dialogue sessions. Generates scores and feedbacks.
    """
    def __init__(self, model_name: str = None):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if self.groq_api_key:
            self.client = OpenAI(api_key=self.groq_api_key, base_url="https://api.groq.com/openai/v1")
            self.model_name = model_name or "llama-3.1-8b-instant"
        elif self.openai_api_key:
            self.client = OpenAI(api_key=self.openai_api_key)
            self.model_name = model_name or "gpt-3.5-turbo"
        else:
            self.client = None
            self.model_name = None

    def _fallback_evaluation(self, history=None) -> dict:
        """Returns placeholder evaluation if LLM fails or is unconfigured."""
        q_evals = []
        if history:
            current_q = None
            for item in history:
                if item.get("role") == "system":
                    current_q = item.get("content")
                elif item.get("role") == "user" and current_q:
                    q_evals.append({
                        "question": current_q,
                        "candidate_answer": item.get("content"),
                        "score": 85.0,
                        "feedback": "This is a placeholder evaluation because the LLM API is not configured or failed.",
                        "expected_answer": "Configure GROQ_API_KEY or OPENAI_API_KEY in the .env file.",
                        "keywords": ["placeholder", "api-key"]
                    })
                    current_q = None

        if not q_evals:
            q_evals = [
                {
                    "question": "Can you describe a time you faced a difficult technical challenge?",
                    "candidate_answer": "I once had to optimize a slow database query...",
                    "score": 85.0,
                    "feedback": "Good example, but could use more detail on the specific outcome.",
                    "expected_answer": "Use the STAR method to describe the situation, task, action, and measurable result.",
                    "keywords": ["STAR", "optimization", "metrics"]
                }
            ]

        return {
            "score_overall": 85.0,
            "score_metrics": {
                "technical_accuracy": 90.0,
                "communication_skills": 80.0,
                "problem_solving": 85.0,
                "confidence": 85.0
            },
            "feedback": "Strong technical foundation. Work on using structured frameworks like STAR to answer behavioral questions.",
            "learning_roadmap": [
                {
                    "topic": "System Design Patterns",
                    "suggestion": "Read Designing Data-Intensive Applications."
                }
            ],
            "question_evaluations": q_evals
        }

    def evaluate_interview_session(self, history: list) -> dict:
        """
        Processes conversation logs to evaluate answers across multiple metrics.
        Expects `history` to be a list of dictionaries with 'role' ('system' or 'user') and 'content'.
        """
        if not self.client or not history:
            return self._fallback_evaluation(history), 0

        num_questions = sum(1 for item in history if item.get("role") == "system")
        
        system_prompt = (
            "You are an expert technical recruiter and senior engineer. You must evaluate the candidate's interview performance. "
            "I will provide you with the transcript of the interview (Interviewer questions and Candidate responses). "
            "You MUST return the evaluation strictly as a valid JSON object without any additional markdown formatting or text. "
            f"IMPORTANT: The transcript contains exactly {num_questions} questions. Your `question_evaluations` array MUST contain EXACTLY {num_questions} objects, one for each question asked by the Interviewer. Do not omit or combine any questions.\n"
            "The JSON must have this exact structure:\n"
            "{\n"
            "  \"score_overall\": <float between 0 and 100>,\n"
            "  \"score_metrics\": {\n"
            "    \"technical_accuracy\": <float between 0 and 100>,\n"
            "    \"communication_skills\": <float between 0 and 100>,\n"
            "    \"problem_solving\": <float between 0 and 100>,\n"
            "    \"confidence\": <float between 0 and 100>\n"
            "  },\n"
            "  \"feedback\": \"<A detailed paragraph summarizing the performance, strengths, and weaknesses.>\",\n"
            "  \"learning_roadmap\": [\n"
            "    {\"topic\": \"<Specific topic to study>\", \"suggestion\": \"<Actionable advice or resource>\"}\n"
            "  ],\n"
            "  \"question_evaluations\": [\n"
            "    {\n"
            "      \"question\": \"<Original question text>\",\n"
            "      \"candidate_answer\": \"<Candidate's answer>\",\n"
            "      \"score\": <float between 0 and 100>,\n"
            "      \"feedback\": \"<Constructive feedback on what was good and missing>\",\n"
            "      \"expected_answer\": \"<A brief summary of an ideal answer>\",\n"
            "      \"keywords\": [\"<keyword1>\", \"<keyword2>\"]\n"
            "    }\n"
            "  ]\n"
            "}"
        )

        user_context = "Interview Transcript:\n"
        for idx, item in enumerate(history):
            role_name = "Interviewer" if item.get("role") == "system" else "Candidate"
            user_context += f"{role_name}: {item.get('content')}\n"

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_context}
                ],
                max_tokens=2500,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            raw_content = response.choices[0].message.content.strip()
            # Some models might still wrap with markdown despite instructions
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]
                
            tokens = response.usage.total_tokens if response.usage else 0
            return json.loads(raw_content), tokens
            
        except Exception as e:
            print(f"Error generating evaluation via LLM: {e}")
            return self._fallback_evaluation(history), 0
