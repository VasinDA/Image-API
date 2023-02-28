from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from .models import APIImage

class ImageSerializer(serializers.ModelSerializer):
   user = serializers.HiddenField(default=serializers.CurrentUserDefault())
   urls = serializers.URLField(read_only=True, allow_blank=True)
   image = serializers.FileField(write_only=True, validators=[FileExtensionValidator(['jpg','jpeg','png'])])
   
   class Meta:
       model = APIImage
       fields = ('id','image','user', 'urls')

class DeteilImageSerializer(serializers.ModelSerializer):
   user = serializers.HiddenField(default=serializers.CurrentUserDefault())
   urls = serializers.URLField(read_only=True, allow_blank=True)
   
   class Meta:
       model = APIImage
       fields = ('id','user', 'urls')

