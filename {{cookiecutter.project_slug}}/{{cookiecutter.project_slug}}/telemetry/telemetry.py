import requests
import time
import psutil  # To track system metrics like CPU, memory, etc.

class Telemetry:
    """
    A simple telemetry class to log events and send performance metrics to a remote server.
    """

    def __init__(self, telemetry_endpoint: str):
        """
        Initializes the telemetry system with a remote endpoint for sending telemetry data.

        Args:
            telemetry_endpoint (str): The URL endpoint where telemetry data will be sent.
        """
        self.telemetry_endpoint = telemetry_endpoint
        self.session_id = int(time.time())  # Unique session ID based on the timestamp

    def log_event(self, event_name: str, details: str):
        """
        Logs an event to the local file and sends it to the telemetry server.

        Args:
            event_name (str): Name of the event to log.
            details (str): Additional information about the event.
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
            "timestamp": int(time.time())
        }

        response = requests.post(self.telemetry_endpoint, json=event_data)


telemetry = Telemetry("https://mock-telemetry-server.com/api/telemetry")
telemetry.log_event("AppStart", "The application has started successfully.")