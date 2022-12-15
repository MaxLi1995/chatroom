import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from project.models import *


def index(request):
    return render(request, "chatroom/index.html")

def room_page(request, id):
    return render(request, "chatroom/room_page.html")

@csrf_exempt
@login_required
def add_message(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    rooms = Room.objects.filter(pk=data.get("roomId")).all()
    if len(rooms) == 0:
        return JsonResponse({"error": "Room does not exists"}, status=400)
    room = rooms[0]
    
    if not room.users.all().contains(request.user) and not room.creator == request.user:
        return JsonResponse({"error": "You do not have permission to see this room"}, status=400)

    message = Message(
        user= request.user,
        message=data.get("message"),
        room = room
        )
    message.save()
    return JsonResponse({"message": "Message added successfully."}, status=201)

@csrf_exempt
@login_required
def get_room(request, roomId):

    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    rooms = Room.objects.filter(pk=roomId).all()
    if len(rooms) == 0:
        return JsonResponse({"error": "Room does not exists"}, status=400)
    room = rooms[0]
    
    if not room.users.all().contains(request.user) and not room.creator == request.user:
        return JsonResponse({"error": "You do not have permission to see this room"}, status=400)
    
    return JsonResponse({
        "id": room.pk,
        "messages": [message.serialize() for message in room.messages.order_by("timestamp").all()],
        "users": [user.username for user in room.users.all()],
        "creator": room.creator.username,
        "my_room": room.creator == request.user
        }, safe=False)

@csrf_exempt
@login_required
def create_room(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    rooms = Room.objects.filter(name=data.get("name")).all()
    if len(rooms) > 0:
        return JsonResponse({"error": "Room already exists"}, status=400)
    newRoom = Room(
        name = data.get("name"),
        password = data.get("password"),
        creator = request.user
    )
    newRoom.save()
    return JsonResponse({"message": "Room created", "id": newRoom.pk}, safe=False)

@csrf_exempt
@login_required
def delete_room(request, roomId):

    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)

    rooms = Room.objects.filter(pk=roomId).all()
    if len(rooms) == 0:
        return JsonResponse({"error": "Room does not exists"}, status=400)
    if rooms[0].creator != request.user:
        return JsonResponse({"error": "No permission to delete"}, status=400)
    rooms[0].delete()
    return JsonResponse({"message": "Room deleted"}, safe=False)

@csrf_exempt
@login_required
def join_room(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    rooms = Room.objects.filter(name=data.get("name")).all()
    if len(rooms) == 0:
        return JsonResponse({"error": "Room does not exists"}, status=400)
    room = rooms[0]
    if room.password == data.get("password"):
        if not room.users.contains(request.user) and not room.creator == request.user:
            room.users.add(request.user)
            room.save()
        return JsonResponse({"message": "Room joined", "id": room.pk}, safe=False)
    return JsonResponse({"error": "Wrong password"}, status=400)

@csrf_exempt
@login_required
def leave_room(request, roomId):

    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)

    rooms = Room.objects.filter(pk=roomId).all()
    if len(rooms) == 0:
        return JsonResponse({"error": "Room does not exists"}, status=400)
    room = rooms[0]
    if room.users.all().contains(request.user):
        room.users.remove(request.user)
        room.save()
    if room.creator == request.user:
        users = room.users.all()
        if len(users) == 0:
            return delete_room(request, roomId)
        else:
            room.creator = users[0]
            room.users.remove(users[0])
            room.save()
    return JsonResponse({"message": "Room left"}, safe=False)

@csrf_exempt
@login_required
def kick_user(request):

    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)

    data = json.loads(request.body)
    rooms = Room.objects.filter(pk=data.get("roomId")).all()
    if len(rooms) == 0:
        return JsonResponse({"error": "Room does not exists"}, status=400)
    room = rooms[0]
    if room.creator != request.user:
        return JsonResponse({"error": "No permission to kick"}, status=400)
    user = User.objects.filter(username=data.get("username")).get()
    room.users.remove(user)
    room.save()
    return JsonResponse({"message": "User kicked"}, safe=False)

@csrf_exempt
@login_required
def get_open_rooms(request):

    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    rooms = Room.objects.filter(password="").all()
    return JsonResponse({"rooms": [room.serialize() for room in rooms]}, safe=False)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chatroom/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chatroom/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chatroom/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "chatroom/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chatroom/register.html")
