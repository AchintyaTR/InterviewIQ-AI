import sqlite3

try:
    conn = sqlite3.connect('interview_iq.db')
    cursor = conn.cursor()
    
    print("--- RESUMES ---")
    cursor.execute("SELECT id, user_id FROM resumes")
    print(cursor.fetchall())
    
    print("--- INTERVIEWS ---")
    cursor.execute("SELECT id, user_id, resume_id, status FROM interviews")
    print(cursor.fetchall())
    
    print("--- QUESTIONS ---")
    cursor.execute("SELECT id, interview_id, order_index FROM questions")
    print(cursor.fetchall())
    
    conn.close()
except Exception as e:
    print("Error:", e)
