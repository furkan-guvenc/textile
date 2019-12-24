"""textile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from mockup import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_page, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('index/', views.index, name='index'),
    path('upload_pattern/', views.upload_pattern, name='upload_pattern'),
    path('load_images', views.load_images, name='load_images'),  # ajax
    path('delete_image', views.delete_image, name='delete_image'),  # ajax
    path('show_layers/<str:image_name>/', views.show_layers, name='show_layers'),
    path('upload_image', views.upload_image_page, name='upload_image'),
    path('dominant_color', views.dominant_color_page, name='dominant_color'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
