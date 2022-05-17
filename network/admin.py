from django.contrib import admin
from .models import User, Post

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active", "date_joined")
    list_filter = ("active", "date_joined")
    search_fields = ("username", "email")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "poster", "content", "created_on", "edited")
    list_filter = ("created_on")
    search_fields = ("username", "email")

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
