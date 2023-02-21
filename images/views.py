from rest_framework import generics
from .models import Image
from .serializers import ImageSerializer

class ListImage(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class DetailsImage(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer