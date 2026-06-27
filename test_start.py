import os
import requests
from backend.app.database.connection import SessionLocal
from backend.app.models.user import User
from backend.app.models.resume import Resume

db = SessionLocal()
user = db.query(User).filter(User.email == 'test_fetch@example.com').first()

if user:
    # create fake resume
    res = Resume(user_id=user.id, file_path='fake.pdf', extracted_skills=['Python'], extracted_experience=[])
    db.add(res)
    db.commit()
    db.refresh(res)
    
    # get token
    token_res = requests.post('http://localhost:8000/api/v1/auth/token', data={'username': 'test_fetch@example.com', 'password': 'password'})
    token = token_res.json().get('access_token')
    
    # start interview
    headers = {'Authorization': f'Bearer {token}'}
    data = {'resume_id': str(res.id), 'target_role': 'Engineer', 'target_company': 'Tech'}
    resp = requests.post('http://localhost:8000/api/v1/interviews/start', json=data, headers=headers)
    print("STATUS CODE:", resp.status_code)
    print("RESPONSE:", resp.text)
