from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import validate_year
from core.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        verbose_name='Название',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        blank=True,
        null=True,
        help_text='Выберите категорию',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Выберите жанр',
    )
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='Год',
        blank=True,
        null=True,
        db_index=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Максимальная оценка - 10'),
        ]
    )

    class Meta:
        ordering = ('pub_date',)
        unique_together = ('title', 'author',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
