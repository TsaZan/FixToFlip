from django import template

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
