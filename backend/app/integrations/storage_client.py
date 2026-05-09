import hashlib
import uuid
from pathlib import Path

from app.core.config import get_settings

settings = get_settings()


class LocalStorageClient:
    def __init__(self):
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    # Save uploaded file content to local storage.
    def save_upload(self, original_filename: str, content: bytes) -> dict[str, str]:
        suffix = Path(original_filename).suffix.lower()
        stored_filename = f"{uuid.uuid4()}{suffix}"
        file_path = self.upload_dir / stored_filename
        file_path.write_bytes(content)
        checksum = hashlib.sha256(content).hexdigest()

        return {
            "stored_filename": stored_filename,
            "file_path": str(file_path),
            "checksum": checksum,
        }