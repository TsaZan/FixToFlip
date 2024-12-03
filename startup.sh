#!/bin/bash

source ./antenv/bin/activate

celery -A FixToFlip worker --loglevel=info &
