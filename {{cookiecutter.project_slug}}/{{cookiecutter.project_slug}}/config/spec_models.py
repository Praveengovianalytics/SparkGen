"""
Pydantic models for the Spec-as-Code workflow description.

These models purposely mirror the YAML shape so that validation, JSON Schema
generation, and runtime wiring share a single source of truth.
"""

from __future__ import annotations

import re
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


ENV_REF_PATTERN = re.compile(r"^\\${[A-Z0-9_]+}$")


def _ensure_env_ref(value: str) -> str:
    if not ENV_REF_PATTERN.match(value):
        raise ValueError("Credentials must be provided as ${ENV_VAR} references.")
    return value


class ChunkingConfig(BaseModel):
    size: int = Field(default=500, description="Chunk size in tokens/characters.")
    overlap: int = Field(default=50, description="Chunk overlap to preserve context.")
    strategy: Literal["sliding_window", "sentence", "recursive"] = "sliding_window"


class RerankerConfig(BaseModel):
    enabled: bool = False
    provider: Literal["none", "local", "cross_encoder"] = "none"
    top_n: int = 3


class RAGConfig(BaseModel):
    enabled: bool = True
    retriever: Literal["in_memory", "stub"] = "in_memory"
    top_k: int = 3
    embedding_model: str = "local-hash-128"
    chunking: ChunkingConfig = Field(default_factory=ChunkingConfig)
    reranker: Optional[RerankerConfig] = None
    citations: bool = True
    collection: str = "sparkgen"


class MemoryWindow(BaseModel):
    store: Literal["memory_store", "vector_store", "document_store"] = "memory_store"
    ttl_messages: Optional[int] = Field(default=20, description="Number of messages to retain.")
    summarization_policy: Literal["truncate", "summarize"] = "summarize"


class MemoryConfig(BaseModel):
    short_term: MemoryWindow = Field(default_factory=MemoryWindow)
    long_term: MemoryWindow = Field(
        default_factory=lambda: MemoryWindow(ttl_messages=None, summarization_policy="summarize")
    )


class VectorStoreConfig(BaseModel):
    backend: Literal["local_memory", "chroma_stub"] = "local_memory"
    collection: str = "sparkgen_vectors"
    path: Optional[str] = None
    credentials: Dict[str, str] = Field(default_factory=dict)

    @field_validator("credentials")
    @classmethod
    def validate_credentials(cls, value: Dict[str, str]) -> Dict[str, str]:
        for _, val in value.items():
            _ensure_env_ref(val)
        return value


class DocumentStoreConfig(BaseModel):
    backend: Literal["filesystem", "stub"] = "filesystem"
    path: str = "data/docs"
    credentials: Dict[str, str] = Field(default_factory=dict)

    @field_validator("credentials")
    @classmethod
    def validate_credentials(cls, value: Dict[str, str]) -> Dict[str, str]:
        for _, val in value.items():
            _ensure_env_ref(val)
        return value


class StorageConfig(BaseModel):
    vector_store: VectorStoreConfig = Field(default_factory=VectorStoreConfig)
    document_store: DocumentStoreConfig = Field(default_factory=DocumentStoreConfig)
    memory_store_path: str = ".sparkgen_memory.json"


class MCPTool(BaseModel):
    name: str
    resource: str
    description: Optional[str] = None
    active: bool = True
    rate_limit_per_minute: Optional[int] = None


class MCPConnector(BaseModel):
    name: str
    host: str = "localhost"
    port: int = 8000
    protocol: Literal["ws", "wss", "http"] = "ws"
    active: bool = True
    credentials: Dict[str, str] = Field(default_factory=dict)
    tools: List[MCPTool] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)

    @field_validator("credentials")
    @classmethod
    def validate_credentials(cls, value: Dict[str, str]) -> Dict[str, str]:
        for _, val in value.items():
            _ensure_env_ref(val)
        return value


class ToolRegistry(BaseModel):
    builtin: List[str] = Field(default_factory=lambda: ["get_delivery_date"])
    mcp_connectors: List[MCPConnector] = Field(default_factory=list)
    exposed_mcp_tools: List[str] = Field(default_factory=list)


class GuardrailSpec(BaseModel):
    banned_terms: List[str] = Field(default_factory=list)
    max_output_len: int = 2000


class AgentMemoryBinding(BaseModel):
    short_term: bool = True
    long_term: bool = False
    summary_prompt: Optional[str] = None


class AgentSpec(BaseModel):
    name: str
    role: str
    prompt_file: str
    context_file: Optional[str] = None
    tools: List[str] = Field(default_factory=list)
    memory: AgentMemoryBinding = Field(default_factory=AgentMemoryBinding)
    guardrails: GuardrailSpec = Field(default_factory=GuardrailSpec)
    handoff_notes: Optional[str] = None


class HandoffRule(BaseModel):
    source: str
    target: str
    trigger: str = "always"
    message_contract: str = "text"


class ObservabilityConfig(BaseModel):
    logging: Literal["basic", "verbose"] = "basic"
    tracing: bool = True
    metrics: bool = True
    run_id_env: Optional[str] = None
    telemetry_endpoint: Optional[str] = "https://telemetry.example.com/events"
    mlflow_tracking_uri: Optional[str] = None
    langfuse_host: Optional[str] = None
    langfuse_public_key_env: Optional[str] = None
    langfuse_secret_key_env: Optional[str] = None


class LLMConfig(BaseModel):
    provider: Literal["openai"] = "openai"
    model: str = "gpt-4o-mini"
    api_key_env: str = "LLM_API_KEY"
    use_agents_sdk: bool = False
    agent_id_env: Optional[str] = None


class WorkflowOverrides(BaseModel):
    rag: Optional[RAGConfig] = None
    storage: Optional[StorageConfig] = None
    memory: Optional[MemoryConfig] = None
    tools: Optional[ToolRegistry] = None
    observability: Optional[ObservabilityConfig] = None
    llm: Optional[LLMConfig] = None


class WorkflowSpec(BaseModel):
    version: Literal["v1"] = "v1"
    name: str
    description: Optional[str] = None
    entry_agent: str
    environment: str = "dev"
    rag: RAGConfig = Field(default_factory=RAGConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    tools: ToolRegistry = Field(default_factory=ToolRegistry)
    agents: List[AgentSpec]
    handoffs: List[HandoffRule] = Field(default_factory=list)
    observability: ObservabilityConfig = Field(default_factory=ObservabilityConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    environments: Dict[str, WorkflowOverrides] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_agents_and_entry(self):
        agent_names = {agent.name for agent in self.agents}
        if self.entry_agent not in agent_names:
            raise ValueError(f"entry_agent '{self.entry_agent}' is not defined in agents.")
        if len(agent_names) != len(self.agents):
            raise ValueError("Agent names must be unique.")

        if self.tools.builtin and "get_delivery_date" not in self.tools.builtin:
            self.tools.builtin.append("get_delivery_date")
        return self
