import csv
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand

# Заменить api_v1 на имя приложения
from api_v1.models import (Genre, Category, Title, GenreTitle, Review,
                           Comment, User)


def _get_file_reader(filename):
    filepath = Path.joinpath(Path.cwd(), 'static', 'data', filename)
    if filepath.is_file():
        with open(filepath) as f:
            reader = csv.reader(f)
    return reader


def _load_category():
    """Загрузка в модель категорий."""
    reader = _get_file_reader('category.csv')
    next(reader)
    for line in reader:
        _, created = Category.objects.get_or_create(
            pk=int(line[0]),
            name=line[1],
            slug=line[2]
        )


def _load_genre():
    """Загрузка в модель жанров."""
    reader = _get_file_reader('genre.csv')
    next(reader)
    for line in reader:
        _, created = Genre.objecs.get_or_create(
            pk=int(line[0]),
            name=line[1],
            slug=line[2]
        )


def _load_genre_title():
    """Загрузка в модель отношения произведение-жанр."""
    reader = _get_file_reader('genre_title.csv')
    next(reader)
    for line in reader:
        _, created = GenreTitle.objects.get_or_create(
            pk=int(line[0]),
            title_id=Title.objects.get(pk=int(line[1])),
            genre_id=Genre.objects.get(pk=int(line[2]))
        )


def _load_titles():
    """Загрузка в модель произведений."""
    reader = _get_file_reader('titles.csv')
    next(reader)
    for line in reader:
        _, created = Title.objects.get_or_create(
            pk=int(line[0]),
            name=line[1],
            year=datetime.strftime(line[2], "%Y").date(),
            category=Category.objects.get(pk=int(line[3]))
        )


def _load_reviews():
    """Загрузка в модель рецензий."""
    reader = _get_file_reader('titles.csv')
    next(reader)
    for line in reader:
        _, created = Review.objects.get_or_create(
            pk=int(line[0]),
            title_id=Title.objects.get(pk=int(line[1])),
            text=line[2],
            author=User.objects.get(pk=int(line[3])),
            score=int(line[4]),
            pub_date=datetime.strptime(line[5], '%Y-%B-%dT%H:%M:%S.%fZ%Z')
        )


class Command(BaseCommand):
    help = 'Загрузка данных в БД'

    def handle(self, *args, **options):
        if options['all']:
            pass
        else:
            pass

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            default=False,
            help='Загружать все таблицы.'
        )
