from django.urls import path
from . import views

urlpatterns = [
    path('', views.BagView.as_view(), name='bag'),
]
