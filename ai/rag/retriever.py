import os
import chromadb
from chromadb.utils import embedding_functions

class RAGRetriever:
    """
    RAG retriever helper module interfaces with ChromaDB
    to query role-specific and company-specific question templates.
    """
    def __init__(self, persist_directory: str = "data/chroma_db"):
        os.makedirs(persist_directory, exist_ok=True)
        # Initialize ChromaDB persistent client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Use default sentence transformer embedding function
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        # Get or create the main collection for interview questions
        self.collection = self.client.get_or_create_collection(
            name="interview_templates",
            embedding_function=self.embedding_function
        )

    def add_templates(self, texts: list[str], metadatas: list[dict], ids: list[str]):
        """
        Adds question templates to the vector database.
        """
        if not texts:
            return
            
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def retrieve_relevant_templates(self, query: str, limit: int = 3) -> list:
        """
        Queries similarity matching vectors matching target parameters (query string).
        """
        if self.collection.count() == 0:
            # Fallback if DB is empty
            return [
                {
                    "topic": "System Design",
                    "question": "How would you design a highly scalable message processing service?"
                },
                {
                    "topic": "Coding Round",
                    "question": "Implement an algorithm to detect loops in a directed graph."
                }
            ]

        results = self.collection.query(
            query_texts=[query],
            n_results=limit
        )
        
        templates = []
        if results and results["documents"] and len(results["documents"]) > 0:
            for i, doc in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i] if results["metadatas"] else {}
                templates.append({
                    "topic": meta.get("topic", "General"),
                    "question": doc
                })
                
        return templates
