from django.urls import path

from demo.views import HomeView, CreateView, EditView, DeleteView

app_name = "demo"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("create/", CreateView.as_view(), name="create"),
    path("edit/<int:pk>", EditView.as_view(), name="edit"),
    path("delete/<int:pk>", DeleteView.as_view(), name="delete")
]
