import uuid
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'full.{0}'.format(ext)
    return 'user_{0}/{1}/{2}'.format(instance.user.id, uuid.uuid4(), filename)

class Images(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, 
            validators=[FileExtensionValidator(['jpg','png', 'jpeg'])], max_length=512)
    expires_after = models.IntegerField(default=300)
    created_time = models.DateTimeField(auto_now_add=True)

    @property
    def urls(self):
        return self._urls
    
    @urls.setter
    def urls(self, value):
        self._urls = value
    
    