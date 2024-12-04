"""
URL configuration for ITArch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin page
    path('', include('Website.urls')),  # Routes all application-specific URLs to the 'Website' app
    path('accounts/', include('django.contrib.auth.urls')),  # Django's built-in authentication URLs (login, logout, etc.)
]

# Serve static files during development (CSS, JavaScript, images, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Serve media files (uploaded files, such as product images) during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
