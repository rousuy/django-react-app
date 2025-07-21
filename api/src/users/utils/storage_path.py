import uuid

from django.db import models


def avatar_dir_path(instance: models.Model, filename: str) -> str:
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"

    return f"profile_avatar-{instance.user.id}-{unique_filename}"  # type: ignore[attr-defined]
