from rest_framework.views import APIView
from rest_framework import generics
from .models import Image
from django.shortcuts import  get_object_or_404
from django.http import HttpResponse, FileResponse
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
        image =  get_object_or_404(Image, pk=pk)
        image_url = image.image.url[1:]
        with open(image_url, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/jpeg")

class BinaryView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    def get(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        image_url = image.image.url[1:]
        return FileResponse(open(image_url, 'rb'), as_attachment=True, filename='binary.jpg')

class LinkView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    def get(self, request, pk, pk1, pk2):
        image = get_object_or_404(Image, image='user_{0}/{1}/{2}'.format(pk, pk1, pk2))
        image_url = image.image.url[1:]
        with open(image_url, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/jpeg")

class ThumbnailView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    def get(self, request, pk, pk1):
        image = get_object_or_404(Image, pk=pk)
        image_url = image.image.url[:-8]
        with open('{0}{2}.[a-z]+'.format(image_url[1:], pk1), 'rb') as f:
            return HttpResponse(f.read(), content_type="image/jpeg")