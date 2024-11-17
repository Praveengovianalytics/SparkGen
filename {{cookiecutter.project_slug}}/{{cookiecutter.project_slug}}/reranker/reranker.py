from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer

# Define the re-ranker class
class Reranker:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Load a pre-trained embedding model (can be customized)
        self.model = SentenceTransformer(model_name)
        
    def encode(self, text: List[str]) -> np.ndarray:
        """Encodes a list of sentences into embeddings."""
        return self.model.encode(text)
    
    def rerank(self, query: str, candidates: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        """Re-ranks candidates based on similarity to the query."""
        # Encode the query and candidates
        # Compute similarity between the query and each candidate        
        # Combine candidates with their similarity scores and sort them
        # Return the top-k most similar candidates
        return ranked_candidates[:top_k]