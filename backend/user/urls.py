# Django imports
from django.urls import path

# View imports
from .views import *

app_name = "user_end_points"

urlpatterns = [
    path("login/",LoginUserView.as_view(),name="LoginUser"),
    path("logout/",LogoutUserView.as_view(),name="LogoutUser"),
    path("register/",RegisterUserView.as_view(),name="RegisterUser"),
    path("me/",GetUserDetailsView.as_view(),name="UserDetails"),
    path("delete/",DeleteUserView.as_view(),name="DeleteUser"),
]
