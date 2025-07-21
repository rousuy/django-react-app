from __future__ import annotations

from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from src.users.models.profile_model import Profile
from src.users.models.user_model import User


@receiver(post_save, sender=User)
def create_user_profile(
    sender: type[User],
    instance: User,
    *,
    created: bool,
    **kwargs: dict[str, Any],
) -> None:
    """
    Signal to automatically create a user profile when a new user is created.

    Args:
        sender: The model class that sent the signal (User)
        instance: The actual instance of the User model that was saved
        created: Boolean indicating if this is a new record
        **kwargs: Additional keyword arguments
    """
    if created:
        Profile.objects.create(
            user=instance,
            first_name="",
            last_name="",
        )
