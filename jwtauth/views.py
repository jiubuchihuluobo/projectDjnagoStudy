from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status, filters
from rest_framework import mixins
from rest_framework import response
from rest_framework import viewsets
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from customauth.models import User
from jwtauth.serialziers import GeneralUserSerializer
from utils.pagination import MyPageNumberPagination


class RegisterViewSet(viewsets.ViewSetMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = GeneralUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        refresh = tokens.RefreshToken.for_user(serializer.instance)

        return response.Response(
            data={**serializer.data, **{"refresh": str(refresh), "access": str(refresh.access_token)}},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class LoginView(TokenObtainPairView):
    ...


class RefreshView(TokenRefreshView):
    ...


class MyTokenVerifyView(TokenVerifyView):
    ...


@method_decorator(decorator=cache_page(60), name="list")
@method_decorator(decorator=cache_page(60), name="retrieve")
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = GeneralUserSerializer
    queryset = User.objects.prefetch_related("outstandingtoken_set")

    # 覆盖默认限流策略
    throttle_classes = []

    # 范围限流必须声明throttle_scope
    # throttle_scope = 'contacts'

    authentication_classes = []
    permission_classes = []

    # permission_classes = [
    #     # permissions.IsAuthenticated | permissions.DjangoModelPermissions
    #     # permissions.IsAuthenticated,
    #     # DjangoObjectPermissions,
    #     # IsOwnerOrReadOnly,
    # ]
    # filterset_fields = ['id', 'username']

    # Search Filter
    # '^'从搜索开始。
    # '=' 精确匹配。
    # '@'全文搜索。（目前仅支持Django的PostgreSQL后端。）
    # '$'正则表达式搜索。
    filter_backends = [filters.SearchFilter]
    search_fields = ['=username']

    def get_object(self):
        obj = super().get_object()
        return obj


class UserTestViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = GeneralUserSerializer

    # Search Filter
    # '^'从搜索开始。
    # '=' 精确匹配。
    # '@'全文搜索。（目前仅支持Django的PostgreSQL后端）
    # '$'正则表达式搜索。
    filter_backends = [filters.SearchFilter]
    search_fields = ['@username']

    pagination_class = MyPageNumberPagination

    def list(self, request, *args, **kwargs):
        # 获取原始查询集
        queryset = self.filter_queryset(self.get_queryset())

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # 序列化数据
        serializer = self.get_serializer(queryset, many=True)

        return response.Response(serializer.data)
