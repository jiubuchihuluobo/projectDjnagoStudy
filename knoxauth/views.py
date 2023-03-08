from knox.views import LoginView, LogoutView, LogoutAllView
from rest_framework.authentication import BasicAuthentication


class KnoxLoginView(LoginView):
    authentication_classes = (BasicAuthentication,)


class KnoxLogoutView(LogoutView):
    ...


class KnoxLogoutALLView(LogoutAllView):
    ...
