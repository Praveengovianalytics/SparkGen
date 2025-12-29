"""Lightweight channel connectors for posting agent responses to chat apps."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from {{ cookiecutter.project_slug }}.channel.config import load_channel_configs


@dataclass
class ChannelClient:
    """Base channel client."""

    name: str

    def send_message(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError


@dataclass
class SlackWebhookChannel(ChannelClient):
    webhook_url: str

    def send_message(self, text: str) -> Dict[str, Any]:
        response = requests.post(self.webhook_url, json={"text": text})
        return {
            "ok": response.ok,
            "status_code": response.status_code,
            "response": response.text,
        }


@dataclass
class TeamsWebhookChannel(ChannelClient):
    webhook_url: str

    def send_message(self, text: str) -> Dict[str, Any]:
        payload = {"text": text}
        response = requests.post(self.webhook_url, json=payload)
        return {
            "ok": response.ok,
            "status_code": response.status_code,
            "response": response.text,
        }


@dataclass
class TelegramChannel(ChannelClient):
    bot_token: str
    chat_id: str

    def send_message(self, text: str) -> Dict[str, Any]:
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": text}
        response = requests.post(url, json=payload)
        body = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
        return {
            "ok": response.ok and body.get("ok", False),
            "status_code": response.status_code,
            "response": body or response.text,
        }


@dataclass
class WhatsAppChannel(ChannelClient):
    api_url: str
    token: str
    phone_number_id: str
    to_number: str

    def send_message(self, text: str) -> Dict[str, Any]:
        endpoint = f"{self.api_url}/{self.phone_number_id}/messages"
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {
            "messaging_product": "whatsapp",
            "to": self.to_number,
            "type": "text",
            "text": {"body": text},
        }
        response = requests.post(endpoint, headers=headers, json=payload)
        body = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
        return {
            "ok": response.ok,
            "status_code": response.status_code,
            "response": body or response.text,
        }


def build_channel_clients(channel_configs: List[Dict[str, Any]]) -> Dict[str, ChannelClient]:
    """Instantiate channel clients from configuration."""

    clients: Dict[str, ChannelClient] = {}
    for cfg in channel_configs:
        if not cfg.get("active", True):
            continue
        name = cfg["name"]
        settings = cfg.get("settings") or {}
        channel_type = cfg["type"].lower()
        client: Optional[ChannelClient] = None
        if channel_type == "slack" and settings.get("webhook_url"):
            client = SlackWebhookChannel(name=name, webhook_url=settings["webhook_url"])
        elif channel_type == "teams" and settings.get("webhook_url"):
            client = TeamsWebhookChannel(name=name, webhook_url=settings["webhook_url"])
        elif channel_type == "telegram" and settings.get("bot_token") and settings.get("chat_id"):
            client = TelegramChannel(name=name, bot_token=settings["bot_token"], chat_id=settings["chat_id"])
        elif channel_type == "whatsapp" and all(
            settings.get(key) for key in ["api_url", "token", "phone_number_id", "to_number"]
        ):
            client = WhatsAppChannel(
                name=name,
                api_url=settings["api_url"],
                token=settings["token"],
                phone_number_id=settings["phone_number_id"],
                to_number=settings["to_number"],
            )
        if client:
            clients[name] = client
    return clients


def load_and_build_channel_clients(config_path: str) -> Dict[str, ChannelClient]:
    configs = load_channel_configs(config_path)
    return build_channel_clients(configs)
