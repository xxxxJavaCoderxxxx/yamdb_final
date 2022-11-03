from datetime import datetime as dt

from django.core.exceptions import ValidationError
from rest_framework import exceptions


class MyUsernameValidator(object):

    def __call__(self, value):
        username = value.get('username')
        if username == 'me':
            raise exceptions.ValidationError(
                {
                    'username':
                        ['Нельзя создать пользователя с username = me.', ]
                }
            )
        return value


def validate_year(value):
    current_year = dt.now().year
    if value > current_year:
        raise ValidationError(
            f'Год произведения не может быть больше, чем {current_year}!'
            f'Проверьте указанный год!'
        )
    return True
