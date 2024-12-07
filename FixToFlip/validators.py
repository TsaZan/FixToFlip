from django.core.exceptions import ValidationError

from django.utils.deconstruct import deconstructible


@deconstructible
class OnlyLettersValidator:
    def __init__(self, message=None):
        self.message = message or 'Only letters are allowed.'

    def __call__(self, value):
        for char in value:
            if not char.isalpha():
                raise ValidationError(self.message)
