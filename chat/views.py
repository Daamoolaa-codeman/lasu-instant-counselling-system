# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


@login_required(login_url="/login/student")
def chat_room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': request.user.username
    })
