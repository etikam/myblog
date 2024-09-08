from django.db import models
from django.contrib.auth.models import AbstractUser

class user(AbstractUser):
    is_writer = models.BooleanField(default=False, verbose_name="Je suis Editeur")