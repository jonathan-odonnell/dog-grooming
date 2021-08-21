from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(),
         name='terms_of_service'),
]
