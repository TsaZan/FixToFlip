from django.core.exceptions import ValidationError
import datetime

from django.utils.deconstruct import deconstructible


def get_current_year():
    return datetime.date.today().year


def get_current_date():
    return datetime.date.today()


def offer_image_max_size_validator(value):
    if value.size > 10 * 1024 * 1024:
        raise ValidationError(f'Image size must be less than 10MB. Your file is {(value.size / 1024 / 1024):.0f}MB')


@deconstructible
class OnlyLettersValidator:
    def __init__(self, message=None):
        self.message = message or 'Only letters are allowed.'

    def __call__(self, value):
        for char in value:
            if not char.isalpha():
                raise ValidationError(self.message)
