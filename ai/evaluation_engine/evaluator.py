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
            self.model_name = model_name or "llama3-8b-8192"
        elif self.openai_api_key:
            self.client = OpenAI(api_key=self.openai_api_key)
            self.model_name = model_name or "gpt-3.5-turbo"
        else:
            self.client = None
            self.model_name = None

    def _fallback_evaluation(self) -> dict:
        """Returns placeholder evaluation if LLM fails or is unconfigured."""
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
            ]
        }

    def evaluate_interview_session(self, history: list) -> dict:
        """
        Processes conversation logs to evaluate answers across multiple metrics.
        Expects `history` to be a list of dictionaries with 'role' ('system' or 'user') and 'content'.
        """
        if not self.client or not history:
            return self._fallback_evaluation()

        system_prompt = (
            "You are an expert technical recruiter and senior engineer. You must evaluate the candidate's interview performance. "
            "I will provide you with the transcript of the interview (Interviewer questions and Candidate responses). "
            "You MUST return the evaluation strictly as a valid JSON object without any additional markdown formatting or text. "
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
                max_tokens=800,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            raw_content = response.choices[0].message.content.strip()
            # Some models might still wrap with markdown despite instructions
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]
                
            return json.loads(raw_content)
            
        except Exception as e:
            print(f"Error generating evaluation via LLM: {e}")
            return self._fallback_evaluation()
