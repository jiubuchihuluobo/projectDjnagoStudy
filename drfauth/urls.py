from django.urls import path

from drfauth.views import RegisterView, LoginView

app_name = "drfauth"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
