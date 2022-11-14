from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import PostCategory


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    # print('контрольная точка до формирования электронной почты о новой статье')
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=subscribers,  # Если не хочется, чтобы подписчики видели адреса других
        # можно использовать bcc - поле to не обязательное.
        # скрытая копия, адреса не показываются другим получателям
        # или отправлять в цикле
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print('команда отправки электронной почты о новой статье выполнена')


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []  # аннотация типа, не валидация, ошибки не даст
        for category in categories:
            subscribers += category.subscribers.all()  # объекты модели User

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk,
                           instance.title, subscribers)
