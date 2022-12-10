from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField("User", related_name="liked", blank=True)

    def serialize(self, username):
        return {
            "id": self.id,
            "poster": self.user.username,
            "posterid": self.user.pk,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "liker" : self.likers.count(),
            "self_post": self.user.username == username
        }

class Profile(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="profile")
    followers = models.ManyToManyField("User", related_name="following", blank=True)
