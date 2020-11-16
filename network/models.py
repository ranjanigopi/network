from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.utils import timezone


class NewPost(forms.Form):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={"placeholder": "Whats happening today.."})
    )

    def __init__(self, *args, **kwargs):
        super(NewPost, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control max-width-50'})


class User(AbstractUser):
    pass


class Posts(models.Model):
    creator = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    content = models.TextField(max_length=500)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.creator} \n {self.content} \n Posted on {self.created}"


class Follows(models.Model):
    followee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="follower")
    follower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="following")

    def __str__(self):
        return f"{self.follower} following {self.followee}"


class Like(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.SET_NULL, null=True, blank=True, related_name="likes")
    liker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="liker")

    def __dir__(self):
        return f"{self.liker} liked {self.post_id}"





