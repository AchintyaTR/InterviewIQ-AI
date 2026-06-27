import os
import sys

# Add project root to sys.path
sys.path.append(os.getcwd())

from ai.rag.retriever import RAGRetriever
from ai.question_generator.generator import QuestionGenerator

try:
    print('Testing RAGRetriever...')
    rag = RAGRetriever()
    print('RAGRetriever initialized')
    templates = rag.retrieve_relevant_templates(query='test', limit=2)
    print('Templates:', templates)
    
    print('Testing QuestionGenerator...')
    gen = QuestionGenerator()
    print('QuestionGenerator initialized')
    q = gen.generate_question('Python', 'Engineer', 'Tech', templates, [], 1)
    print('Question:', q)
except Exception as e:
    import traceback
    traceback.print_exc()
