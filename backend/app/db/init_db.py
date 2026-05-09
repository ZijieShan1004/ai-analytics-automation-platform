from pathlib import Path

from app.core.config import get_settings

settings = get_settings()


# Create local storage directories required by the application.
def init_storage() -> None:
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)