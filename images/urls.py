from django.urls import path
from .views import ListImage, DetailsImage


urlpatterns = [
    path('image', ListImage.as_view(), name='image_list'),
    path('image/<int:pk>/', DetailsImage.as_view(), name='image_details'),
]