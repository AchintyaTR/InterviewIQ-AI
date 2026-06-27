import os
import requests
import uuid

API = 'http://localhost:8000/api/v1'

# 1. Create a mock PDF
from reportlab.pdfgen import canvas
pdf_path = "mock_resume.pdf"
c = canvas.Canvas(pdf_path)
c.drawString(100, 750, "Mock Resume")
c.drawString(100, 730, "Skills: Python, React")
c.save()

# 2. Register / Login
email = f"test_{uuid.uuid4().hex[:8]}@example.com"
requests.post(f"{API}/auth/register", json={"email": email, "password": "pass", "full_name": "Test"})
token = requests.post(f"{API}/auth/token", data={"username": email, "password": "pass"}).json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 3. Upload Resume
with open(pdf_path, 'rb') as f:
    res = requests.post(f"{API}/resumes/upload", headers=headers, files={"file": ("mock_resume.pdf", f, "application/pdf")})
resume_id = res.json()["resume_id"]

# 4. Start Interview
start_res = requests.post(f"{API}/interviews/start", headers=headers, json={"resume_id": resume_id, "target_role": "Dev", "target_company": "Tech"})
interview_id = start_res.json()["interview_id"]

# 5. Respond
print("Sending respond request...")
try:
    respond_res = requests.post(f"{API}/interviews/{interview_id}/respond", headers=headers, json={"answer_text": "I like python."}, timeout=10)
    print("Respond status:", respond_res.status_code)
    print("Respond text:", respond_res.text)
except Exception as e:
    print("Respond error:", e)
