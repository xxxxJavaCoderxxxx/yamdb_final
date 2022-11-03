from django.core.management.base import BaseCommand

from core.models import User
from reviews.models import Category, Comment, Genre, Review, Title


class Command(BaseCommand):

    help = ('Удалить данные из БД для модели.'
            'Пример - manage.py delete_model User')
    files = {
        'User': User,
        'Category': Category,
        'Comment': Comment,
        'Title': Title,
        'Review': Review,
        'Genre': Genre,
    }

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)

    def handle(self, *args, **options):
        model = options.get('model')
        if model not in self.files:
            print(f'Model "{model}" not in {self.files.keys()}')
            return
        Obj = self.files.get(model)
        Obj.objects.all().delete()
