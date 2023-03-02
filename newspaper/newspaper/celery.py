import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newspaper.settings')

app = Celery('newspaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_digest': {
        'task': 'news.tasks.broadcast',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
    'update_ratings': {
        'task': 'news.tasks.update_authors_rating',
        'schedule': crontab(minute=0, hour=0),
    },
}
