from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_year


MAX_SCORE = 'Максимальная оценка'
MIN_SCORE = 'Минимальная оценка'
USER_ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
)


class User(AbstractUser):
    """
    Модель пользователя.
    Добавлены поля 'Биография', 'Роль' и 'Код подтверждения'.
    """
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=255,
        choices=USER_ROLES,
        default='user'
    )
    confirmation_code = models.TextField(
        'Код подтверждения',
        null=True,
        blank=True,
    )

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Genre(models.Model):
    """Модель жанров."""
    name = models.TextField(verbose_name='Название жанра')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категорий."""
    name = models.TextField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=255,
                            verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год выпуска',
                               validators=[validate_year])
    description = models.TextField(max_length=255, verbose_name='Описание',
                                   blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='title',
    )
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   verbose_name='Жанр',
                                   related_name='titles')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель связи произведения с жанром."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    """Модель отзывов."""
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField('оценка', validators=[
                                MinValueValidator(1, 'Минимальная оценка-1'),
                                MaxValueValidator(10, 'Максимальная оценка-10')
                                ])
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_riview')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев."""
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        'Дата комментария', auto_now_add=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
