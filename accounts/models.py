from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    plan = models.ForeignKey('plans.Plan', on_delete=models.CASCADE, null=True, blank=True)