#!/bin/bash

celery -A FixToFlip worker --loglevel=info &
