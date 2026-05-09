from __future__ import annotations

import socket
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class ServiceCheck:
  name: str
  host: str
  port: int
  available: bool
  error: str | None = None


# Read an environment variable with a fallback value.
def get_env(name: str, default: str) -> str:
  import os

  return os.getenv(name, default)


# Parse a network URL into host and port.
def parse_service_url(url: str, default_port: int) -> tuple[str, int]:
  parsed = urlparse(url)
  host = parsed.hostname or "localhost"
  port = parsed.port or default_port
  return host, port


# Check whether a TCP service is reachable.
def check_tcp_service(name: str, host: str, port: int, timeout: float = 3.0) -> ServiceCheck:
  try:
    with socket.create_connection((host, port), timeout=timeout):
      return ServiceCheck(name=name, host=host, port=port, available=True)
  except OSError as error:
    return ServiceCheck(
      name=name,
      host=host,
      port=port,
      available=False,
      error=str(error),
    )


# Check Redis availability through the configured broker URL.
def check_redis() -> ServiceCheck:
  broker_url = get_env("CELERY_BROKER_URL", "redis://localhost:6379/0")
  host, port = parse_service_url(broker_url, 6379)
  return check_tcp_service("redis", host, port)


# Check PostgreSQL availability through the configured database URL.
def check_postgres() -> ServiceCheck:
  database_url = get_env(
    "DATABASE_URL",
    "postgresql+psycopg://analytics:analytics@localhost:5432/analytics_platform",
  )
  normalized_url = database_url.replace("postgresql+psycopg://", "postgresql://")
  host, port = parse_service_url(normalized_url, 5432)
  return check_tcp_service("postgres", host, port)


# Check whether the Celery application can be imported.
def check_celery_import() -> ServiceCheck:
  try:
    from app.tasks.celery_app import celery_app

    task_count = len(celery_app.tasks)
    return ServiceCheck(
      name=f"celery_import_{task_count}_tasks",
      host="local",
      port=0,
      available=True,
    )
  except Exception as error:
    return ServiceCheck(
      name="celery_import",
      host="local",
      port=0,
      available=False,
      error=str(error),
    )


# Print a service check result.
def print_check(check: ServiceCheck) -> None:
  status = "OK" if check.available else "FAILED"

  if check.error:
    print(f"{check.name}: {status} ({check.host}:{check.port}) - {check.error}")
  else:
    print(f"{check.name}: {status} ({check.host}:{check.port})")


# Run all worker health checks.
def main() -> int:
  checks = [
    check_redis(),
    check_postgres(),
    check_celery_import(),
  ]

  for check in checks:
    print_check(check)

  failed = [check for check in checks if not check.available]
  return 1 if failed else 0


if __name__ == "__main__":
  raise SystemExit(main())