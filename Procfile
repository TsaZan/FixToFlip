web: gunicorn FixToFlip.wsgi
worker: /home/site/wwwroot/venv/bin/celery -A FixToFlip worker --loglevel=info --pidfile=/tmp/celery_worker.pid
beat: /home/site/wwwroot/venv/bin/celery -A FixToFlip beat --loglevel=info --pidfile=/tmp/celery_beat.pid
