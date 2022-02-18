from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

# from .validators import validate_year

MAX_SCORE = 'Максимальная оценка'
MIN_SCORE = 'Минимальная оценка'


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


# Это модели, сделанные Хайрулло, мне нравятся, но решать тем,
# кто с ними будет работать. Оставил тут для возможности посмотреть.
# ================================================================
# class Category(models.Model):
#     """Модель категорий."""
#     name = models.CharField(
#         verbose_name='Категория',
#         max_length=128,
#         unique=True
#     )
#     slug = models.SlugField(
#         unique=True
#     )

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = 'Категория'
#         verbose_name_plural = 'Категории'
#         ordering = ('name',)


# class Genre(models.Model):
#     """Модель жанров."""
#     name = models.CharField(
#         verbose_name='Жанр',
#         max_length=128,
#         unique=True
#     )
#     slug = models.SlugField(
#         unique=True
#     )

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = 'Жанр'
#         verbose_name_plural = 'Жанры'
#         ordering = ('name',)


# class Title(models.Model):
#     """Модель произведений."""
#     name = models.CharField(
#         verbose_name='Наименование',
#         max_length=128
#     )
#     genre = models.ManyToManyField(
#         Genre,
#         verbose_name='Жанр',
#         related_name='titles',
#         blank=True,
#         through='GenreTitle',
#     )
#     category = models.ForeignKey(
#         Category,
#         verbose_name='Категория',
#         on_delete=models.SET_NULL,
#         related_name='titles',
#         blank=True,
#         null=True
#     )
#     year = models.PositiveSmallIntegerField(
#         null=True,
#         blank=True,
#         db_index=True,
#         validators=(validate_year,),
#         verbose_name='Дата выхода'
#     )
#     description = models.CharField(
#         verbose_name='Описание',
#         max_length=256,
#         blank=True,
#     )

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = 'Произведение'
#         verbose_name_plural = 'Произведения'
#         ordering = ('id',)


# class GenreTitle(models.Model):
#     """Модель для связи произведений и жанров отношением многие ко многим."""
#     title = models.ForeignKey(Title, on_delete=models.CASCADE)
#     genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
# ================================================================

class Review(models.Model):
    """Модель Произведение"""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'Оценка',
        default=5,
        validators=(
            MaxValueValidator(10, message=MAX_SCORE),
            MinValueValidator(1, message=MIN_SCORE)
        )
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='one_review'
            ),
        )


class Comment(models.Model):
    """Модель Отзыва"""
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
