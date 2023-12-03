from celery.schedules import crontab

from entry_app import create_app
from entry_app.celery_tasks import backup_entries


flask_app = create_app()
celery_app = flask_app.extensions["celery"]

celery_app.conf.timezone = 'UTC'
celery_app.conf.beat_schedule = {
    'backup-entries-every-week': {
        'task': 'entry_app.celery_tasks.backup_entries',
        # 'schedule': crontab(hour=2, minute=00, day_of_week=1),
        'schedule': crontab(minute='*/15'),
    },
}

