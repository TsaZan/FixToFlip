#!/bin/bash

gunicorn FixToFlip.wsgi --bind=0.0.0.0:8000 &

celery -A FixToFlip worker --loglevel=info &

celery -A FixToFlip beat --loglevel=info --schedule=/home/site/beat-data/celerybeat-schedule
