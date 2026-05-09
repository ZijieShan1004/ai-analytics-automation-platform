from pathlib import Path

from fastapi import HTTPException, status

from app.core.config import get_settings

settings = get_settings()


# Return the lowercase extension of a filename.
def get_file_extension(filename: str | None) -> str:
    if filename is None:
        return ""

    return Path(filename).suffix.lower()


# Validate uploaded file name, extension, and size.
def validate_upload_file(filename: str | None, content: bytes) -> None:
    if filename is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing filename")

    extension = get_file_extension(filename)

    if extension not in settings.get_allowed_extensions():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type")

    max_size_bytes = settings.max_upload_size_mb * 1024 * 1024

    if len(content) > max_size_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")

    if len(content) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file")