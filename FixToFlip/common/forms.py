from django import forms
from django.core.validators import EmailValidator, MinLengthValidator
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3


class ContactUsForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        validators=[MinLengthValidator(5, "Name must be at least 5 characters long.")],
    )
    name.widget.attrs["placeholder"] = "Enter your name"

    email = forms.CharField(validators=[EmailValidator()])
    email.widget.attrs["placeholder"] = "Enter your email address"

    message = forms.CharField(
        widget=forms.Textarea,
        validators=[
            MinLengthValidator(30, "Message must be at least 20 characters long.")
        ],
    )
    message.widget.attrs["placeholder"] = "Enter your message"

    captcha = ReCaptchaField(widget=ReCaptchaV3())
