import datetime as dt

from django.contrib.auth import authenticate
from django.core.validators import MaxValueValidator
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from core.models import User
from reviews.models import Category, Comment, Genre, Review, Title
from .utils import send_email
from .validators import MyUsernameValidator


class CustomTokenSerializer(TokenObtainSerializer):
    """Сериализатор для получения токенов."""

    confirmation_code = serializers.CharField(
        max_length=150,
        required=True,
    )
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['confirmation_code'],
        }
        if not User.objects.filter(
                username=attrs[self.username_field]
        ).exists():
            raise exceptions.NotFound(
                f'Пользователь {attrs[self.username_field]} не найден.'
            )
        user = authenticate(**authenticate_kwargs)
        if not api_settings.USER_AUTHENTICATION_RULE(user):
            raise exceptions.ParseError
        data = {
            'access': str(self.get_token(user))
        }
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    def create(self, validated_data):
        user = User.objects.create(
            **validated_data
        )
        send_email(user)
        return validated_data

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )
        validators = (MyUsernameValidator(),)


class AdminRegistrationSerializer(RegistrationSerializer):
    """
    Сериализатор для отправки письма пользователю,
    созданному администратором.
    """

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        user = User.objects.get(**validated_data)
        send_email(user)
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        validators = (MyUsernameValidator(),)


class PatchUserSerializer(UserSerializer):
    """Сериализатор для PATCH /me ."""

    username = serializers.CharField(
        read_only=True,
        required=False,
    )
    email = serializers.EmailField(
        read_only=True,
        required=False,
    )

    def validate_role(self, value):
        user = self.context.get('request').user
        if not user.is_admin:
            value = user.role
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('__all__',)


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
    )
    year = serializers.IntegerField(
        validators=[MaxValueValidator(dt.date.today().year)]
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'description',
            'category',
            'genre',
            'year',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'text',
            'score',
            'pub_date',
        )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        user = self.context['request'].user
        if user.reviews.filter(title_id=title_id).exists():
            raise serializers.ValidationError(
                'Нельзя оставить отзыв на одно и тоже произведение дважды'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
