import importlib
import importlib.util
import time
from typing import Any, Dict, Optional

import psutil  # To track system metrics like CPU, memory, etc.
import requests


class Telemetry:
    """
    A simple telemetry class to log events and send performance metrics to a remote server,
    with optional MLflow and Langfuse hooks.
    """

    def __init__(
        self,
        telemetry_endpoint: str,
        mlflow_tracking_uri: Optional[str] = None,
        langfuse_config: Optional[Dict[str, str]] = None,
    ):
        self.telemetry_endpoint = telemetry_endpoint
        self.session_id = int(time.time())  # Unique session ID based on the timestamp
        self.mlflow_client = self._resolve_mlflow_client(mlflow_tracking_uri)
        self.langfuse_client = self._resolve_langfuse_client(langfuse_config)

    def _resolve_mlflow_client(self, tracking_uri: Optional[str]):
        if not tracking_uri:
            return None
        spec = importlib.util.find_spec("mlflow")
        if spec is None or spec.name is None:
            return None
        mlflow = importlib.import_module(spec.name)
        mlflow.set_tracking_uri(tracking_uri)
        return mlflow

    def _resolve_langfuse_client(self, langfuse_config: Optional[Dict[str, str]]):
        if not langfuse_config:
            return None
        spec = importlib.util.find_spec("langfuse")
        if spec is None or spec.name is None:
            return None
        langfuse_module = importlib.import_module(spec.name)
        return langfuse_module.Langfuse(  # type: ignore[attr-defined]
            public_key=langfuse_config.get("public_key"),
            secret_key=langfuse_config.get("secret_key"),
            host=langfuse_config.get("host"),
        )

    def log_event(self, event_name: str, details: str):
        """
        Logs an event to local console, telemetry endpoint, MLflow, and Langfuse (if configured).
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()

        event_data = {
            "session_id": self.session_id,
            "cpu_usage": cpu_usage,
            "memory_total": memory_info.total,
            "memory_used": memory_info.used,
            "memory_percent": memory_info.percent,
            "event_name": event_name,
            "details": details,
            "timestamp": int(time.time()),
        }

        try:
            requests.post(self.telemetry_endpoint, json=event_data, timeout=2)
        except Exception:
            # Fail open; telemetry should not crash the app.
            pass

        if self.mlflow_client:
            try:
                with self.mlflow_client.start_run(run_name=f"session-{self.session_id}"):
                    self.mlflow_client.log_params({"session_id": self.session_id, "event": event_name})
                    self.mlflow_client.log_metrics(
                        {"cpu_usage": cpu_usage, "memory_percent": memory_info.percent}
                    )
            except Exception:
                pass

        if self.langfuse_client:
            try:
                self.langfuse_client.trace(  # type: ignore[attr-defined]
                    name=event_name,
                    input=details,
                    metadata={"session_id": self.session_id, "cpu_usage": cpu_usage},
                )
            except Exception:
                pass
