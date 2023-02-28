from django.urls import path

from customauth.views import HomeView, LogOutView, RegisterView

app_name = "customauth"

urlpatterns = [
    path("login/", HomeView.as_view(), name="login"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
