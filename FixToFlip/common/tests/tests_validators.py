from unittest import TestCase

from django.core.exceptions import ValidationError

from FixToFlip.validators import OnlyLettersValidator


class OnlyLettersValidatorTest(TestCase):
    def test_valid_input(self):
        validator = OnlyLettersValidator(message="Custom error message")
        try:
            validator("ValidName")
        except ValidationError:
            self.fail("Validator raised ValidationError for valid input.")

    def test_invalid_input(self):
        validator = OnlyLettersValidator(message="Custom error message")
        with self.assertRaises(ValidationError) as context:
            validator("Invalid1Name")
        self.assertEqual(str(context.exception.message), "Custom error message")
