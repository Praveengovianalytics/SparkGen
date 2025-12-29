from pathlib import Path

import pytest
import yaml

from {{ cookiecutter.project_slug }}.config.errors import SpecValidationError
from {{ cookiecutter.project_slug }}.config.spec_loader import WorkflowSpecLoader


def _write_basic_files(tmp_path: Path) -> Path:
    prompts_dir = tmp_path / "prompts"
    contexts_dir = tmp_path / "contexts"
    guardrails_dir = tmp_path / "guardrails"
    agents_docs_dir = guardrails_dir / "agents"
    prompts_dir.mkdir()
    contexts_dir.mkdir()
    guardrails_dir.mkdir()
    agents_docs_dir.mkdir()
    prompt_path = prompts_dir / "agent.md"
    context_path = contexts_dir / "context.md"
    prompt_path.write_text("You are an agent.")
    context_path.write_text("Context block.")
    (guardrails_dir / "README.md").write_text("Guardrail docs.")
    (guardrails_dir / "workflow.md").write_text("Workflow guardrails.")
    (agents_docs_dir / "a1.md").write_text("Agent A1 guardrails.")

    default_guardrails = {
        "allowed_categories": ["safety"],
        "documentation": "guardrails/README.md",
        "workflow_doc": "guardrails/workflow.md",
        "apply_sets": ["baseline"],
        "sets": [
            {
                "name": "baseline",
                "docs": "guardrails/README.md",
                "rules": [
                    {
                        "name": "empty_input",
                        "description": "Block empty input.",
                        "categories": ["safety"],
                        "applies_to": ["input"],
                        "mode": "block",
                        "severity": "medium",
                        "priority": 1,
                        "patterns": ["^\\s*$"],
                        "tests": [{"prompt": "", "expected_outcome": "block"}],
                    }
                ],
            }
        ],
    }
    (guardrails_dir / "default_guardrails.yaml").write_text(yaml.safe_dump(default_guardrails))

    spec = {
        "version": "v1",
        "name": "test",
        "description": "spec test",
        "entry_agent": "a1",
        "environment": "dev",
        "guardrails": {
            "defaults_path": "guardrails/default_guardrails.yaml",
            "documentation": "guardrails/README.md",
            "workflow_doc": "guardrails/workflow.md",
            "apply_sets": ["baseline"],
            "sets": [],
        },
        "rag": {
            "enabled": False,
            "retriever": "in_memory",
            "top_k": 3,
            "embedding_model": "local",
            "chunking": {"size": 100, "overlap": 10, "strategy": "sliding_window"},
            "citations": False,
            "collection": "demo",
        },
        "storage": {
            "vector_store": {"backend": "local_memory", "collection": "c", "credentials": {"token": "${TOKEN}"}},
            "document_store": {"backend": "filesystem", "path": "./docs", "credentials": {}},
            "memory_store_path": ".mem.json",
        },
        "memory": {
            "short_term": {"store": "memory_store", "ttl_messages": 5, "summarization_policy": "truncate"},
            "long_term": {"store": "vector_store", "ttl_messages": None, "summarization_policy": "summarize"},
        },
        "tools": {"builtin": ["get_delivery_date"]},
        "agents": [
            {
                "name": "a1",
                "role": "alpha",
                "prompt_file": str(prompt_path.relative_to(tmp_path)),
                "context_file": str(context_path.relative_to(tmp_path)),
                "tools": ["get_delivery_date"],
                "memory": {"short_term": True, "long_term": False},
                "guardrails": {"use_sets": ["baseline"], "overrides": [], "doc": "guardrails/agents/a1.md"},
            }
        ],
        "handoffs": [],
        "observability": {
            "logging": "basic",
            "tracing": True,
            "metrics": True,
            "telemetry_endpoint": "http://localhost",
            "langfuse_host": None,
            "langfuse_public_key_env": None,
            "langfuse_secret_key_env": None,
        },
        "llm": {"provider": "openai", "model": "gpt-4o-mini", "api_key_env": "LLM_API_KEY", "use_agents_sdk": False},
        "environments": {"staging": {"rag": {"top_k": 1}}},
    }

    spec_path = tmp_path / "workflow.yaml"
    spec_path.write_text(yaml.safe_dump(spec))
    return spec_path


def test_loader_validates_and_applies_overrides(tmp_path: Path):
    spec_path = _write_basic_files(tmp_path)
    loader = WorkflowSpecLoader(str(spec_path), environment="staging")
    spec = loader.load()
    assert spec.environment == "staging"
    assert spec.rag.top_k == 1
    assert spec.entry_agent == "a1"


def test_missing_prompt_raises(tmp_path: Path):
    spec_path = _write_basic_files(tmp_path)
    data = yaml.safe_load(spec_path.read_text())
    data["agents"][0]["prompt_file"] = "missing.md"
    spec_path.write_text(yaml.safe_dump(data))
    loader = WorkflowSpecLoader(str(spec_path))
    with pytest.raises(SpecValidationError):
        loader.load()


def test_unknown_tool_detection(tmp_path: Path):
    spec_path = _write_basic_files(tmp_path)
    data = yaml.safe_load(spec_path.read_text())
    data["agents"][0]["tools"] = ["missing_tool"]
    spec_path.write_text(yaml.safe_dump(data))
    with pytest.raises(SpecValidationError):
        WorkflowSpecLoader(str(spec_path)).load()


def test_circular_handoff_detection(tmp_path: Path):
    spec_path = _write_basic_files(tmp_path)
    data = yaml.safe_load(spec_path.read_text())
    data["agents"].append(
        {
            "name": "a2",
            "role": "beta",
            "prompt_file": data["agents"][0]["prompt_file"],
            "context_file": data["agents"][0]["context_file"],
            "tools": ["get_delivery_date"],
            "memory": {"short_term": True, "long_term": False},
            "guardrails": {"use_sets": ["baseline"], "overrides": [], "doc": "guardrails/agents/a1.md"},
        }
    )
    data["handoffs"] = [{"source": "a1", "target": "a2", "trigger": "always"}, {"source": "a2", "target": "a1"}]
    spec_path.write_text(yaml.safe_dump(data))
    with pytest.raises(SpecValidationError):
        WorkflowSpecLoader(str(spec_path)).load()


def test_missing_kb_context_raises(tmp_path: Path):
    spec_path = _write_basic_files(tmp_path)
    data = yaml.safe_load(spec_path.read_text())
    data["rag"]["enabled"] = True
    data["rag"]["knowledge_bases"] = [
        {
            "name": "kb1",
            "description": "test kb",
            "collection": "kb1_collection",
            "contexts": ["contexts/missing.md"],
        }
    ]
    spec_path.write_text(yaml.safe_dump(data))
    with pytest.raises(SpecValidationError):
        WorkflowSpecLoader(str(spec_path)).load()


def test_unknown_default_kb_raises(tmp_path: Path):
    spec_path = _write_basic_files(tmp_path)
    data = yaml.safe_load(spec_path.read_text())
    data["rag"]["enabled"] = True
    data["rag"]["knowledge_bases"] = [
        {
            "name": "kb1",
            "description": "test kb",
            "collection": "kb1_collection",
            "contexts": [data["agents"][0]["context_file"]],
        }
    ]
    data["rag"]["default_knowledge_bases"] = ["kb1", "missing_kb"]
    spec_path.write_text(yaml.safe_dump(data))
    with pytest.raises(SpecValidationError):
        WorkflowSpecLoader(str(spec_path)).load()


def test_vector_store_requires_backend_config(tmp_path: Path):
    spec_path = _write_basic_files(tmp_path)
    data = yaml.safe_load(spec_path.read_text())
    data["storage"]["vector_store"]["backend"] = "azure_ai_search"
    data["storage"]["vector_store"].pop("azure_ai_search", None)
    spec_path.write_text(yaml.safe_dump(data))
    with pytest.raises(SpecValidationError):
        WorkflowSpecLoader(str(spec_path)).load()


def test_vector_store_faiss_requires_index(tmp_path: Path):
    spec_path = _write_basic_files(tmp_path)
    data = yaml.safe_load(spec_path.read_text())
    data["storage"]["vector_store"]["backend"] = "faiss"
    data["storage"]["vector_store"].pop("path", None)
    data["storage"]["vector_store"].pop("faiss", None)
    spec_path.write_text(yaml.safe_dump(data))
    with pytest.raises(SpecValidationError):
        WorkflowSpecLoader(str(spec_path)).load()


def test_vector_store_azure_msi_mutual_exclusion(tmp_path: Path):
    spec_path = _write_basic_files(tmp_path)
    data = yaml.safe_load(spec_path.read_text())
    data["storage"]["vector_store"]["backend"] = "azure_ai_search"
    data["storage"]["vector_store"]["azure_ai_search"] = {
        "endpoint": "https://search.example.com",
        "index_name": "idx",
        "auth": {"use_msi": True, "api_key_env": "${API_KEY}"},
    }
    spec_path.write_text(yaml.safe_dump(data))
    with pytest.raises(SpecValidationError):
        WorkflowSpecLoader(str(spec_path)).load()
