from {{ cookiecutter.project_slug }}.evaluation.evaluator import RAGEvaluator
from {{ cookiecutter.project_slug }}.telemetry.telemetry import Telemetry


class EvaluationAgent:
    """
    Lightweight agent that runs RAG evaluation and reports summary results.
    """

    def __init__(self, evaluator: RAGEvaluator, telemetry: Telemetry):
        self.evaluator = evaluator
        self.telemetry = telemetry

    def execute(self, user_query: str):
        self.telemetry.log_event("evaluation_start", user_query)
        results = self.evaluator.evaluate()
        passed = sum(1 for item in results if item["passed"])
        total = len(results)
        summary = {"passed": passed, "total": total, "results": results}
        self.telemetry.log_event("evaluation_complete", f"{passed}/{total} tests passed")
        return summary
