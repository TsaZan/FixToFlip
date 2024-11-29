#!/bin/bash

gunicorn FixToFlip.wsgi:application --bind=0.0.0.0

celery -A FixToFlip worker --loglevel=info &
