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
        self._stores: Dict[str, Dict[str, List]] = {}

    def _get_store(self, index: str) -> Dict[str, List]:
        """Return a named index store, creating it if needed."""

        if index not in self._stores:
            self._stores[index] = {"vectors": [], "documents": [], "metadatas": []}
        return self._stores[index]

    def add_documents(
        self, documents: List[str], metadatas: Optional[List[Dict]] = None, index: str = "default"
    ) -> None:
        """
        Add documents and optional metadata to a named index.
        """

        metadatas = metadatas or [{} for _ in documents]
        if len(metadatas) != len(documents):
            raise ValueError("metadatas length must match documents length.")

        embeddings = self.embedder.embed_documents(documents)
        store = self._get_store(index)
        for doc, metadata, embedding in zip(documents, metadatas, embeddings):
            metadata_with_index = dict(metadata)
            metadata_with_index.setdefault("index", index)
            store["documents"].append(doc)
            store["metadatas"].append(metadata_with_index)
            store["vectors"].append(np.array(embedding, dtype=np.float32))

    @staticmethod
    def _similarity(query_vector: np.ndarray, vectors: List[np.ndarray]) -> List[Tuple[int, float]]:
        """
        Compute cosine similarity between the query vector and stored vectors.
        """

        similarities: List[Tuple[int, float]] = []
        for idx, vector in enumerate(vectors):
            denom = np.linalg.norm(vector) * np.linalg.norm(query_vector)
            if denom == 0:
                score = 0.0
            else:
                score = float(np.dot(vector, query_vector) / denom)
            similarities.append((idx, score))
        return similarities

    def search(self, query: str, top_k: int = 3, indexes: Optional[List[str]] = None) -> List[Dict]:
        """
        Search for the top_k most similar documents across one or more indexes.
        """

        query_vector = np.array(self.embedder.embed(query), dtype=np.float32)
        if not self._stores:
            return []

        target_indexes = indexes or list(self._stores.keys())
        results = []
        for index in target_indexes:
            store = self._stores.get(index)
            if not store:
                continue
            similarities = self._similarity(query_vector, store["vectors"])
            for idx, score in similarities:
                results.append(
                    {
                        "text": store["documents"][idx],
                        "metadata": store["metadatas"][idx],
                        "score": score,
                    }
                )
        ranked = sorted(results, key=lambda item: item["score"], reverse=True)[:top_k]
        return ranked

    def reset(self) -> None:
        """
        Clear all stored vectors and documents.
        """

        self._stores = {}
