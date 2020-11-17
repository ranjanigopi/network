from django import template

register = template.Library()


@register.filter
def user_likes(likes, user):
    return any(like.liker == user for like in likes.all())
