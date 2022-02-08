from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
import uuid
import os


class Company(AbstractUser):
    def get_upload_path(self, filename):
        return os.path.join("companies", self.username, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        verbose_name="Company username for authorization",
        error_messages={"unique": "Username already exists."},
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
    )
    name = models.CharField(
        max_length=128,
        verbose_name="Name of company",
        unique=True,
        error_messages={"unique": "A company with that name already exists."},
    )
    description = models.CharField(max_length=1000)
    legal_address = models.CharField(max_length=1000)
    image = models.ImageField(upload_to=get_upload_path, default="default_image.png")
