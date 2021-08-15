from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrdersView.as_view(), name='orders'),
    path('<str:order_number>/', views.OrderDetailsView.as_view(), name='order_details'),
]
