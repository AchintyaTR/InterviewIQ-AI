class ResumeParser:
    """
    Parser interface responsible for extracting structured metadata from PDF and DOCX files.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def parse_pdf(self, file_path: str) -> dict:
        """
        Parses a PDF file from local storage path.
        Returns:
            dict: Structured keys containing applicant name, skills, and work experience.
        """
        # Placeholder parsing structure
        return {
            "name": "Jane Doe",
            "skills": ["Python", "Next.js", "SQL", "Machine Learning"],
            "experience": [
                {
                    "company": "Tech Solutions Inc",
                    "role": "Frontend Developer",
                    "duration": "2 years"
                }
            ],
            "parsed_status": "success"
        }
