from django.contrib import admin
from reviews.models import Genre, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Страница Title в админке"""

    list_display = (
        'pk',
        'name',
        'year',
        'category',
    )

    list_filter = ('category', 'genre', 'name', 'year',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Страница Genre в админке"""

    list_display = (
        'pk',
        'name',
        'slug',
    )

    list_filter = ('name', 'slug',)
    empty_value_display = '-пусто-'
