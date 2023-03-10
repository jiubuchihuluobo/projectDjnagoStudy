from django.urls import path
from rest_framework import routers

from jwtauth.views import LoginView, RefreshView, MyTokenVerifyView, RegisterViewSet, UserViewSet

app_name = "jwtauth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="logout"),
    path('verify/', MyTokenVerifyView.as_view(), name='verify'),
    path("register/", RegisterViewSet.as_view(actions={"post": "create"}), name="register")
]

router = routers.DefaultRouter()
router.register(viewset=UserViewSet, prefix="user_info")

urlpatterns += router.urls
