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
        return f'{self.content}'

    def is_valid_post(self):
        return self.content != "" and len(self.content) <= 150
