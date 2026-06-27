import sqlite3

try:
    conn = sqlite3.connect('interview_iq_v2.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    print("Users count:", cursor.fetchone()[0])
    
    cursor.execute("SELECT COUNT(*) FROM interviews")
    print("Interviews count:", cursor.fetchone()[0])
    
    conn.close()
except Exception as e:
    print("Error:", e)
