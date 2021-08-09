from django import template
from notes.models import Note

register = template.Library()


@register.filter(name="calculate_stars")
def calculate_stars(value):
    max_stars = 5
    stars_left = max_stars - value
    return stars_left


@register.filter(name="check_user")
def check_user(user):
    return Note.objects.filter(author=user)
