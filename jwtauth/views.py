from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class LoginView(TokenObtainPairView):
    ...


class RefreshView(TokenRefreshView):
    ...
