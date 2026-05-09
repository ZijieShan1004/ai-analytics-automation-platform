from __future__ import annotations

import json
import sys
from typing import Any


# Load the backend Celery application.
def load_celery_app():
  from app.tasks.celery_app import celery_app

  return celery_app


# Convert Celery inspect output into printable JSON.
def print_json(data: Any) -> None:
  print(json.dumps(data, indent=2, default=str))


# Fetch active worker task information.
def show_active() -> int:
  celery_app = load_celery_app()
  inspector = celery_app.control.inspect(timeout=3)
  print_json(inspector.active() or {})
  return 0


# Fetch scheduled worker task information.
def show_scheduled() -> int:
  celery_app = load_celery_app()
  inspector = celery_app.control.inspect(timeout=3)
  print_json(inspector.scheduled() or {})
  return 0


# Fetch reserved worker task information.
def show_reserved() -> int:
  celery_app = load_celery_app()
  inspector = celery_app.control.inspect(timeout=3)
  print_json(inspector.reserved() or {})
  return 0


# Fetch registered task information.
def show_registered() -> int:
  celery_app = load_celery_app()
  inspector = celery_app.control.inspect(timeout=3)
  print_json(inspector.registered() or {})
  return 0


# Fetch worker statistics.
def show_stats() -> int:
  celery_app = load_celery_app()
  inspector = celery_app.control.inspect(timeout=3)
  print_json(inspector.stats() or {})
  return 0


# Ping available Celery workers.
def show_ping() -> int:
  celery_app = load_celery_app()
  inspector = celery_app.control.inspect(timeout=3)
  print_json(inspector.ping() or {})
  return 0


# Route a command to the matching Celery inspection action.
def main() -> int:
  command = sys.argv[1] if len(sys.argv) > 1 else "ping"

  commands = {
    "active": show_active,
    "scheduled": show_scheduled,
    "reserved": show_reserved,
    "registered": show_registered,
    "stats": show_stats,
    "ping": show_ping,
  }

  if command not in commands:
    print("Usage: python workers/celery_status.py [ping|active|scheduled|reserved|registered|stats]")
    return 1

  return commands[command]()


if __name__ == "__main__":
  raise SystemExit(main())