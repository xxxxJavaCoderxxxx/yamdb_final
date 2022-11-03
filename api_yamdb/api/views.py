from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase

from core.models import User
from .filters import TitleFilter
from .permissions import IsAdmin, IsModerator, OwnerOnly, ReadOnly
from reviews.models import Category, Genre, Review, Title
from .serializers import (AdminRegistrationSerializer, CategorySerializer,
                          CommentSerializer, CustomTokenSerializer,
                          GenreSerializer, PatchUserSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitleGetSerializer, TitlePostSerializer,
                          UserSerializer)


class CustomTokenView(TokenViewBase):
    """View для полчения токена."""

    serializer_class = CustomTokenSerializer


class RegistrationView(CreateAPIView):
    """View для регистрации пользователей."""

    def get_serializer_class(self):
        user = {
            'username': self.request.data.get('username'),
            'email': self.request.data.get('email'),
        }
        user = User.objects.filter(**user)
        if user.exists() and not user.first().confirmation_code:
            return AdminRegistrationSerializer
        return RegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = HTTP_200_OK
        return response


class UserViewSet(ModelViewSet):
    """View для обработки пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        serializer_class=PatchUserSerializer,
    )
    def me(self, request):
        serializer = self.get_serializer(
            instance=request.user,
            data=request.data,
            many=False,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CreateListDestroyViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet
):

    permission_classes = [IsAdmin | ReadOnly]
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    ordering_fields = (
        'year',
        'name',
    )
    permission_classes = [IsAdmin | ReadOnly]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = [
        IsModerator
        | OwnerOnly
        | ReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get("title_id"),
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(
            Title,
            id=title_id,
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [
        IsModerator
        | OwnerOnly
        | ReadOnly
    ]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id"),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            id=review_id,
            title__id=title_id,
        )
        serializer.save(author=self.request.user, review=review)
