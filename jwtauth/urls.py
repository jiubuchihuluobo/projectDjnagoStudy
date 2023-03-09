from django.urls import path

from jwtauth.views import LoginView, RefreshView, MyTokenVerifyView, RegisterViewSet

app_name = "jwt"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="logout"),
    path('verify/', MyTokenVerifyView.as_view(), name='verify'),
    path("register/", RegisterViewSet.as_view(actions={"post": "create"}), name="register")
]
