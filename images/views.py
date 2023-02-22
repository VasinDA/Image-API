from rest_framework import generics
from .models import Image
from rest_framework.views import APIView
from django.http import HttpResponse
import os
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

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

class OriginalView(APIView):
    def image_original(request, pk):
        image_path = 'media/user_3/acc19d46-8067-4408-bd93-891bc1a1823c/full.jpg'
        image_full_path = os.path.join(settings.BASE_DIR, image_path)
        with open(image_full_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")