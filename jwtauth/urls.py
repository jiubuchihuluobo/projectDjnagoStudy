from django.urls import path

from jwtauth.views import LoginView, RefreshView

app_name = "jwt"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="logout"),
]
