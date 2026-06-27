import sqlite3

try:
    conn = sqlite3.connect('interview_iq_v2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT interview_id, question_evaluations FROM reports ORDER BY created_at DESC LIMIT 1")
    res = cursor.fetchone()
    if res:
        print("Interview ID:", res[0])
        print("Evals length:", len(res[1]) if res[1] else 0)
        print("Raw Evals:", res[1])
    else:
        print("No reports found.")
    conn.close()
except Exception as e:
    print("Error:", e)
