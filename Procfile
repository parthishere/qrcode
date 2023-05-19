web: gunicorn qrwebsite.wsgi:application -b 0.0.0.0:$PORT
celery: celery -A qrwebsite worker -l INFO -E