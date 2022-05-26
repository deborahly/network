from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=150, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.content}"

    def serialize1(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "created_on": self.created_on.strftime("%b %d %Y, %I:%M %p"),
            "edited": self.edited,
            "likes": self.likes_received.count(),
            "liked_by_user": True
        }

    def serialize2(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "created_on": self.created_on.strftime("%b %d %Y, %I:%M %p"),
            "edited": self.edited,
            "likes": self.likes_received.count(),
            "liked_by_user": False
        }

    def is_valid_post(self):
        return self.content != "" and len(self.content) <= 150

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_by")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.active}: {self.follower} follows {self.followed}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes_received")
    liked_by = models.ManyToManyField(User, related_name="likes")

    def __str__(self):
        return f"{self.post} liked by {self.liked_by.all()}"