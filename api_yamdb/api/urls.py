from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, CustomTokenView,
                    GenreViewSet, RegistrationView, ReviewViewSet,
                    TitleViewSet, UserViewSet)

router = DefaultRouter()
router.register(
    'users',
    UserViewSet,
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    'reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    'comments'
)
router.register(
    'titles',
    TitleViewSet,
    'titles',
)
router.register(
    'genres',
    GenreViewSet,
    'genres',
)
router.register(
    'categories',
    CategoryViewSet,
    'categories',
)
urls = [
    path(
        'auth/token/',
        CustomTokenView.as_view(),
    ),
    path(
        'auth/signup/',
        RegistrationView.as_view(),
    ),
    path(
        '',
        include(router.urls),
    )
]

urlpatterns = [
    path(
        'v1/',
        include(urls)
    ),
]
