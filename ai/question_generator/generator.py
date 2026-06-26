class QuestionGenerator:
    """
    Adaptive mock interview generator. Tailors questions dynamically based on resume context
    and active candidate conversation dialogue context.
    """
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name

    def generate_next_question(self, candidate_profile: dict, history: list) -> str:
        """
        Calculates and adaptively generates the next question.
        """
        # Placeholder question logic
        if not history:
            return f"Welcome! I noticed you have experience with {candidate_profile.get('skills', ['Next.js'])[0]}. Can you tell me about a project where you used it?"
        
        return "Can you explain how you handled state management and context optimization in that project?"
