from django.contrib import admin

from .models import (
    Category,
    Genre,
    Title,
    GenreTitle,
    Review,
    Comment
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass
    list_display = ('name', 'year', 'category')
    search_fields = ('name', 'category__name', 'description')
    list_filter = ('year', 'category')


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'score', 'title')
    search_fields = ('text', 'title__name')
    list_filter = ('author', 'score', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'review', )
    list_filter = ('author', )
    search_fields = ('review__text', 'text')
