import os
from openai import OpenAI

class QuestionGenerator:
    """
    Adaptive mock interview generator. Tailors questions dynamically based on resume context
    and active candidate conversation dialogue context.
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

    def is_valid_role(self, role: str) -> tuple[bool, int]:
        """
        Validates if the provided string is a legitimate job role/profession.
        """
        if not self.client:
            return True, 0 # Fallback if no LLM
            
        system_prompt = (
            "You are a strict data validation assistant. "
            "Determine if the user's input is a legitimate professional job role, title, or career path. "
            "Reply ONLY with 'YES' if it is a valid job role (e.g. 'Software Engineer', 'Data Analyst', 'Marketing Manager'). "
            "Reply ONLY with 'NO' if it is gibberish, a fictional character, a random word, or clearly not a job (e.g. 'Batman', 'asdf', 'Pizza')."
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Job Role: {role}"}
                ],
                max_tokens=10,
                temperature=0.0
            )
            ans = response.choices[0].message.content.strip().upper()
            tokens = response.usage.total_tokens if response.usage else 0
            return "YES" in ans, tokens
        except Exception as e:
            print(f"Error validating role via LLM: {e}")
            return True, 0

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
                    return f"Welcome! Let's start with a scenario: {rag_templates[0]['question']}", 0
                return f"Welcome! I noticed you have experience with {primary_skill}. Can you tell me about a project where you used it?", 0
            
            return f"That's interesting. Given your background in {primary_skill}, can you explain a challenge you faced and how you overcame it?", 0
        
        # --- OpenAI LLM Generation ---
        system_prompt = (
            "You are an expert technical interviewer. You are conducting a mock interview with a candidate. "
            "You must ask one clear, focused interview question based on the candidate's profile, "
            "the conversation history, and any provided question templates. "
            "Keep the tone professional and conversational.\n\n"
            "CRITICAL INSTRUCTION: OUTPUT ONLY THE QUESTION ITSELF. Do NOT include any introductory text, "
            "internal thought processes, explanations, or conversational filler like 'Here is the next question:' or 'Based on the history...'."
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
            tokens = response.usage.total_tokens if response.usage else 0
            return response.choices[0].message.content.strip(), tokens
        except Exception as e:
            print(f"Error generating question via LLM: {e}")
            return "Could you tell me more about your recent project experience?", 0
