from pathlib import Path

from {{ cookiecutter.project_slug }}.channel.config import load_channel_configs
from {{ cookiecutter.project_slug }}.channel.connectors import build_channel_clients


def test_channel_config_env_resolution(tmp_path: Path, monkeypatch):
    config_path = tmp_path / "channels.yaml"
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/abc")
    config_path.write_text(
        """
channels:
  - name: slack_support
    type: slack
    settings:
      webhook_url: ${SLACK_WEBHOOK_URL}
"""
    )

    configs = load_channel_configs(str(config_path))
    assert configs[0]["settings"]["webhook_url"] == "https://hooks.slack.com/services/abc"


def test_build_channel_clients_skips_inactive():
    configs = [
        {"name": "slack_support", "type": "slack", "active": False, "settings": {"webhook_url": "url"}},
        {"name": "teams_updates", "type": "teams", "active": True, "settings": {"webhook_url": "url"}},
    ]

    clients = build_channel_clients(configs)
    assert "slack_support" not in clients
    assert "teams_updates" in clients
