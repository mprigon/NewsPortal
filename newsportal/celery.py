import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsportal.settings')

app = Celery('newsportal')

app.config_from_object('django.conf:settings', namespace='CELERY')

# тестовая задача для проверки Celery
app.conf.beat_schedule = {
    'action_every_5_seconds': {
        'task': 'app1.tasks.printer',
        'schedule': 5,
        'args': (5,),
     },
}

# задача - предупредить о новой статье по подписке
app.conf.beat_schedule = {
    'check_new_post_every_30_sec': {
        'task': 'app1.tasks.celery_notify_about_new_post',
        'schedule': 30.0,
        'args': None
        }
}

# задача - еженедельная рассылка новостей по подписке
app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'app1.tasks.celery_week_notify',
        # чтобы фактически было отправлено в 8 утра, время надо
        # задать с учетом разницы на 3 часа в Celery, то есть, 5
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': None
        }
}

app.autodiscover_tasks()
