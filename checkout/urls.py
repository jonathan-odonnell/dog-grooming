from django.urls import path
from . import views
from .webhooks import WebhookView

urlpatterns = [
    path('', views.CheckoutView.as_view(), name='checkout'),
    path('success/', views.CheckoutSuccessView.as_view(), name='checkout_success'),
    path('cache-checkout-data/', views.CacheCheckoutView.as_view(), name='cache_checkout_data'),
    path('wh/', WebhookView.as_view(), name='webhook')
]
