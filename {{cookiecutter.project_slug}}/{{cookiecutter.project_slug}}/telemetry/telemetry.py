import requests
import time
import psutil

class Telemetry:
    def __init__(self, telemetry_endpoint: str):
        self.telemetry_endpoint = telemetry_endpoint
        self.session_id = int(time.time())

    def log_event(self, event_name: str, details: str):
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
            "timestamp": int(time.time())
        }

        # Send telemetry data to the endpoint
        try:
            response = requests.post(self.telemetry_endpoint, json=event_data)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Telemetry error: {e}")