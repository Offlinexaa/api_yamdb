from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if value < 0:
        raise ValidationError('Год не может быть меньше нуля')
    if value > datetime.today().year:
        raise ValidationError('Год не может быть больше текущего года')
