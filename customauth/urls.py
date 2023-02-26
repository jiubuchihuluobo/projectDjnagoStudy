from django.urls import path

from customauth.views import HomeView

app_name = "customauth"

urlpatterns = [
    path("login/", HomeView.as_view(), name="login"),
    path("logout/", HomeView.as_view(), name="logout"),
]
