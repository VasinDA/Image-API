from rest_framework import serializers
from .models import Images

class ImageSerializer(serializers.ModelSerializer):
   user = serializers.HiddenField(default=serializers.CurrentUserDefault())
   urls = serializers.URLField(read_only=True, allow_blank=True)
   image = serializers.FileField(write_only=True)
   
   class Meta:
       model = Images
       fields = ('id','image','user', 'urls')



