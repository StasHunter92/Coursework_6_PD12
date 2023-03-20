from django.db.models import QuerySet
from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from users.models import User
from users.serializers import UserPasswordChangeSerializer, UserSerializer, UserCreateSerializer


# ----------------------------------------------------------------------------------------------------------------------
# Custom paginator
class Paginator(PageNumberPagination):
    page_size: int = 3


# ----------------------------------------------------------------------------------------------------------------------
# User ViewSet
@extend_schema(tags=['Пользователи'])
@extend_schema_view(
    list=extend_schema(
        summary='Список всех пользователей',
        responses={
            200: OpenApiResponse(response=UserSerializer, description='OK'),
            401: OpenApiResponse(description='Unauthorized')
        }
    ),
    retrieve=extend_schema(
        summary='Конкретный пользователь через ID',
        responses={
            200: OpenApiResponse(response=UserSerializer, description='OK'),
            401: OpenApiResponse(description='Unauthorized'),
            404: OpenApiResponse(description='Not Found')
        }
    ),
    create=extend_schema(
        summary='Создать пользователя',
        responses={
            201: OpenApiResponse(response=UserCreateSerializer, description='Created'),
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(description='Unauthorized')
        }
    ),
    partial_update=extend_schema(
        summary='Обновить данные пользователя по ID',
        responses={
            200: OpenApiResponse(response=UserSerializer, description='OK'),
            401: OpenApiResponse(description='Unauthorized'),
            404: OpenApiResponse(description='Not Found')
        }
    ),
    destroy=extend_schema(
        summary='Удалить пользователя по ID',
        responses={
            204: OpenApiResponse(description='No Response'),
            401: OpenApiResponse(description='Unauthorized'),
            404: OpenApiResponse(description='Not Found')
        }
    ),
    me=extend_schema(
        summary='Личный профиль через JWT',
        responses={
            200: OpenApiResponse(response=UserSerializer, description='OK'),
            401: OpenApiResponse(description='Unauthorized')
        }
    ),
)
class MyUserViewSet(UserViewSet):
    pagination_class = Paginator
    queryset: QuerySet = User.objects.all().order_by('email')
    http_method_names: list[str] = ['get', 'post', 'patch', 'delete']

    @extend_schema(summary='Смена пароля', description='Маршрут для смены пароля',
                   request=UserPasswordChangeSerializer,
                   responses={201: OpenApiResponse(response=UserPasswordChangeSerializer, description='Created'),
                              400: OpenApiResponse(description='Bad Request'),
                              401: OpenApiResponse(description='Unauthorized')}
                   )
    @action(['post'], detail=False)
    def set_password(self, request, *args, **kwargs) -> Response:
        """
        Method for setting a new password for the user

        :param request: HTTP request object
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        :return: Response object containing the updated user data
        :raises: ValidationError if the serializer is invalid
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        super().set_password(request, *args, **kwargs)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
