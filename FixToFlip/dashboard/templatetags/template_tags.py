from allauth.account.models import EmailAddress
from django import template
from django.utils import timezone

from FixToFlip import settings

register = template.Library()


@register.simple_tag
def active_url(request, url_name):
    if request.resolver_match.url_name == url_name:
        return 'active'


@register.simple_tag
def icon_src(request, base_name, url_name):
    if request.resolver_match.url_name == url_name:
        return f"{base_name}_active.svg"
    return f"{base_name}.svg"


@register.filter
def add_class(field, class_name):
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name))
    })


@register.simple_tag
def verified_header(user):
    if user.is_authenticated:
        return EmailAddress.objects.filter(user=user, verified=True).exists()
    return False


@register.simple_tag
def days_to_confirm(user):
    expiration_days = settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS
    days_since_joined = (timezone.now() - user.date_joined).days
    remaining_days = expiration_days - days_since_joined
    return remaining_days
