from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="likers", blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": [user.username for user in self.likes.all()],
        }

class UserFollowing(models.Model):
    user = models.ForeignKey("User", related_name="following", on_delete=models.CASCADE)
    following_user = models.ManyToManyField("User", related_name="followers", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
