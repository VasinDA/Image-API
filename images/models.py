import uuid
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'full.{0}'.format(ext)
    return 'user_{0}/{1}/{2}'.format(instance.user.id, uuid.uuid4(), filename)

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, 
            validators=[FileExtensionValidator(['jpg','png'])])
    expires_at = models.IntegerField(default=300)