import re
from django.db import models
from django.core.exceptions import ValidationError


def validate_available_hights(value):
    pattern = '^[0-9,]+$'
    if not re.match(pattern, value):
        raise ValidationError("It should be integers only (e.g. '200' or '100,200')")
    return value

class Plan(models.Model):
    title = models.CharField(max_length=50)
    original_image_link = models.BooleanField(default=False)
    binary_image_link = models.BooleanField(default=False)
    available_hights = models.CharField(max_length=200, 
        help_text="Comma separated list of heights (e.g. '100,200')", 
        validators =[validate_available_hights], default='')
    
    def __str__(self):
        return self.title

    
    

    

    
