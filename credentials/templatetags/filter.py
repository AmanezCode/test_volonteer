from django import template

register = template.Library()

@register.filter
def is_registered(event, username):
    return event.volunteer_set.filter(profile__username__username=username).exists()
