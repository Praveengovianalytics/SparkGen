"""
Entry point for generated projects.

This module now supports a Spec-as-Code workflow (`sparksgen run workflow.yaml`),
an init helper (`sparksgen init --template rag_agentic`), JSON Schema export,
and the legacy pattern-based runner for backwards compatibility.
"""

import argparse
import json
from pathlib import Path
from typing import List

from {{ cookiecutter.project_slug }}.agents.agent import Agent, RouterManager
from {{ cookiecutter.project_slug }}.agents.eval_agent import EvaluationAgent
from {{ cookiecutter.project_slug }}.prompt.prompt_template import PromptTemplate
from {{ cookiecutter.project_slug }}.llms.base_llm import BaseLLM
from {{ cookiecutter.project_slug }}.tools.tools import assemble_tools
from {{ cookiecutter.project_slug }}.memory.memory import ChatMemory
from {{ cookiecutter.project_slug }}.telemetry.telemetry import Telemetry
from {{ cookiecutter.project_slug }}.config.config_loader import ConfigLoader
from {{ cookiecutter.project_slug }}.protocols.a2a_protocol import AgentToAgentProtocol
from {{ cookiecutter.project_slug }}.guardrails.policies import build_default_guardrails
from {{ cookiecutter.project_slug }}.evaluation.evaluator import RAGEvaluator
from {{ cookiecutter.project_slug }}.orchestration.spec_runtime import load_workflow
from {{ cookiecutter.project_slug }}.config.errors import SpecValidationError
from {{ cookiecutter.project_slug }}.config.spec_loader import WorkflowSpecLoader
from {{ cookiecutter.project_slug }}.config.spec_templates import init_template, TemplateError


def build_base_components(config, telemetry):
    llm = BaseLLM(
        {
            "api_key": config["api_key"],
            "model": config["model_name"],
            "use_agents": config.get("openai_agent_sdk") == "enabled",
            "agent_id": config.get("openai_agent_id"),
        }
    )
    prompt = PromptTemplate()
    memory = ChatMemory()
    guardrails = build_default_guardrails(config)
    return llm, prompt, memory, guardrails, telemetry


def build_single_agent_flow(config, telemetry):
    toolset = assemble_tools(config)
    llm, prompt, memory, guardrails, telemetry = build_base_components(config, telemetry)
    agent = Agent(
        llm=llm,
        tools=toolset,
        prompt=prompt.PROMPT_TEMPLATE,
        history=[],
        output_parser=lambda resp: resp,
        memory=memory,
        telemetry=telemetry,
        use_agents_sdk=config.get("openai_agent_sdk") == "enabled",
        guardrails=guardrails,
    )
    return agent


def build_router_manager_flow(config, telemetry):
    toolset = assemble_tools(config)
    llm, prompt, memory, guardrails, telemetry = build_base_components(config, telemetry)

    research_agent = Agent(
        llm=llm,
        tools=toolset,
        prompt=f"Research agent: {prompt.PROMPT_TEMPLATE}",
        history=["You are a research specialist."],
        output_parser=lambda resp: resp,
        memory=memory,
        telemetry=telemetry,
        use_agents_sdk=config.get("openai_agent_sdk") == "enabled",
        guardrails=guardrails,
    )

    coding_agent = Agent(
        llm=llm,
        tools=toolset,
        prompt=f"Coding agent: {prompt.PROMPT_TEMPLATE}",
        history=["You write code and return patches."],
        output_parser=lambda resp: resp,
        memory=memory,
        telemetry=telemetry,
        use_agents_sdk=config.get("openai_agent_sdk") == "enabled",
        guardrails=guardrails,
    )

    router = RouterManager(agents=[research_agent, coding_agent])
    return router


class SimplePlanner:
    """
    Minimal planner scaffold that selects an agent based on declared skills.
    """

    def __init__(self, protocol: AgentToAgentProtocol, agents):
        self.protocol = protocol
        self.agents = agents
        for idx, agent in enumerate(agents):
            self.protocol.register_agent(f"agent_{idx}", ["generic"])

    def plan_and_execute(self, user_query: str):
        # Naive strategy: pick first agent that has any skill.
        target_id = next(iter(self.protocol.registry.keys()))
        result = self.agents[0].execute(user_query)
        self.protocol.send_message("planner", target_id, f"executed:{user_query}")
        return result


def parse_args():
    parser = argparse.ArgumentParser(description="Run SparkGen agent flows.")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run a Spec-as-Code workflow.")
    run_parser.add_argument("workflow", help="Path to workflow.yaml")
    run_parser.add_argument("--env", dest="environment", help="Environment override (dev/staging/prod).")
    run_parser.add_argument("--query", help="User query for the workflow.")

    init_parser = subparsers.add_parser("init", help="Bootstrap a workflow from a template.")
    init_parser.add_argument("--template", default="rag_agentic", help="Template name to copy.")
    init_parser.add_argument("--output", default=".", help="Destination directory.")

    schema_parser = subparsers.add_parser("schema", help="Export JSON Schema for workflow.yaml")
    schema_parser.add_argument(
        "--output",
        default=str(Path.cwd() / "workflow.schema.json"),
        help="Path to write the JSON Schema.",
    )

    legacy_parser = subparsers.add_parser("legacy", help="Legacy runtime preserved for backward compatibility.")
    legacy_parser.add_argument(
        "--pattern",
        choices=["single-agent", "router-manager", "planner-builder", "evaluation"],
        help="Override the multi-agent pattern.",
    )
    legacy_parser.add_argument("--query", help="User query to send to the selected pattern.")
    legacy_parser.add_argument(
        "--dataset",
        default=str(Path(__file__).parent / "evaluation" / "rag_dataset.json"),
        help="Path to evaluation dataset for --pattern evaluation.",
    )

    parser.set_defaults(command="legacy")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == "run":
        try:
            runtime = load_workflow(args.workflow, environment=args.environment)
            result = runtime.run(args.query or "Hello! Can you summarize the project scope?")
            print(json.dumps(result, indent=2))
        except SpecValidationError as exc:
            raise SystemExit(f"[spec-validation] {exc}") from exc
        return

    if args.command == "init":
        try:
            dest = init_template(args.template, args.output)
            print(f"Template '{args.template}' copied into {dest}")
        except TemplateError as exc:
            raise SystemExit(str(exc)) from exc
        return

    if args.command == "schema":
        target = Path(args.output)
        WorkflowSpecLoader.write_schema(target)
        print(f"JSON Schema written to {target}")
        return

    config = ConfigLoader().load_config()
    mode = getattr(args, "pattern", None) or config.get("multi_agent_mode", "single-agent")
    user_query = getattr(args, "query", None) or "Hello! Can you summarize the project scope?"

    telemetry = Telemetry(
        telemetry_endpoint=config.get("telemetry_endpoint"),
        mlflow_tracking_uri=config.get("mlflow_tracking_uri"),
        langfuse_config={
            "host": config.get("langfuse_host"),
            "public_key": config.get("langfuse_public_key"),
            "secret_key": config.get("langfuse_secret_key"),
        },
    )
    telemetry.log_event("startup", f"Mode: {mode}")

    if mode == "router-manager":
        router = build_router_manager_flow(config, telemetry)
        result = router.route(user_query)
    elif mode == "planner-builder":
        router = build_router_manager_flow(config, telemetry)
        planner = SimplePlanner(protocol=AgentToAgentProtocol(), agents=router.agents)
        result = planner.plan_and_execute(user_query)
    elif mode == "evaluation":
        evaluator = RAGEvaluator(dataset_path=args.dataset)
        evaluation_agent = EvaluationAgent(evaluator=evaluator, telemetry=telemetry)
        result = evaluation_agent.execute(user_query or "Run evaluation suite.")
    else:
        agent = build_single_agent_flow(config, telemetry)
        result = agent.execute(user_query)

    print("Execution result:", result)


if __name__ == "__main__":
    main()
