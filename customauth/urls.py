from django.urls import path

from customauth.views import UserLoginView

app_name = "customauth"
urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login")
]
