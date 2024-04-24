from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
@stringfilter
def split(string, sep):
    """Return the string split by sep.

    Example usage: {{ value|split:"/" }}
    """
    return string.split(sep)


@register.filter
@stringfilter
def underscore_to_hyphen(string):
    """문자열의 _을 -로 변환한다.

    Example usage: {{ value| underscore_to_hyphen }}
    """
    return string.replace('_', '-')
