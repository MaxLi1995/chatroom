
from django.urls import path

from project import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("room/<int:id>", views.room_page, name="room_page"),

# API Routes
    path("message", views.add_message, name="add_message"),
    path("room_info/<int:roomId>", views.get_room, name="get_room"),
    path("create", views.create_room, name="create_room"),
    path("delete/<int:roomId>", views.delete_room, name="delete_room"),
    path("join", views.join_room, name="join_room"),
    path("leave_room/<int:roomId>", views.leave_room, name="leave_room"),
    path("kick_user", views.kick_user, name="kick_user"),
    path("open_rooms", views.get_open_rooms, name="get_open_rooms")
]