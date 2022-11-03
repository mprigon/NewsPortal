from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    # title = forms.CharField(
    #     empty_value='заголовок',
    #     max_length=128,
    #     required=True,
    #     )


    class Meta:
        model = Post
        fields = [
            'author',
            # 'categoryType', выбор - статья или новость
            'postCategory',
            'title',
            'text',
            ]

    # def clean_title(self):
    #     data = self.cleaned_data['title']
    #     if title == '':
    #         raise forms.ValidationError('А где же заголовок?')
    #     return data
    #
    # def clean_text(self):
    #     data = self.cleaned_data['text']
    #     if text == '':
    #         raise forms.ValidationError('А где же Ваш текст?')
    #     return data


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'author',
            # 'categoryType', выбор - статья или новость
            'postCategory',
            'title',
            'text',
        ]