"""
Helpers to scaffold starter Spec-as-Code projects.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional


class TemplateError(ValueError):
    """Raised when an init template cannot be applied."""


def init_template(template_name: str, destination: str) -> Path:
    """
    Copy a template directory into the destination.
    """
    template_dir = Path(__file__).parent / "templates" / template_name
    if not template_dir.exists():
        raise TemplateError(f"Unknown template '{template_name}'. Available templates: rag_agentic")

    dest_path = Path(destination)
    dest_path.mkdir(parents=True, exist_ok=True)
    for item in template_dir.iterdir():
        target = dest_path / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy(item, target)
    return dest_path
