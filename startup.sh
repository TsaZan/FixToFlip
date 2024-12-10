#!/bin/bash

gunicorn FixToFlip.wsgi --bind=0.0.0.0:$PORT

celery -A FixToFlip worker --loglevel=info &

celery -A FixToFlip beat --loglevel=info --schedule=/home/site/beat-data/celerybeat-schedule
