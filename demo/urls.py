from django.urls import path

from demo.views import HomeView

app_name = "demo"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home")
]
