from django.urls import path

from todoapp.views import HomeView

app_name = "todoapp"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home")
]
