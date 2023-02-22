from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import ListImage, DetailsImage, OriginalView


urlpatterns = [
    path('images', ListImage.as_view(), name='image_list'),
    path('images/<int:pk>/', DetailsImage.as_view(), name='image_details'),
    path('', OriginalView.as_view(), name='image_original'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

