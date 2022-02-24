from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Валидатор корректности года создания произведения."""
    if value < 0:
        raise ValidationError('Год не может быть меньше нуля.')
    if value > timezone.now().year:
        raise ValidationError(
            ('Год %(value)s больше текущего!'),
            params={'value': value},
        )
