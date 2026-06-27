import os
import sys
import time

sys.path.append(os.getcwd())
from ai.question_generator.generator import QuestionGenerator

print('Testing QuestionGenerator...')
start_time = time.time()
try:
    gen = QuestionGenerator()
    q = gen.generate_next_question(
        candidate_profile={"skills": ["Python", "React"]},
        history=[{"role": "system", "content": "Hello"}, {"role": "user", "content": "Hi"}],
        rag_templates=[]
    )
    print("Success! Generated in", time.time() - start_time, "seconds")
    print("Result:", q)
except Exception as e:
    print("Error:", e)
