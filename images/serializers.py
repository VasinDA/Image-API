from rest_framework import serializers
from PIL import Image
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('id','image')
        model = Image