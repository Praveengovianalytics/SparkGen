import hashlib
from typing import List, Sequence

import numpy as np


class Embedder:
    """
    Lightweight, dependency-free embedder that produces deterministic vectors.
    Designed for starter projects to avoid heavy external services.
    """

    def __init__(self, dimensions: int = 128) -> None:
        """
        Initializes the Embedder instance.

        Args:
            dimensions (int): Size of the embedding vector to generate.
        """
        self.dimensions = dimensions

    def _token_vector(self, token: str) -> np.ndarray:
        """
        Convert a token into a deterministic vector using hashing.
        """
        # Use SHA-256 to ensure consistent token representation.
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        # Expand digest to the requested dimensions by repeating.
        repeat_count = (self.dimensions + len(digest) - 1) // len(digest)
        expanded = (digest * repeat_count)[: self.dimensions]
        return np.frombuffer(expanded, dtype=np.uint8).astype(np.float32)

    def embed(self, text: str) -> List[float]:
        """
        Generates an embedding vector for the provided text.
        """
        tokens = text.split()
        if not tokens:
            return [0.0] * self.dimensions

        vectors = [self._token_vector(token) for token in tokens]
        stacked = np.stack(vectors)
        mean_vector = stacked.mean(axis=0)
        norm = np.linalg.norm(mean_vector)
        if norm == 0:
            return [0.0] * self.dimensions
        normalized = (mean_vector / norm).tolist()
        return normalized

    def embed_documents(self, documents: Sequence[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents.
        """
        return [self.embed(doc) for doc in documents]
