from rest_framework import serializers
from PIL import Image
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
   user = serializers.HiddenField(default=serializers.CurrentUserDefault())

   class Meta:
       model = Image
       fields = ('id','image','user',)
