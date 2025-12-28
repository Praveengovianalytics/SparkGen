"""
Centralized guardrail scaffolding.

Define pre- and post-execution guardrails that can be composed per agent or
globally. Extend these with custom checks (PII, safety, domain rules) as needed.
"""

import re
from typing import Callable, Dict, List, Optional


class GuardrailViolation(Exception):
    """Raised when a guardrail is violated."""


class GuardrailManager:
    def __init__(
        self,
        pre: Optional[List[Callable[[str], None]]] = None,
        post: Optional[List[Callable[[str], None]]] = None,
        scrubbers: Optional[List[Callable[[str], str]]] = None,
    ):
        self.pre = pre or []
        self.post = post or []
        self.scrubbers = scrubbers or []

    def run_pre(self, user_input: str):
        for check in self.pre:
            check(user_input)

    def run_post(self, output: str) -> str:
        sanitized = output
        for scrubber in self.scrubbers:
            sanitized = scrubber(sanitized)
        for check in self.post:
            check(sanitized)
        return sanitized


# Example, configurable policies
def block_empty_input(text: str):
    if not text or not text.strip():
        raise GuardrailViolation("Empty input is not allowed.")


def block_banned_terms(banned: List[str]):
    def _checker(text: str):
        lowered = text.lower()
        if any(term.lower() in lowered for term in banned):
            raise GuardrailViolation("Input contains banned terms.")
    return _checker


def limit_output_length(max_len: int = 2000):
    def _checker(text: str):
        if text and len(text) > max_len:
            raise GuardrailViolation(f"Output exceeds {max_len} characters.")
    return _checker


def scrub_emails(text: str) -> str:
    """
    Redact email-like strings to protect PII in outputs.
    """
    email_regex = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    return email_regex.sub("[REDACTED_EMAIL]", text)


def build_default_guardrails(config: Dict) -> GuardrailManager:
    """
    Build default guardrails using config-driven policies.
    """
    banned_terms = config.get("guardrail_banned_terms", "").split(",") if config.get("guardrail_banned_terms") else []
    max_len = int(config.get("guardrail_max_output_len", 2000))

    pre_checks = [block_empty_input]
    if banned_terms:
        pre_checks.append(block_banned_terms([term.strip() for term in banned_terms if term.strip()]))
    post_checks = [limit_output_length(max_len)]

    scrubbers = [scrub_emails]

    return GuardrailManager(pre=pre_checks, post=post_checks, scrubbers=scrubbers)
