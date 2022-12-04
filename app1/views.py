# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
import logging


from django.core.cache import cache
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView,\
    DeleteView
from django.views import View
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Post, Category
from .filters import PostFilter
from .forms import NewsForm, ArticleForm
from .tasks import hello, printer

# from django.http import HttpResponseRedirect
# from django import forms
# from django.core.exceptions import ValidationError
import datetime

from django.conf import settings


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_all.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # количество записей на странице


class PostListSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news_search'
    paginate_by = 4  # количество записей на странице

    # Переопределяем функцию получения списка публикаций
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список публикаций
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной публикации
    model = Post
    # Используем другой шаблон — news_id.html
    template_name = 'news_id.html'
    # Название объекта, в котором будет выбранная пользователем публикация
    context_object_name = 'news_id'  # используем в news_delete.html, article_delete.html

    logger = logging.getLogger(__name__)
    logger.error('hello from logger.error in PostDetail')

    # добавляем кэширование страниц по отдельной публикации
    # напоминание про pk и id
    # можно переопределить название pk, например, на id
    # pk_url_kwarg = 'id'
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


# Добавляем новое представление для создания Новости.
class NewsCreate(PermissionRequiredMixin, CreateView):
    print('начало работы view NewsCreate')
    permission_required = ('app1.add_post')
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель публикаций
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_create.html'

    def form_valid(self, form):
        # categoryType - выбираем в зависимости от того, с какой страницы запрос
        # /news/create/ - NEWS

        post = form.save(commit=False)
        print('валидация form.save')
        post.categoryType = 'NW'

        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('app1.change_post')
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('app1.delete_post')
    raise_exception = True
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_article')
    context_object_name = 'news_id'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('app1.add_post')
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = ArticleForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'article_create.html'

    def form_valid(self, form):
        # categoryType - выбираем в зависимости от того, с какой страницы запрос
        # /articles/create/ - ARTICLES

        post = form.save(commit=False)
        post.categoryType = 'AR'

        return super().form_valid(form)
        # запрет публиковать более трех статей в день


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('app1.delete_post')
    raise_exception = True
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_article')
    context_object_name = 'news_id'


class TestView(View):
    def get(self, request, *args, **kwargs):
        current_path = request.path
        current_method = request.method
        current_get = request.GET
        return HttpResponse(f"CreatePost {current_path} method = {current_method} GET param = {current_get}")


class HomePageView(ListView):
    model = Post
    template_name = 'home_page.html'

    # запуск задач по открытию домашней страницы
    # тестирование Celery
    # def get(self, request):
    #     # printer.delay(10)
    #     printer.apply_async([10], countdown=5)
    #     hello.delay()
    #     return HttpResponse('Hello!')


# view для страницы, на которой можно будет подписаться на определенную категорию новостей
class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'
    ordering = '-time'

    def get_queryset(self):
        # фильтруем новости по категории, которую передали в адресе страницы как pk
        # метод ..._404 удобен, так как не требуется обрабатывать ошибку, если категории нет
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category)
        # .order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # кнопка "подписаться" должна появляться у тех, кто еще не подписан
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    """Subscribe authorized user to news in specific category"""
    user = request.user
    category = Category.objects.get(id=pk)
    # можно было бы и здесь использовать get_object_or_404, а не просто get но
    # сюда мы будем передавать pk только существующей категории
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def author_status_request(request):
    """Send e-mail request to administrator to acquire Author status.
    Admin will give the status manually."""
    user = request.user
    # user_email = request.user.email
    mail_subject = 'Zayavka заявка'
    admin_message = f'Пользователь {user}. Заявка на статус "Автор" через сайт'
    confirm_message = 'Ваша заявка на присвоение статуса "Автор" направлена администратору'
    send_mail(
        subject=mail_subject,
        message=admin_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL]
    )

    return render(request, 'author_status_request.html', {'message': confirm_message})
