from django.db import models

class Plan(models.Model):
    title = models.CharField(max_length=50)
    image_file = models.FileField()