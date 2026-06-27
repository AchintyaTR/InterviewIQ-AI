import sqlite3

try:
    conn = sqlite3.connect('interview_iq_v2.db')
    cursor = conn.cursor()
    
    interview_id = 'f0627ba9-3eca-4e1f-a0e8-a8e374f1bb7b'
    
    cursor.execute("SELECT question_evaluations FROM reports WHERE interview_id = ?", (interview_id,))
    res = cursor.fetchone()
    print("Report found:", res is not None)
    if res:
        print("Evals:", res[0])
        
    conn.close()
except Exception as e:
    print("Error:", e)
