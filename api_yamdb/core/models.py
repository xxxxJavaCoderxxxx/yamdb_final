from django.contrib.auth.models import AbstractUser, AnonymousUser, UserManager
from django.db import models

from core.constants import ADMIN, MODERATOR, ROLES, USER


class CustomUserManager(UserManager):
    """Класс для управления объектами User."""

    def create_superuser(self, username, email, password, **extra_fields):
        for key in ('is_staff', 'is_superuser', 'confirmation_code'):
            if not extra_fields.setdefault(key, True):
                raise ValueError(f'Superuser must have {key} = True.')
        extra_fields['role'] = ADMIN
        return self._create_user(username, email, password, **extra_fields)


class CustomAnonymousUser(AnonymousUser):
    """Анонимный пользователь."""

    @property
    def is_admin(self):
        return False

    @property
    def is_moderator(self):
        return False


class User(AbstractUser):
    """Модель для пользователей."""

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        db_index=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLES,
        default=USER,
        max_length=9,
    )
    confirmation_code = models.BooleanField(
        verbose_name='Отправлено ли письмо',
        default=False,
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR or self.is_admin
