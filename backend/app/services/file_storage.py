"""
File storage service for image uploads.
"""

import os
import uuid
import aiofiles
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


class FileStorageService:
    """Handles saving, validating and deleting uploaded image files."""

    def __init__(self, upload_dir: str = settings.UPLOAD_DIR):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def _get_medicine_dir(self, medicine_id: uuid.UUID) -> Path:
        """Return per-medicine directory, creating it if needed."""
        path = self.upload_dir / "medicines" / str(medicine_id)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _validate_file(self, file: UploadFile) -> None:
        """Validate content type and size."""
        if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"File type '{file.content_type}' not allowed. "
                       f"Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}",
            )

    def _make_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename preserving the extension."""
        suffix = Path(original_filename).suffix.lower()
        return f"{uuid.uuid4().hex}{suffix}"

    async def save_image(
        self,
        file: UploadFile,
        medicine_id: uuid.UUID,
    ) -> dict:
        """
        Save an uploaded image to the local filesystem.
        Returns a dict with file_path, original_filename, file_size, mime_type.
        """
        self._validate_file(file)

        medicine_dir = self._get_medicine_dir(medicine_id)
        unique_name = self._make_unique_filename(file.filename or "image.jpg")
        file_path = medicine_dir / unique_name

        content = await file.read()
        file_size = len(content)

        # Size check
        max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE_MB}MB.",
            )

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        # Return relative path for DB storage
        relative_path = f"medicines/{medicine_id}/{unique_name}"
        return {
            "file_path": relative_path,
            "original_filename": file.filename,
            "file_size": file_size,
            "mime_type": file.content_type,
        }

    def delete_image(self, file_path: str) -> None:
        """Delete an image file from disk. Silent if already missing."""
        full_path = self.upload_dir / file_path
        try:
            full_path.unlink(missing_ok=True)
        except Exception:
            pass  # Non-critical, log in production


file_storage_service = FileStorageService()
