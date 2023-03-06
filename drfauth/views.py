from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import Request

from drfauth.serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class LoginTestView(GenericAPIView):
    def post(self, request: Request):
        user = authenticate(request, username=request.data.get("username"), password=request.data.get("password"))
        from rest_framework.authtoken.models import Token
        token = Token.objects.create(user=user)
        TokenAuthentication
        print(token.key)
        if user:
            login(request, user)
            serializer = UserSerializer(instance=user)
            return Response(data=serializer.data)
        else:
            return Response(data={"detail": "Password input error"})
