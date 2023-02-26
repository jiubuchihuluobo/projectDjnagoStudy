from django.urls import path

from demo.views import HomeView, CreateView

app_name = "demo"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("create/", CreateView.as_view(), name="create"),
]
