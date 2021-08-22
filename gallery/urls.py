from django.urls import path
from . import views

urlpatterns = [
    path('', views.GalleryView.as_view(), name='gallery'),
    path('delete/<int:pk>/', views.DeleteImageView.as_view(), name='delete_image'),
]
