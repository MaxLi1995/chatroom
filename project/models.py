from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Message(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="message")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="messages")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "message": self.message,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Room(models.Model):
    name = models.TextField()
    password = models.TextField(blank=True)
    creator = models.ForeignKey("User", on_delete=models.CASCADE, related_name="owned_rooms")
    users = models.ManyToManyField("User", related_name="joined_rooms", blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "creator": self.creator.username
        }
