import sqlite3
import requests

try:
    conn = sqlite3.connect('interview_iq_v2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM interviews WHERE status = 'in_progress' LIMIT 1")
    row = cursor.fetchone()
    
    if not row:
        print("No active interview found.")
    else:
        interview_id = row[0]
        print(f"Found active interview: {interview_id}")
        
        # We need a valid token. Create one or login.
        token_res = requests.post('http://localhost:8000/api/v1/auth/token', data={'username': 'testuser@example.com', 'password': 'password123'})
        token = token_res.json().get('access_token')
        
        if not token:
            print("Login failed, trying to register...")
            requests.post('http://localhost:8000/api/v1/auth/register', json={'email': 'testuser2@example.com', 'password': 'password123', 'full_name': 'Test'})
            token_res = requests.post('http://localhost:8000/api/v1/auth/token', data={'username': 'testuser2@example.com', 'password': 'password123'})
            token = token_res.json().get('access_token')
            
        print("Sending respond request...")
        headers = {'Authorization': f'Bearer {token}'}
        res = requests.post(f'http://localhost:8000/api/v1/interviews/{interview_id}/respond', headers=headers, json={'answer_text': 'I used Python.'}, timeout=15)
        print("Status:", res.status_code)
        print("Response:", res.text)
except Exception as e:
    print("Error:", e)
