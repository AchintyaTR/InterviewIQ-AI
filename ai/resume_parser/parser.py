import os
import re
import pdfplumber
import docx

class ResumeParser:
    """
    Parser interface responsible for extracting structured metadata from PDF and DOCX files.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        # Basic list of tech skills to look for
        self.common_skills = [
            "python", "java", "c++", "javascript", "typescript", "react", "next.js", 
            "node.js", "express", "sql", "postgresql", "mongodb", "aws", "docker", 
            "kubernetes", "machine learning", "deep learning", "nlp", "html", "css",
            "fastapi", "django", "flask", "pytorch", "tensorflow", "git", "linux"
        ]

    def _extract_text_from_pdf(self, file_path: str) -> str:
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text

    def _extract_text_from_docx(self, file_path: str) -> str:
        text = ""
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {e}")
        return text

    def _extract_name(self, text: str) -> str:
        # Simple heuristic: assume the first non-empty line might contain the name.
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            return lines[0]
        return "Unknown Candidate"

    def _extract_skills(self, text: str) -> list:
        found_skills = set()
        text_lower = text.lower()
        for skill in self.common_skills:
            # Word boundary regex for skills
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.add(skill.title() if len(skill) > 3 else skill.upper())
        return list(found_skills)

    def parse_file(self, file_path: str) -> dict:
        """
        Parses a PDF or DOCX file from local storage path.
        Returns:
            dict: Structured keys containing applicant name, skills, and work experience.
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        text = ""
        if ext == ".pdf":
            text = self._extract_text_from_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            text = self._extract_text_from_docx(file_path)
        else:
            return {"parsed_status": "error", "message": "Unsupported file format"}
            
        if not text:
            return {"parsed_status": "error", "message": "Could not extract text from document"}

        name = self._extract_name(text)
        skills = self._extract_skills(text)
        
        # Simple heuristic for experience for now (can be improved with LLM later)
        experience = [{"company": "Various", "role": "Professional", "duration": "See Resume"}]

        return {
            "name": name,
            "skills": skills,
            "experience": experience,
            "raw_text": text,
            "parsed_status": "success"
        }

    def parse_pdf(self, file_path: str) -> dict:
        """Legacy wrapper"""
        return self.parse_file(file_path)
