from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *
from django.urls import path


app_name = "rest_api_v1"

urlpatterns = [
    path("testing",Tester.as_view(),name="testing"),

    # JWT token URLs.
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
