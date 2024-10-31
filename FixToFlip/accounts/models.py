from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseAccount(AbstractUser):
    last_login = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.username
