from django.urls import path
from django.views.decorators.cache import cache_page

# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostListSearch, NewsCreate, \
    NewsEdit, NewsDelete, ArticleCreate, ArticleDelete, TestView, \
    CategoryListView, subscribe, HomePageView, author_status_request


urlpatterns = [
    # path — означает путь.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    # добавляем кэширование 1 минуту на главную страницу
    path('news/', cache_page(60)(PostList.as_view()), name='news_article'),
    # и кэширование 5 минут на страницу отдельной новости
    path('news/<int:pk>', cache_page(60 * 5)(PostDetail.as_view()), name='news_id'),
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
    path('news/author_status_request/', author_status_request, name='author_status_request'),

    path('test/', TestView.as_view(), name='test'),

]
