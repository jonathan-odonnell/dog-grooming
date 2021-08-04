from django.urls import path
from . import views

urlpatterns = [
    path('', views.ServicesView.as_view(), name='services'),
    path('<int:pk>/appointments/', views.AppointmentsView.as_view(), name='service_appointments'),
    path('<int:pk>/appointments/<int:month>/<int:year>/', views.AppointmentsView.as_view(), name='service_appointments_by_month'),
    path('add/', views.AddServiceView.as_view(), name='add_service'),
    path('edit/<int:pk>/', views.EditServiceView.as_view(), name='edit_service'),
    path('delete/<int:pk>/', views.DeleteServiceView.as_view(),
         name='delete_service'),
]
