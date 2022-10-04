from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter, CharFilter
from django.forms import DateTimeInput
from .models import Post, Category, PostCategory


class PostFilter(FilterSet):
    added_after = DateTimeFilter(  # календарь для поиска дата после
        field_name='time',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            # для тега HTML - <input> elements of type datetime-local create input controls that
            # let the user easily enter both a date and a time, including the year,
            # month, and day as well as the time in hours and minutes.
            # datetime-local выводит календарь
            attrs={'type': 'datetime-local'},
        ),
    )

    category = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Select a category',
    )

    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title',
    )

    # class Meta:
    #     model = Post
    #     fields = {
    #         'title': ['icontains'],  # поиск по названию
    #         'postCategory__name': ['icontains'],  # поиск по категории
    #     }
