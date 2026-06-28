import os
from datetime import datetime

LOG_FILE = "/app/logs/tokens.txt" if os.path.exists("/app") else os.path.join(os.getcwd(), "logs", "tokens.txt")

def log_token_usage(session_id: str, step_name: str, tokens: int):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Session: {session_id} | Step: {step_name} | Tokens Used: {tokens}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
