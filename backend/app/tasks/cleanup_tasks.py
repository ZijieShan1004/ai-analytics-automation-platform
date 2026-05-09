from app.tasks.celery_app import celery_app


# Run a placeholder cleanup task.
@celery_app.task(name="cleanup_old_processing_artifacts")
def cleanup_old_processing_artifacts() -> dict[str, str]:
    return {"status": "ok"}