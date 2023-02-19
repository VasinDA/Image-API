from django.db import models
from django.utils import timezone

class Plan(models.Model):
    title = models.CharField(max_length=50)
    image_url = models.ImageField(upload_to='images/')
    expires_after = models.IntegerField(default=300)

    def generate_link_with_expiration(self):
        expires_at = timezone.now() + timezone.timedelta(seconds=self.expires_after)
        link = Plan.objects.create(image_url=self.image_url, expires_at=expires_at)
        return link.image_url
    
    
    

    

    
