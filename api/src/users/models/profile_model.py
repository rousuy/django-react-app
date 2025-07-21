from django.db import models
from django.utils.translation import gettext_lazy as _

from src.users.models.user_model import User
from src.users.utils.storage_path import avatar_dir_path


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name=_("User"))
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone number"))
    avatar = models.ImageField(upload_to=avatar_dir_path, blank=True, null=True, verbose_name=_("Avatar"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
