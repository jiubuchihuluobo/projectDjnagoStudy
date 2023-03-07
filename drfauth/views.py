from django.contrib.auth import login, authenticate
from django.views import View
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import Request

from drfauth.serializers import UserSerializer


class RegisterView(APIView):
    # throttle_classes = ()
    # permission_classes = ()
    # parser_classes = ()
    # renderer_classes = ()
    serializer_class = UserSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class LoginTestView(View):
    serializer_class = UserSerializer

    def post(self, request: Request):
        username = request.data["username"]
        password = request.data["password"]
        user = request.user
        user = authenticate(request=request, username=username, password=password)
        if user:
            # serializer = self.get_serializer(instance=user)
            serializer = UserSerializer(instance=user)
            token, created = Token.objects.get_or_create(user=user)
            response_data = serializer.data
            response_data.update({"token": token.key})
            login(request, user)
            return Response(response_data)
        else:
            return Response({"status": "failure", "detail": "密码错误请重新输入"})
