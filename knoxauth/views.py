from knox.views import LoginView
from rest_framework.authentication import BasicAuthentication


class KnoxLoginView(LoginView):
    authentication_classes = (BasicAuthentication,)
