from rest_framework import generics
from .models import Images
import os
from rest_framework.reverse import reverse
from PIL import Image
from plans.models import Plan
from django.utils import timezone
from django.shortcuts import  get_object_or_404
from django.http import HttpResponse, FileResponse
from rest_framework.permissions import IsAuthenticated
from .serializers import ImageSerializer, DeteilImageSerializer

class ListImage(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        image_ojects = Images.objects.filter(user=user)
        plan = Plan.objects.get(id=user.plan_id)
        available_hights = plan.available_hights.split(',')
        for image in image_ojects:
            urls = []
            url  = reverse('thumbnail_link',kwargs={'pk':image.id, 'pk1':200}, request=self.request)
            print(url)
            for hight in available_hights:
                urls.append(reverse('thumbnail_link',kwargs={'pk':image.id, 'pk1':hight}, request=self.request))
            if plan.original_image_link == True:
                urls.append(reverse('image_original',kwargs={'pk':image.id}, request=self.request))
            if plan.binary_image_link == True:
                urls.append(reverse('image_binary',kwargs={'pk':image.id}, request=self.request))
            image.urls = urls
            image.save()
        return image_ojects

class DetailsImage(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeteilImageSerializer
    def get_object(self):
        pk = self.kwargs.get('pk')
        user = self.request.user
        image = get_object_or_404(Images, pk=pk)
        plan = Plan.objects.get(id=user.plan_id)
        available_hights = plan.available_hights.split(',')
        urls = []
        for hight in available_hights:
            urls.append(reverse('thumbnail_link',kwargs={'pk':image.id, 'pk1':hight}, request=self.request))
        if plan.original_image_link == True:
            urls.append(reverse('image_original',kwargs={'pk':image.id}, request=self.request))
        if plan.binary_image_link == True:
            urls.append(reverse('image_binary',kwargs={'pk':image.id}, request=self.request))
        image.urls = urls
        image.save()
        return image

class OriginalView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    def get(self, request, pk):
        image =  get_object_or_404(Images, pk=pk)
        image_url = image.image.url[1:]
        content_type_image = 'image/{0}'.format(image_url.split('.')[-1])
        with open(image_url, 'rb') as f:
            return HttpResponse(f.read(), content_type=content_type_image)

class BinaryView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    def get(self, request, pk):
        image = get_object_or_404(Images, pk=pk)
        image_url = image.image.url[1:]
        file_ext = image_url.split('.')[-1]
        link_expiration_time = image.created_time + timezone.timedelta(seconds=image.expires_after)
        if timezone.now() < link_expiration_time:
            return FileResponse(open(image_url, 'rb'), as_attachment=True, filename='binary.{0}'.format(file_ext))
        return HttpResponse(status=410)

class ThumbnailView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    def get(self, request, pk, pk1):
        image = get_object_or_404(Images, pk=pk)
        image_url = image.image.url[:-8]
        file_ext = image.image.url[1:].split('.')[-1]
        content_type_image = 'image/{0}'.format(file_ext)
        full_image_path = '{0}{1}.{2}'.format(image_url[1:], pk1, file_ext)
        if os.path.exists(full_image_path):
            with open(full_image_path, 'rb') as f:
                return HttpResponse(f.read(), content_type=content_type_image)
        try:
            original_image = Image.open('{0}full.{1}'.format(image_url[1:], file_ext))
            height_size = int(pk1)
            height_percent = (height_size / float(original_image.size[0]))
            width_size = int((float(original_image.size[0]) * float(height_percent)))
            thumbnail_image = original_image
            thumbnail_image.thumbnail((height_size, width_size))
            thumbnail_image.save('{0}{1}.{2}'.format(image_url[1:], pk1, file_ext))
            with open(full_image_path, 'rb') as f:
                return HttpResponse(f.read(), content_type=content_type_image)
        except IOError:
            return HttpResponse(status=404)