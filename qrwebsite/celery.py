from __future__ import absolute_import, unicode_literals

from celery import Celery
import os

    
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qrwebsite.settings')


app = Celery("qrwebsite")


app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    
}
app.autodiscover_tasks()

# Celery beat settings
    

@app.task(bind=True)
def debug_task(self):
    print(f'{self.request}')