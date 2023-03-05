from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView


class RegisterView(APIView):
    def post(self):
        ...


class LoginView(GenericAPIView):
    def post(self):
        ...
