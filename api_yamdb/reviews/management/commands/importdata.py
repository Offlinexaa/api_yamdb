import csv
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


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
            title=Title.objects.get(pk=int(line[1])),
            genre=Genre.objects.get(pk=int(line[2]))
        )


def _load_titles():
    """Загрузка в модель произведений."""
    reader = _get_file_reader('titles.csv')
    for line in reader[1:]:
        _, created = Title.objects.get_or_create(
            pk=int(line[0]),
            name=line[1],
            year=int(line[2]),
            category=Category.objects.get(pk=int(line[3]))
        )


def _load_reviews():
    """Загрузка в модель рецензий."""
    reader = _get_file_reader('review.csv')
    for line in reader[1:]:
        _, created = Review.objects.get_or_create(
            pk=int(line[0]),
            title=Title.objects.get(pk=int(line[1])),
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
            review=Review.objects.get(pk=int(line[1])),
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
            if options['category']:
                loaders.append(_load_category)
            if options['genre']:
                loaders.append(_load_genre)
            if options['titles']:
                loaders.append(_load_titles)
            if options['review']:
                loaders.append(_load_reviews)
            if options['comments']:
                loaders.append(_load_comments)
            if options['users']:
                loaders.append(_load_users)
            if options['genre_title']:
                loaders.append(_load_genre_title)

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
        parser.add_argument(
            '-ca',
            '--category',
            action='store_true',
            default=False,
            help='Загружать категории'
        )
        parser.add_argument(
            '-g',
            '--genre',
            action='store_true',
            default=False,
            help='Загружать жанры'
        )
        parser.add_argument(
            '-t',
            '--titles',
            action='store_true',
            default=False,
            help='Загружать произведения'
        )
        parser.add_argument(
            '-r',
            '--review',
            action='store_true',
            default=False,
            help='Загружать рецензии'
        )
        parser.add_argument(
            '-co',
            '--comments',
            action='store_true',
            default=False,
            help='Загружать коментарии'
        )
        parser.add_argument(
            '-u',
            '--users',
            action='store_true',
            default=False,
            help='Загружать пользователей'
        )
        parser.add_argument(
            '-gt',
            '--genre_title',
            action='store_true',
            default=False,
            help='Загружать связь произведений и категорий'
        )
