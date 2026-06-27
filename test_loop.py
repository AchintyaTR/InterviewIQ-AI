import os
import requests
import uuid

API = 'http://localhost:8000/api/v1'

email = f"test_{uuid.uuid4().hex[:8]}@example.com"
requests.post(f"{API}/auth/register", json={"email": email, "password": "pass", "full_name": "Test"})
token = requests.post(f"{API}/auth/token", data={"username": email, "password": "pass"}).json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

with open("mock_resume.pdf", 'rb') as f:
    res = requests.post(f"{API}/resumes/upload", headers=headers, files={"file": ("mock_resume.pdf", f, "application/pdf")})
resume_id = res.json()["resume_id"]

start_res = requests.post(f"{API}/interviews/start", headers=headers, json={"resume_id": resume_id, "target_role": "Dev", "target_company": "Tech"})
interview_id = start_res.json()["interview_id"]

for i in range(1, 6):
    print(f"Submitting Q{i}...")
    res = requests.post(f"{API}/interviews/{interview_id}/respond", headers=headers, json={"answer_text": f"Answer {i}"}, timeout=15)
    print(f"Status Q{i}:", res.status_code)
    print(f"Text Q{i}:", res.text[:200])
    
print("Done!")
