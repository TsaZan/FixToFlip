web: gunicorn FixToFlip.wsgi:application --bind=0.0.0.0:8000
worker: celery -A FixToFlip worker --loglevel=info
beat: celery -A FixToFlip beat --loglevel=info