"""Send Bamboo build logs to Azure Event Hub."""

import argparse
import os
import sys
from pathlib import Path
from typing import Iterable, Optional

from azure.eventhub import EventData, EventHubProducerClient


def _iter_log_lines(log_path: Path) -> Iterable[str]:
    with log_path.open("r", encoding="utf-8") as log_file:
        for line in log_file:
            stripped = line.rstrip("\n")
            if stripped:
                yield stripped


def _send_logs_to_eventhub(
    connection_string: str, eventhub_name: str, log_path: Path, batch_size_hint: int = 250
) -> None:
    client = EventHubProducerClient.from_connection_string(
        conn_str=connection_string, eventhub_name=eventhub_name
    )
    with client:
        batch = client.create_batch()
        for entry in _iter_log_lines(log_path):
            try:
                batch.add(EventData(entry))
            except ValueError:
                client.send_batch(batch)
                batch = client.create_batch()
                batch.add(EventData(entry))
            if len(batch) >= batch_size_hint:
                client.send_batch(batch)
                batch = client.create_batch()
        if len(batch) > 0:
            client.send_batch(batch)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Push Bamboo logs to Azure Event Hub.")
    parser.add_argument(
        "--log-file",
        required=True,
        help="Path to the Bamboo log file that should be pushed.",
    )
    parser.add_argument(
        "--connection-string",
        default=os.getenv("AZURE_EVENTHUB_CONNECTION_STRING"),
        help="Azure Event Hub connection string (defaults to AZURE_EVENTHUB_CONNECTION_STRING).",
    )
    parser.add_argument(
        "--eventhub-name",
        default=os.getenv("AZURE_EVENTHUB_NAME"),
        help="Azure Event Hub name (defaults to AZURE_EVENTHUB_NAME).",
    )

    args = parser.parse_args(argv)

    if not args.connection_string or not args.eventhub_name:
        print(
            "Missing Azure Event Hub configuration. "
            "Set AZURE_EVENTHUB_CONNECTION_STRING and AZURE_EVENTHUB_NAME or pass the flags explicitly.",
            file=sys.stderr,
        )
        return 1

    log_path = Path(args.log_file)
    if not log_path.exists():
        print(f"Log file not found at {log_path}", file=sys.stderr)
        return 1

    _send_logs_to_eventhub(
        connection_string=args.connection_string,
        eventhub_name=args.eventhub_name,
        log_path=log_path,
    )
    print(f"Sent logs from {log_path} to Event Hub {args.eventhub_name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
