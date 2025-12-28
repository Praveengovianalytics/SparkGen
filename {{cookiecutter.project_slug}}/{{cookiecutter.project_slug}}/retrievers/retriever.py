from typing import Dict, List, Optional

from {{ cookiecutter.project_slug }}.embeddings.embedder import Embedder
from {{ cookiecutter.project_slug }}.vectordatabase.vector_store import InMemoryVectorStore


class Retriever:
    """
    Minimal retriever that wraps the in-memory vector store.
    """

    def __init__(
        self,
        vector_store: Optional[InMemoryVectorStore] = None,
        embedder: Optional[Embedder] = None,
        top_k: int = 3,
    ) -> None:
        self.vector_store = vector_store or InMemoryVectorStore(embedder=embedder)
        self.top_k = top_k

    def add_texts(
        self, texts: List[str], metadatas: Optional[List[Dict]] = None
    ) -> None:
        """
        Index a batch of texts with optional metadata.
        """
        self.vector_store.add_documents(texts, metadatas)

    def retrieve(self, query: str) -> List[Dict]:
        """
        Return the most relevant documents for a query.
        """
        return self.vector_store.search(query, top_k=self.top_k)
