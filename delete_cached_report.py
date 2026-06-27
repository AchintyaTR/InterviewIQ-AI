import sqlite3

try:
    conn = sqlite3.connect('interview_iq_v2.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reports WHERE interview_id = 'f0627ba93eca4e1fa0e8a8e374f1bb7b'")
    conn.commit()
    print("Successfully deleted the cached report.")
    conn.close()
except Exception as e:
    print("Error:", e)
