from typing import Dict, List, Optional, Tuple

import numpy as np

from {{ cookiecutter.project_slug }}.embeddings.embedder import Embedder


class InMemoryVectorStore:
    """
    A simple in-memory vector store powered by NumPy for similarity search.
    Suitable for starter projects without external database dependencies.
    """

    def __init__(self, embedder: Optional[Embedder] = None) -> None:
        self.embedder = embedder or Embedder()
        self._vectors: List[np.ndarray] = []
        self._documents: List[str] = []
        self._metadatas: List[Dict] = []

    def add_documents(
        self, documents: List[str], metadatas: Optional[List[Dict]] = None
    ) -> None:
        """
        Add documents and optional metadata to the store.
        """
        metadatas = metadatas or [{} for _ in documents]
        if len(metadatas) != len(documents):
            raise ValueError("metadatas length must match documents length.")

        embeddings = self.embedder.embed_documents(documents)
        for doc, metadata, embedding in zip(documents, metadatas, embeddings):
            self._documents.append(doc)
            self._metadatas.append(metadata)
            self._vectors.append(np.array(embedding, dtype=np.float32))

    def _similarity(self, query_vector: np.ndarray) -> List[Tuple[int, float]]:
        """
        Compute cosine similarity between the query vector and stored vectors.
        """
        similarities: List[Tuple[int, float]] = []
        for idx, vector in enumerate(self._vectors):
            denom = np.linalg.norm(vector) * np.linalg.norm(query_vector)
            if denom == 0:
                score = 0.0
            else:
                score = float(np.dot(vector, query_vector) / denom)
            similarities.append((idx, score))
        return similarities

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search for the top_k most similar documents to the query.
        """
        query_vector = np.array(self.embedder.embed(query), dtype=np.float32)
        if not self._vectors:
            return []

        similarities = self._similarity(query_vector)
        ranked = sorted(similarities, key=lambda pair: pair[1], reverse=True)[:top_k]
        results = []
        for idx, score in ranked:
            results.append(
                {
                    "text": self._documents[idx],
                    "metadata": self._metadatas[idx],
                    "score": score,
                }
            )
        return results

    def reset(self) -> None:
        """
        Clear all stored vectors and documents.
        """
        self._vectors = []
        self._documents = []
        self._metadatas = []
