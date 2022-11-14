import datetime
import time
from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from .models import Post, Category, PostCategory


# задача для тестирования работы Celery
@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


# задача для тестирования работы Celery
@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


# функция, вызывающая по событию "добавление новой новости"
# асинхнонное выполнение в Celery задачи оповестить подписчиков
# о публикации новой статьи по подписке
@receiver(m2m_changed, sender=PostCategory)
def celery_notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []  # аннотация типа, она не валидация, ошибки не даст
        for category in categories:
            subscribers += category.subscribers.all()  # объекты модели User

            subscribers = [s.email for s in subscribers]

        celery_send_notifications.delay(instance.preview(), instance.pk, instance.title, subscribers)


@shared_task
# задача для Celery
# асинхронно выполняемая функция для оповещения о новой публикации по подписке
def celery_send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'celery_post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    print('контрольная точка до создания письма celery task о новой статье')
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=subscribers,

    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print('celery task отправки электронной почты о новой статье выполнена')


# функция для еженедельной рассылки новостей
@shared_task
def celery_week_notify():
    print('работает celery week оповещатель о статьях по расписанию')
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    # flat - чтобы на выходе был список, а не словарь с именами категорий
    subscribers = set(Category.objects.filter(name__in=categories).values_list(
        'subscribers__email', flat=True))
    html_content = render_to_string(
        'celery_daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts
        }

    )
    msg = EmailMultiAlternatives(
        subject='CELERY: Статьи за неделю',
        body='',  # пустой, потому что у нас есть шаблон
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=subscribers,  # вместо to используем bcc, чтобы не показывать всех получателей
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
