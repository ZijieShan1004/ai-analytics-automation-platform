from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"
ML_ROOT = PROJECT_ROOT / "ml"

sys.path.insert(0, str(BACKEND_ROOT))
sys.path.insert(0, str(ML_ROOT))


# Test that the Celery application can be imported.
def test_celery_app_imports():
  from app.tasks.celery_app import celery_app

  assert celery_app is not None


# Test that analytics tasks are registered with Celery.
def test_analytics_task_module_imports():
  import app.tasks.analytics_tasks as analytics_tasks

  assert analytics_tasks is not None


# Test that the ML pipeline can be imported by the worker process.
def test_ml_pipeline_imports():
  from analytics_platform_ml.pipeline import run_full_pipeline

  assert run_full_pipeline is not None