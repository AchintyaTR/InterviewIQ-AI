import os
import sys
import time
from dotenv import load_dotenv

sys.path.append(os.getcwd())
load_dotenv()

from ai.question_generator.generator import QuestionGenerator

print('Testing QuestionGenerator with .env...')
start_time = time.time()
try:
    gen = QuestionGenerator()
    q = gen.generate_next_question(
        candidate_profile={"skills": ["Python", "React"], "target_role": "Developer"},
        history=[{"role": "system", "content": "Hello"}, {"role": "user", "content": "Hi"}],
        rag_templates=[]
    )
    print("Success! Generated in", time.time() - start_time, "seconds")
    print("Result:", q)
except Exception as e:
    print("Error:", e)
