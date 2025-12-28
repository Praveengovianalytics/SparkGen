import json
from pathlib import Path
from typing import List, Dict

from {{ cookiecutter.project_slug }}.retrievers.retriever import Retriever


class RAGEvaluator:
    """
    Tiny evaluator that measures whether the retriever surfaces expected context.
    """

    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.retriever = Retriever()
        self.dataset = self._load_dataset()
        self._index_corpus()

    def _load_dataset(self) -> List[Dict]:
        if not self.dataset_path.exists():
            return []
        try:
            return json.loads(self.dataset_path.read_text())
        except json.JSONDecodeError:
            return []

    def _index_corpus(self) -> None:
        corpus = [item["context"] for item in self.dataset if "context" in item]
        metadatas = [{"source": item.get("source", f"doc-{idx}")} for idx, item in enumerate(self.dataset)]
        if corpus:
            self.retriever.add_texts(corpus, metadatas=metadatas)

    def evaluate(self) -> List[Dict]:
        """
        For each query, ensure the top retrieval contains the expected snippet.
        """
        results: List[Dict] = []
        for item in self.dataset:
            query = item.get("query", "")
            expected = item.get("expected_answer", "")
            retrieved = self.retriever.retrieve(query)
            top_text = retrieved[0]["text"] if retrieved else ""
            passed = expected.lower() in top_text.lower()
            results.append(
                {
                    "query": query,
                    "expected": expected,
                    "retrieved": top_text,
                    "passed": passed,
                }
            )
        return results
