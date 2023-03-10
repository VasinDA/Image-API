from django.urls import path
from .views import ListImage, DetailsImage, OriginalView, BinaryView, ThumbnailView 


urlpatterns = [
    path('image', ListImage.as_view(), name='image_list'),
    path('image/<int:pk>/', DetailsImage.as_view(), name='image_details'),
    path('image/<int:pk>/original', OriginalView.as_view(), name='image_original'),
    path('image/<int:pk>/binary', BinaryView.as_view(), name='image_binary'),
    path('image/<int:pk>/thumbnail/<int:pk1>', ThumbnailView.as_view(), name='thumbnail_link')
    ]