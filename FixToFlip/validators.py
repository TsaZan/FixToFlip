from django.core.exceptions import ValidationError

from django.utils.deconstruct import deconstructible
import re


@deconstructible
class OnlyLettersValidator:
    def __init__(self, message=None):
        self.message = message or 'Only letters are allowed.'

    def __call__(self, value):
        for char in value:
            if not char.isalpha():
                raise ValidationError(self.message)


with open("./FixToFlip/badwords.txt") as f:
    BAD_WORDS = f.read().splitlines()


def bad_words_validator(text):
    words = set(re.sub(r"[^\w]", " ", text).split())
    for bad_word in BAD_WORDS:
        if bad_word in words:
            raise ValidationError(f"Word {bad_word} is not allowed.")


def image_validator(value):
    if not value:
        return value

    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
    if value.content_type not in valid_mime_types:
        raise ValidationError('Unsupported file type. Please upload a JPEG, PNG or GIF image.')

    max_file_size = 5 * 1024 * 1024
    if value.size > max_file_size:
        raise ValidationError('File size exceeds the maximum limit of 5MB.')

    return value
