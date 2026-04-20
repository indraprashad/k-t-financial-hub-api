from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/', include('about.urls')),
    path('api/', include('admin_profiles.urls')),
    path('api/', include('blog.urls')),
    path('api/', include('blog_categories.urls')),
    path('api/', include('bookings.urls')),
    path('api/', include('business.urls')),
    path('api/', include('contact.urls')),
    path('api/', include('home.urls')),
    path('api/', include('roles.urls')),
    path('api/', include('services.urls')),
    path('api/', include('service_categories.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
