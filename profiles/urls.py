from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('orders/<str:order_number>', views.OrderDetailsView.as_view(), name='order_details'),
]
