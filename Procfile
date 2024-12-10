web: gunicorn FixToFlip.wsgi
worker: celery -A FixToFlip worker --loglevel=info
beat: celery -A FixToFlip beat --loglevel=info