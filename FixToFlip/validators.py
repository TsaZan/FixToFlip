from django.core.exceptions import ValidationError
from django.db import models
import datetime


def get_current_year():
    return datetime.date.today().year


def get_current_date():
    return datetime.date.today()


def offer_image_max_size_validator(value):
    if value.size > 10 * 1024 * 1024:
        raise ValidationError(f'Image size must be less than 10MB. Your file is {(value.size / 1024 / 1024):.0f}MB')
