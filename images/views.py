from rest_framework import generics
from .models import Image
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated

from .serializers import ImageSerializer

class ListImage(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(user=user)

class DetailsImage(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class OriginalView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    def get(self, request, pk):
        image = Image.objects.get(pk=pk)
        image_url = image.image.url[1:]
        with open(image_url, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/jpeg")