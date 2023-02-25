from rest_framework import generics
from .models import Image
from plans.models import Plan
from django.shortcuts import  get_object_or_404
from django.http import HttpResponse, FileResponse
from rest_framework.permissions import IsAuthenticated
from .serializers import ImageSerializer

class ListImage(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        image_ojects = Image.objects.filter(user=user)
        plan = Plan.objects.get(id=user.plan_id)
        available_hights = plan.available_hights.split(',')
        for image in image_ojects:
            urls = []
            for hight in available_hights:
                urls.append('http://127.0.0.1:8000/api/v1/image/{0}/thumbnail/{1}'.format(image.id, hight))
            if plan.original_image_link == 1:
                urls.append(('http://127.0.0.1:8000/api/v1/image/{0}/original'.format(image.id)))
            if plan.binary_image_link == 1:
                urls.append(('http://127.0.0.1:8000/api/v1/image/{0}/binary'.format(image.id)))
            image.urls = urls
            image.save()
        return image_ojects

class DetailsImage(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class OriginalView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    def get(self, request, pk):
        image =  get_object_or_404(Image, pk=pk)
        image_url = image.image.url[1:]
        content_type_image = 'image/{0}'.format(image_url.split('.')[-1])
        with open(image_url, 'rb') as f:
            return HttpResponse(f.read(), content_type=content_type_image)

class BinaryView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    def get(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        image_url = image.image.url[1:]
        file_ext = image_url.split('.')[-1]
        return FileResponse(open(image_url, 'rb'), as_attachment=True, filename='binary.{0}'.format(file_ext))

class ThumbnailView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    def get(self, request, pk, pk1):
        image = get_object_or_404(Image, pk=pk)
        image_url = image.image.url[:-8]
        content_type_image = 'image/{0}'.format(image_url.split('.')[-1])
        with open('{0}{1}.{2}}'.format(image_url[1:], pk1, content_type_image), 'rb') as f:
            return HttpResponse(f.read(), content_type=content_type_image)

class LinkView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    def get(self, request, pk, pk1, pk2):
        image = get_object_or_404(Image, image='user_{0}/{1}/{2}'.format(pk, pk1, pk2))
        image_url = image.image.url[1:]
        content_type_image = 'image/{0}'.format(image_url.split('.')[-1])
        with open(image_url, 'rb') as f:
            return HttpResponse(f.read(), content_type=content_type_image)