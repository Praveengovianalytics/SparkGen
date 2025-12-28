"""
Utility to evaluate a running API instance against the bundled RAG dataset.
"""

import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

from {{ cookiecutter.project_slug }}.telemetry.telemetry import Telemetry


def main():
    load_dotenv()
    dataset_path = Path(__file__).parent / "{{cookiecutter.project_slug}}" / "evaluation" / "rag_dataset.json"
    samples = json.loads(dataset_path.read_text())
    telemetry = Telemetry(
        telemetry_endpoint=os.getenv("TELEMETRY_ENDPOINT", "http://localhost:8000/telemetry"),
        langfuse_config={
            "host": os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
            "public_key": os.getenv("LANGFUSE_PUBLIC_KEY", ""),
            "secret_key": os.getenv("LANGFUSE_SECRET_KEY", ""),
        },
    )
    for sample in samples:
        payload = {"query": sample["query"]}
        started = time.time()
        response = requests.post("http://localhost:8000/agent/invoke", json=payload, timeout=5)
        latency_ms = (time.time() - started) * 1000
        telemetry.log_api_trace("/agent/invoke", response.status_code, latency_ms)
        try:
            data = response.json()
        except Exception:
            data = {"error": "invalid json"}
        print({"query": sample["query"], "status": response.status_code, "latency_ms": latency_ms, "response": data})


if __name__ == "__main__":
    main()
