# yourapp/templatetags/querystring.py
from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def querystring_replace(context, **kwargs):
    """
    Allows query string manipulation from templates.
    Example: {% querystring_replace page2=2 %}
    """
    request = context['request']
    query = request.GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return '?' + urlencode(query)
