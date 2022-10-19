from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostListSearch, NewsCreate, \
    NewsEdit, NewsDelete, ArticleCreate, ArticleDelete, TestView, \
    CategoryListView, subscribe, HomePageView

urlpatterns = [
    # path — означает путь.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('news/', PostList.as_view(), name='news_article'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_id'),
    path('news/search/', PostListSearch.as_view(), name='news_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', NewsEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('', HomePageView.as_view(), name='home_page'),

    path('test/', TestView.as_view(), name='test'),


]