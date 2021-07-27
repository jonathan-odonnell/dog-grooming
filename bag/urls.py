from django.urls import path
from . import views

urlpatterns = [
    path('', views.BagView.as_view(), name='bag'),
    path('add/service/<int:item_id>/', views.AddServiceView.as_view(), name='add_service_to_bag'),
    path('remove/service/<item_id>/', views.RemoveServiceView.as_view(), name='remove_service_from_bag'),
]
