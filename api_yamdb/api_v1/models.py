from django.contrib.auth.models import AbstractUser
from django.db import models


# Это только скелет базы. Требует уточнений и правок.
# Сделан для обкатки скипта импорта данных, но можно пользовать
# и дальше.
class User(AbstractUser):
    USER_ROLES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    ]

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=255,
        choices=USER_ROLES,
    )


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=255)
    year = models.DateField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='title',
    )


class GenreTitle(models.Model):
    """Модель связи произведения с жанром."""
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genre',
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='title',
    )


class Review(models.Model):
    """Модель рецензии."""
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField()


class Comment(models.Model):
    """Модель коментария к рецензии."""
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    pub_date = models.DateTimeField()
