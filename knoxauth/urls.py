from django.urls import path

from knoxauth.views import KnoxLoginView, KnoxLogoutView

app_name = "knox"

urlpatterns = [
    path("login/", KnoxLoginView.as_view(), name="login"),
    path("logout/", KnoxLogoutView.as_view(), name="logout"),
]
