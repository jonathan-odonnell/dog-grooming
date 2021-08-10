from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('newsletter-email/', views.NewsletterEmailView.as_view(),
         name='newsletter_email'),
]
