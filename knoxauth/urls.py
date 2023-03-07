from django.urls import path

from knoxauth.views import KnoxLoginView

app_name = "knox"

urlpatterns = [
    path("login/", KnoxLoginView.as_view())
]
