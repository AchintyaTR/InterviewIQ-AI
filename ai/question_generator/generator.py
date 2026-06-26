import os
from openai import OpenAI

class QuestionGenerator:
    """
    Adaptive mock interview generator. Tailors questions dynamically based on resume context
    and active candidate conversation dialogue context.
    """
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def generate_next_question(self, candidate_profile: dict, history: list, rag_templates: list = None) -> str:
        """
        Calculates and adaptively generates the next question.
        Uses OpenAI if API key is present, otherwise falls back to heuristics.
        """
        # --- Fallback Heuristic ---
        if not self.client:
            skills = candidate_profile.get("skills", [])
            primary_skill = skills[0] if skills else "software engineering"
            
            if not history:
                if rag_templates:
                    return f"Welcome! Let's start with a scenario: {rag_templates[0]['question']}"
                return f"Welcome! I noticed you have experience with {primary_skill}. Can you tell me about a project where you used it?"
            
            return f"That's interesting. Given your background in {primary_skill}, can you explain a challenge you faced and how you overcame it?"
        
        # --- OpenAI LLM Generation ---
        system_prompt = (
            "You are an expert technical interviewer. You are conducting a mock interview with a candidate. "
            "You must ask one clear, focused interview question based on the candidate's profile, "
            "the conversation history, and any provided question templates. "
            "Keep the tone professional and conversational."
        )
        
        user_context = f"Candidate Profile:\n{candidate_profile}\n\n"
        if rag_templates:
            user_context += f"Recommended Question Templates:\n{rag_templates}\n\n"
            
        user_context += "Conversation History:\n"
        if not history:
            user_context += "None. This is the first question.\n"
        else:
            for item in history:
                role = "Candidate" if item.get("role") == "user" else "Interviewer"
                user_context += f"{role}: {item.get('content')}\n"
                
        user_context += "\nPlease generate the next interview question."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_context}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating question via LLM: {e}")
            return "Could you tell me more about your recent project experience?"
