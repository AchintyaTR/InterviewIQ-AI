import os
import requests
from reportlab.pdfgen import canvas

# Create a valid minimal PDF
pdf_path = "valid_resume.pdf"
c = canvas.Canvas(pdf_path)
c.drawString(100, 750, "John Doe Resume")
c.drawString(100, 730, "Skills: Python, React, AWS")
c.save()

# Login
token_res = requests.post('http://localhost:8000/api/v1/auth/token', data={'username': 'testuser@example.com', 'password': 'password123'})
token = token_res.json().get('access_token')
print("Token:", token)

headers = {'Authorization': f'Bearer {token}'}

# Upload
with open(pdf_path, 'rb') as f:
    upload_res = requests.post('http://localhost:8000/api/v1/resumes/upload', headers=headers, files={'file': ('valid_resume.pdf', f, 'application/pdf')})
print("Upload status:", upload_res.status_code)
print("Upload response:", upload_res.text)

if upload_res.status_code == 202:
    resume_id = upload_res.json()['resume_id']
    
    # Start
    start_res = requests.post('http://localhost:8000/api/v1/interviews/start', headers=headers, json={'resume_id': resume_id, 'target_role': 'Developer', 'target_company': 'Tech'})
    print("Start status:", start_res.status_code)
    print("Start response:", start_res.text)
