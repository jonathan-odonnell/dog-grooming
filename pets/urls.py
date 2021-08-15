from django.urls import path
from . import views

urlpatterns = [
    path('', views.PetsView.as_view(), name='pets'),
    path('add/', views.AddPetView.as_view(), name='add_pet'),
    path('edit/<int:pk>/', views.EditPetView.as_view(), name='edit_pet'),
    path('delete/<int:pk>/', views.DeletePetView.as_view(), name='delete_pet'),
]
