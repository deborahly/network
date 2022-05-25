from django.contrib import admin
from .models import User, Post, Follow, Like

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active", "date_joined")
    list_filter = ("active", "date_joined")
    search_fields = ("username", "email")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "poster", "content", "created_on", "edited")
    list_filter = ("created_on")
    search_fields = ("username", "email")

class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "followed", "active")
    list_filter = ("follower", "followed", "active")
    search_fields = ("follower", "followed")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("post", "liked_by")
    list_filter = ("liked_by")
    search_fields = ("post", "liked_by")

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)
