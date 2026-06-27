import sqlite3

try:
    conn = sqlite3.connect('interview_iq_v2.db')
    cursor = conn.cursor()
    
    print("--- USERS ---")
    cursor.execute("SELECT id, email FROM users")
    print(cursor.fetchall())
    
    print("--- INTERVIEWS ---")
    cursor.execute("SELECT id, user_id, status FROM interviews")
    interviews = cursor.fetchall()
    print(interviews)
    
    print("--- QUESTIONS ---")
    cursor.execute("SELECT id, interview_id, order_index FROM questions")
    questions = cursor.fetchall()
    print(questions)
    
    print("--- RESPONSES ---")
    cursor.execute("SELECT id, question_id, response_text FROM responses")
    responses = cursor.fetchall()
    print(responses)
    
    conn.close()
except Exception as e:
    print("Error:", e)
