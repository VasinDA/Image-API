from django.urls import path
from .views import ListImage, DetailsImage, OriginalView


urlpatterns = [
    path('image', ListImage.as_view(), name='image_list'),
    path('image/<int:pk>/', DetailsImage.as_view(), name='image_details'),
    path('image/<int:pk>/original', OriginalView.as_view(), name='image_original'),
    
]