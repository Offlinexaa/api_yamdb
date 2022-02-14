import csv
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand

# Заменить api_v1 на имя приложения
from api_v1.models import (Genre, Category, Title, GenreTitle, Review,
                           Comment, User)


def _get_file_reader(filename):
    """Возвращает ридер из выбранного *.csv файла."""
    filepath = Path.joinpath(Path.cwd(), 'static', 'data', filename)
    if filepath.is_file():
        with open(filepath, encoding='utf-8') as f:
            reader = list(csv.reader(f))
    return reader


def _load_category():
    """Загрузка в модель категорий."""
    reader = _get_file_reader('category.csv')
    for line in reader[1:]:
        _, created = Category.objects.get_or_create(
            pk=int(line[0]),
            name=line[1],
            slug=line[2]
        )


def _load_genre():
    """Загрузка в модель жанров."""
    reader = _get_file_reader('genre.csv')
    for line in reader[1:]:
        _, created = Genre.objects.get_or_create(
            pk=int(line[0]),
            name=line[1],
            slug=line[2]
        )


def _load_genre_title():
    """Загрузка в модель отношения произведение-жанр."""
    reader = _get_file_reader('genre_title.csv')
    for line in reader[1:]:
        _, created = GenreTitle.objects.get_or_create(
            pk=int(line[0]),
            title_id=Title.objects.get(pk=int(line[1])),
            genre_id=Genre.objects.get(pk=int(line[2]))
        )


def _load_titles():
    """Загрузка в модель произведений."""
    reader = _get_file_reader('titles.csv')
    for line in reader[1:]:
        _, created = Title.objects.get_or_create(
            pk=int(line[0]),
            name=line[1],
            year=datetime.strptime(line[2], "%Y").date(),
            category=Category.objects.get(pk=int(line[3]))
        )


def _load_reviews():
    """Загрузка в модель рецензий."""
    reader = _get_file_reader('review.csv')
    for line in reader[1:]:
        _, created = Review.objects.get_or_create(
            pk=int(line[0]),
            title_id=Title.objects.get(pk=int(line[1])),
            text=line[2],
            author=User.objects.get(pk=int(line[3])),
            score=int(line[4]),
            pub_date=datetime.strptime(line[5], '%Y-%m-%dT%H:%M:%S.%fZ')
        )


def _load_comments():
    """Загрузка в модель коментариев."""
    reader = _get_file_reader('comments.csv')
    for line in reader[1:]:
        _, created = Comment.objects.get_or_create(
            pk=int(line[0]),
            review_id=Review.objects.get(pk=int(line[1])),
            text=line[2],
            author=User.objects.get(pk=int(line[3])),
            pub_date=datetime.strptime(line[4], '%Y-%m-%dT%H:%M:%S.%fZ')
        )


def _load_users():
    """Загрузка пользователей."""
    reader = _get_file_reader('users.csv')
    for line in reader[1:]:
        _, created = User.objects.get_or_create(
            pk=int(line[0]),
            username=line[1],
            email=line[2],
            role=line[3],
            bio=line[4],
            first_name=line[5],
            last_name=line[6]
        )


class Command(BaseCommand):
    help = 'Загрузка данных в БД'

    def handle(self, *args, **options):
        loaders = []
        if options['all']:
            loaders.append(_load_users)
            loaders.append(_load_category)
            loaders.append(_load_genre)
            loaders.append(_load_titles)
            loaders.append(_load_genre_title)
            loaders.append(_load_reviews)
            loaders.append(_load_comments)
        else:
            pass
        for loader in loaders:
            loader()

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            default=False,
            help='Загружать все таблицы.'
        )
