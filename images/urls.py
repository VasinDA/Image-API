from django.urls import path
from .views import ListImage, DetailsImage, OriginalView, BinaryView, LinkView, ThumbnailView 


urlpatterns = [
    path('image', ListImage.as_view(), name='image_list'),
    path('image/<int:pk>/', DetailsImage.as_view(), name='image_details'),
    path('image/<int:pk>/original', OriginalView.as_view(), name='image_original'),
    path('image/<int:pk>/binary', BinaryView.as_view(), name='image_binary'),
    path('media/user_<pk>/<pk1>/<pk2>', LinkView.as_view(), name='image_link'),
    path('image/<int:pk>/thumbnail/<pk1>', ThumbnailView.as_view, ame='thumbnail_link')
    
    ]