$ErrorActionPreference = "Stop"

if (-not $env:PYTHONPATH) {
  $env:PYTHONPATH = "backend;ml"
}
else {
  $env:PYTHONPATH = "$env:PYTHONPATH;backend;ml"
}

if (-not $env:CELERY_LOG_LEVEL) {
  $env:CELERY_LOG_LEVEL = "info"
}

if (-not $env:CELERY_WORKER_NAME) {
  $env:CELERY_WORKER_NAME = "analytics-worker@%h"
}

if ($env:CELERY_QUEUES) {
  celery -A app.tasks.celery_app.celery_app worker `
    --loglevel=$env:CELERY_LOG_LEVEL `
    --hostname=$env:CELERY_WORKER_NAME `
    --queues=$env:CELERY_QUEUES
}
else {
  celery -A app.tasks.celery_app.celery_app worker `
    --loglevel=$env:CELERY_LOG_LEVEL `
    --hostname=$env:CELERY_WORKER_NAME
}