from django.urls import path

from drfauth.views import RegisterView, LoginTestView

app_name = "drfauth"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginTestView.as_view(), name="login"),
]
