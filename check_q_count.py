import sqlite3

try:
    conn = sqlite3.connect('interview_iq_v2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM questions WHERE interview_id = 'f0627ba93eca4e1fa0e8a8e374f1bb7b'")
    print("Questions count:", cursor.fetchone()[0])
    
    cursor.execute("SELECT count(*) FROM responses WHERE question_id IN (SELECT id FROM questions WHERE interview_id = 'f0627ba93eca4e1fa0e8a8e374f1bb7b')")
    print("Responses count:", cursor.fetchone()[0])
    conn.close()
except Exception as e:
    print("Error:", e)
