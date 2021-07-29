from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from services.urls import urlpatterns, extra_patterns

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('profiles.urls')),
    path('services/', include(urlpatterns)),
    path('prices/', include(extra_patterns)),
    path('gallery/', include('gallery.urls')),
    path('contact/', include('contact.urls')),
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
