import sqlite3

try:
    conn = sqlite3.connect('interview_iq_v2.db')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE interviews ADD COLUMN interview_mode VARCHAR DEFAULT 'voice'")
    conn.commit()
    print("Successfully added interview_mode column.")
    conn.close()
except Exception as e:
    print("Error:", e)
