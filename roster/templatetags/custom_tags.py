# custom_tags.py

from django import template
from ..utils import get_completeness_percentage, get_missing_years

register = template.Library()

@register.simple_tag
def get_completeness_percentage():
    return get_completeness_percentage()

@register.simple_tag
def get_missing_years():
    return get_missing_years()
