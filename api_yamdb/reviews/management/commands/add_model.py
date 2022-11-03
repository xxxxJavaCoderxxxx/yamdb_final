import csv
import os

from django.core.management.base import BaseCommand

from core.models import User
from reviews.models import Category, Comment, Genre, Review, Title
from api_yamdb.settings import BASE_DIR


class Command(BaseCommand):
    help = ('Загрузить данные из файла.'
            'Пример - manage.py add_model users.csv')
    files = {
        'users.csv': User,
        'category.csv': Category,
        'comments.csv': Comment,
        'titles.csv': Title,
        'review.csv': Review,
        'genre.csv': Genre,
    }
    fields = {
        'title_id': 'title',
        'review_id': 'review',
    }

    def _prepare_fields(self, row: dict) -> None:
        fields = {
            'title': Title.objects.get(
                id=row.get('title_id')
            ) if row.get('title_id') else None,
            'author': User.objects.get(
                id=row.get('author')
            ) if row.get('author') else None,
            'category': Category.objects.get(
                id=row.get('category')
            ) if row.get('category') else None,
            'review': Review.objects.get(
                id=row.get('review')
            ) if row.get('review') else None,
        }
        for key, value in self.fields.items():
            if key in row:
                row.pop(key)
                row[value] = None
        for key, value in fields.items():
            if key in row:
                row[key] = value

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        filename = options.get('filename')
        if filename not in self.files:
            print(
                f'Filename {filename} not in {list(self.files.keys())}'
            )
            return
        obj = self.files.get(filename)
        csv_file = os.path.join(
            BASE_DIR,
            f'static/data/{filename}',
        )
        if not os.path.isfile(csv_file):
            print('file not found!')
            return

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self._prepare_fields(row)
                obj.objects.update_or_create(**row)
