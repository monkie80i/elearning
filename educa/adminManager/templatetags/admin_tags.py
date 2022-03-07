from django import template
from django.urls import reverse_lazy

register  = template.Library()

@register.filter
def rev_lazy(url_name):
    try:
        return reverse_lazy(url_name)
    except AttributeError:
        return None