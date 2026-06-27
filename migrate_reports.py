import sqlite3

try:
    conn = sqlite3.connect('interview_iq_v2.db')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE reports ADD COLUMN question_evaluations JSON")
    conn.commit()
    print("Successfully added question_evaluations column.")
    conn.close()
except Exception as e:
    print("Error:", e)
