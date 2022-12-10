from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from network.models import User, Post, Profile
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Profile)
