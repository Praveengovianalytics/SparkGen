import os
from typing import Dict, Any


class ConfigLoader:
    """
    Basic configuration loader that reads environment variables while providing
    sensible defaults from cookiecutter inputs. This allows the generated
    project to quickly experiment with single-agent or multi-agent flows.
    """

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from environment variables with defaults that can be
        overridden at runtime.

        Returns:
            Dict[str, Any]: configuration mapping for the runtime components.
        """
        return {
            "api_key": os.getenv("LLM_API_KEY", "your-api-key"),
            "model_name": os.getenv("LLM_MODEL_NAME", "gpt-4o-mini"),
            "multi_agent_mode": os.getenv(
                "MULTI_AGENT_MODE", "{{ cookiecutter.multi_agent_mode }}"
            ),
            "api_framework": os.getenv("API_FRAMEWORK", "{{ cookiecutter.api_framework }}"),
            "observability": os.getenv("OBSERVABILITY", "{{ cookiecutter.observability }}"),
            "telemetry_endpoint": os.getenv(
                "TELEMETRY_ENDPOINT", "https://telemetry.example.com/events"
            ),
            "openai_agent_sdk": os.getenv("OPENAI_AGENT_SDK", "{{ cookiecutter.openai_agent_sdk }}"),
            "openai_agent_id": os.getenv("OPENAI_AGENT_ID"),
            "mlflow_tracking_uri": os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"),
            "langfuse_host": os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
            "langfuse_public_key": os.getenv("LANGFUSE_PUBLIC_KEY", "your-public-key"),
            "langfuse_secret_key": os.getenv("LANGFUSE_SECRET_KEY", "your-secret-key"),
            "guardrail_banned_terms": os.getenv("GUARDRAIL_BANNED_TERMS", ""),
            "guardrail_max_output_len": os.getenv("GUARDRAIL_MAX_OUTPUT_LEN", "2000"),
        }
