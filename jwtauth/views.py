from rest_framework import generics, status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from customauth.models import User
from jwtauth.serialziers import UserSerializer


class RegisterViewSet(viewsets.ViewSetMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        refresh = tokens.RefreshToken.for_user(serializer.instance)

        return Response({**serializer.data, **{"refresh": str(refresh), "access": str(refresh.access_token)}}, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(TokenObtainPairView):
    ...


class RefreshView(TokenRefreshView):
    ...


class MyTokenVerifyView(TokenVerifyView):
    ...


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related("outstandingtoken_set")

    authentication_classes = []
    permission_classes = []
