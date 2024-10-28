from django import template
from django.template.defaultfilters import stringfilter
import readtime

import markdown as md

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.filter(is_safe=True)
@stringfilter
def add_dashes(value):
    """
    Add slashes before quotes. Useful for escaping strings in CSV, for
    example. Less useful for escaping JavaScript; use the ``escapejs``
    filter instead.
    """
    return value.strip().replace(' ', '-')


@register.filter(is_safe=True, name='readtime')
@stringfilter
def read(html):
    return readtime.of_html(html)
