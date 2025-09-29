"""
URL configuration for reward_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include


def home(request):
    print(">>> HOME VIEW LOADED <<<")  # debug
    return render(request, "home.html")


urlpatterns = [
    #path("admin/", admin.site.urls),
    path('custom-admin/', include('admin_panel.urls', namespace='admin_panel')),
    path('users/', include('users.urls')),
    path("", home, name="home"),
    path("api/", include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
