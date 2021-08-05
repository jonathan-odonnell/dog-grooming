from django.urls import path
from . import views

urlpatterns = [
    path('', views.BagView.as_view(), name='bag'),
    path('add/service/<item_id>/',
         views.AddServiceToBagView.as_view(), name='add_service_to_bag'),
    path('remove/service/<item_id>/', views.RemoveServiceFromBagView.as_view(),
         name='remove_service_from_bag'),
]
