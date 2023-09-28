from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include("rest_api_v1.urls",namespace="rest_api_v1"))
]
