from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=150, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.content}'
