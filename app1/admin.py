from django.contrib import admin
from .models import Category, Post, Author, PostCategory, Comment


def my_action(modeladmin, request, queryset):
    my_action.short_description = 'Empty action'


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями,
    # которые вы хотите видеть в таблице с публикациями
    # list_display = [field.name for field in Post._meta.get_fields()]
    # генерируем список имён всех полей для более красивого отображения
    # выдает ошибку на поле ManyToMany, которое не поддерживается
    list_display = ['time', 'title', 'author']
    list_filter = ['title', 'author']
    search_fields = ['postCategory__name']
    ordering = ['time']
    actions = [my_action]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['authorUser', 'ratingAuthor']
    list_filter = ['authorUser']
    search_fields = ['authorUser']
    ordering = ['authorUser']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'commentUser', 'dateCreation',
                    'rating']
    list_filter = ['commentUser', 'dateCreation']
    search_fields = ['commentUser']
    ordering = ['commentUser']

# Register your models here.

admin.site.register(Category)
admin.site.register(Post, PostAdmin)

admin.site.register(Author, AuthorAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
