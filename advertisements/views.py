from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import TitleFilter
from advertisements.models import Advertisement, Comment
from advertisements.permissions import IsOwnerOrAdmin
from advertisements.serializers import AdvertisementListSerializer, AdvertisementDetailSerializer, \
    AdvertisementCreateSerializer, CommentSerializer, CommentCreateSerializer


# ----------------------------------------------------------------------------------------------------------------------
# Custom paginator
class AdvertisementPaginator(PageNumberPagination):
    """
    Custom paginator to override default page size
    """
    page_size: int = 4


class CommentPaginator(PageNumberPagination):
    """
    Custom paginator to override default page size
    """
    page_size: int = 100


# ----------------------------------------------------------------------------------------------------------------------
# Advertisement ViewSet
@extend_schema(tags=['Объявления'])
@extend_schema_view(
    list=extend_schema(summary='Список всех объявлений'),
    retrieve=extend_schema(summary='Конкретное объявление'),
    create=extend_schema(summary='Создать объявление'),
    partial_update=extend_schema(summary='Отредактировать объявление'),
    destroy=extend_schema(summary='Удалить объявление')
)
class AdvertisementsViewSet(ModelViewSet):
    """
    A ViewSet that provides CRUD operations for the Advertisement model
    """
    queryset: QuerySet = Advertisement.objects.all().order_by('-created_at')
    default_serializer = AdvertisementListSerializer
    default_permission: list[type] = [AllowAny]
    pagination_class = AdvertisementPaginator
    filter_backends: tuple[type] = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names: list[str] = ['get', 'post', 'patch', 'delete']

    serializers: dict[str, type] = {
        'retrieve': AdvertisementDetailSerializer,
        'create': AdvertisementCreateSerializer,
        'update': AdvertisementCreateSerializer,
        'partial_update': AdvertisementCreateSerializer,
    }

    permissions: dict[str, list[type]] = {
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsOwnerOrAdmin],
        'partial_update': [IsAuthenticated, IsOwnerOrAdmin],
        'destroy': [IsAuthenticated, IsOwnerOrAdmin],
    }

    def get_permissions(self) -> list[type]:
        """
        Returns the permission classes for the current action
        """
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self) -> type:
        """
        Method to define serializer class
        """
        return self.serializers.get(self.action, self.default_serializer)


@extend_schema(summary='Список объявлений пользователя', tags=['Объявления'])
class AdvertisementUserListView(ListAPIView):
    """
    GET list of advertisements created by current user
    """
    queryset = Advertisement.objects.all().order_by('-created_at')
    serializer_class = AdvertisementListSerializer
    permission_classes: list[type] = [IsAuthenticated]
    pagination_class = AdvertisementPaginator

    def get_queryset(self) -> list[Advertisement]:
        """
        Method to get queryset of advertisements created by current user
        """
        return self.queryset.filter(author=self.request.user)


# ----------------------------------------------------------------------------------------------------------------------
# Comment ViewSet
@extend_schema(tags=['Комментарии'])
@extend_schema_view(
    list=extend_schema(summary='Список всех комментариев'),
    retrieve=extend_schema(summary='Конкретный комментарий'),
    create=extend_schema(summary='Создать комментарий'),
    partial_update=extend_schema(summary='Отредактировать комментарий'),
    destroy=extend_schema(summary='Удалить комментарий')
)
class CommentViewSet(ModelViewSet):
    """
    A ViewSet that provides CRUD operations for the Comment model
    """
    queryset: QuerySet = Comment.objects.all().order_by('-created_at')
    default_serializer = CommentSerializer
    default_permission: list[type] = [IsAuthenticated]
    pagination_class = CommentPaginator
    http_method_names: list[str] = ['get', 'post', 'patch', 'delete']

    serializers: dict[str, type] = {
        'create': CommentCreateSerializer,
        'update': CommentCreateSerializer,
        'partial_update': CommentCreateSerializer,
    }

    permissions: dict[str, type] = {
        'retrieve': [IsAuthenticated, IsOwnerOrAdmin],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsOwnerOrAdmin],
        'partial_update': [IsAuthenticated, IsOwnerOrAdmin],
        'destroy': [IsAuthenticated, IsOwnerOrAdmin],
    }

    def get_permissions(self) -> list[type]:
        """
        Returns the permission classes for the current action
        """
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self) -> type:
        """
        Return serializer class based on action.
        """
        return self.serializers.get(self.action, self.default_serializer)

    def get_queryset(self) -> QuerySet:
        """
        Return queryset for list action.
        """
        return self.queryset.filter(ad_id=self.kwargs['ad_id'])

    def get_object(self) -> Comment:
        """
        Return single object based on primary key.
        """
        queryset: QuerySet = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj
