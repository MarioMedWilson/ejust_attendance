"""
URL configuration for ejust_attendance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path


# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

# urls.py
from django.urls import path, include
from members.views import upload_image, test_server, custom_404_view
from django.conf.urls import handler404

from django.http import JsonResponse



handler404 = custom_404_view
urlpatterns = [
    path('upload', upload_image, name='upload_image'),
    path('test/', test_server, name='test_server'),
]
