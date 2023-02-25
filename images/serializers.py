from rest_framework import serializers
from PIL import Image
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
   user = serializers.HiddenField(default=serializers.CurrentUserDefault())
   urls = serializers.URLField(read_only=True, allow_blank=True)
   image = serializers.FileField(write_only=True)
   
   class Meta:
       model = Image
       fields = ('id','image','user', 'urls')



