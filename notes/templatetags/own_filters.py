from django import template

register = template.Library()


@register.filter(name="calculate_stars")
def calculate_stars(value):
    max_stars = 5
    stars_left = max_stars - value
    return stars_left
