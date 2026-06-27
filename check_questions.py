import sqlite3

try:
    conn = sqlite3.connect('interview_iq_v2.db')
    cursor = conn.cursor()
    
    interview_id = 'f0627ba9-3eca-4e1f-a0e8-a8e374f1bb7b'
    
    cursor.execute("SELECT count(*) FROM questions WHERE interview_id = ?", (interview_id,))
    q_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT count(*) FROM responses WHERE question_id IN (SELECT id FROM questions WHERE interview_id = ?)", (interview_id,))
    r_count = cursor.fetchone()[0]
    
    print(f"Questions: {q_count}, Responses: {r_count}")
    
    cursor.execute("SELECT question_text FROM questions WHERE interview_id = ?", (interview_id,))
    questions = cursor.fetchall()
    for i, q in enumerate(questions):
        print(f"Q{i+1}: {q[0]}")
        
    conn.close()
except Exception as e:
    print("Error:", e)
