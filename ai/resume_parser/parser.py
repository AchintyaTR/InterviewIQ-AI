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
        
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if self.groq_api_key:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.groq_api_key, base_url="https://api.groq.com/openai/v1")
            self.model_name = "llama-3.1-8b-instant"
        elif self.openai_api_key:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.openai_api_key)
            self.model_name = "gpt-3.5-turbo"
        else:
            self.client = None

    def _extract_text_from_pdf(self, file_path: str) -> str:
        text = ""
        # Try PyMuPDF (fitz) first for better compatibility
        try:
            import fitz
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
        except Exception as e:
            print(f"Error reading PDF with fitz: {e}")
            
        # Fallback to pdfplumber if fitz failed or returned empty text
        if not text.strip():
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                print(f"Error reading PDF with pdfplumber: {e}")
                
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

    def _analyze_resume(self, text: str) -> tuple[bool, list, int]:
        if not self.client:
            # Fallback to simple regex if no API client is configured
            found_skills = set()
            text_lower = text.lower()
            for skill in self.common_skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                    found_skills.add(skill.title() if len(skill) > 3 else skill.upper())
            return True, list(found_skills), 0

        system_prompt = (
            "You are a technical recruiter AI. Analyze the following text extracted from a document. "
            "1. Determine if it represents a professional resume or CV. "
            "2. Extract a comprehensive list of all technical skills, programming languages, frameworks, databases, tools, and relevant soft skills. "
            "Return ONLY a valid JSON object with exactly two keys: "
            "\"is_valid\" (boolean, true if it is a resume, false if random junk/not a resume) and "
            "\"skills\" (array of strings, empty if none). "
            "Do not include any markdown, backticks, or explanations. "
            "Example output: {\"is_valid\": true, \"skills\": [\"Python\", \"React\", \"Docker\"]}"
        )
        
        text_sample = text[:3000]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text_sample}
                ],
                max_tokens=250,
                temperature=0.0
            )
            
            import json
            ans = response.choices[0].message.content.strip()
            
            # Clean up markdown if the LLM accidentally wraps it
            if ans.startswith("```json"):
                ans = ans[7:-3].strip()
            elif ans.startswith("```"):
                ans = ans[3:-3].strip()
                
            data = json.loads(ans)
            is_valid = data.get("is_valid", True)
            skills = data.get("skills", [])
            if not isinstance(skills, list):
                skills = []
            tokens = response.usage.total_tokens if response.usage else 0
            return is_valid, skills, tokens
        except Exception as e:
            print(f"Error analyzing resume via LLM: {e}")
            # Fallback to regex if LLM fails
            found_skills = set()
            text_lower = text.lower()
            for skill in self.common_skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                    found_skills.add(skill.title() if len(skill) > 3 else skill.upper())
            return True, list(found_skills), 0

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

        is_valid, skills, tokens = self._analyze_resume(text)
        
        if not is_valid:
            return {"parsed_status": "error", "message": "The uploaded document does not appear to be a valid resume. Please upload a professional CV or Resume."}

        name = self._extract_name(text)
        
        # Simple heuristic for experience for now (can be improved with LLM later)
        experience = [{"company": "Various", "role": "Professional", "duration": "See Resume"}]

        return {
            "name": name,
            "skills": skills,
            "experience": experience,
            "raw_text": text,
            "tokens": tokens,
            "parsed_status": "success"
        }

    def parse_pdf(self, file_path: str) -> dict:
        """Legacy wrapper"""
        return self.parse_file(file_path)
