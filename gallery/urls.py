from django.urls import path
from . import views

urlpatterns = [
    path('', views.GalleryView.as_view(), name='gallery'),
    path('', views.DeleteImageView.as_view(), name='delete-image'),
]
