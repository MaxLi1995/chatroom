from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from project.models import User, Message, Room
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Message)
admin.site.register(Room)
