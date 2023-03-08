from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


class LoginView(TokenObtainPairView):
    ...


class RefreshView(TokenRefreshView):
    ...


class MyTokenVerifyView(TokenVerifyView):
    ...
