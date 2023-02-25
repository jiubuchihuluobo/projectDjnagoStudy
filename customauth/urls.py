from django.urls import path

from customauth.views import HomeView

app_name = "customauth"

urlpatterns = [
    path("index/", HomeView.as_view(), name="home")
]
