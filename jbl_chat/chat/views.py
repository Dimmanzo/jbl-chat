import json

from django.db.models import Q
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from chat.models import Message


def home_view(request):
    """"
    Starter endpoint that gives basic API info.
    """
    return JsonResponse({
        "message": "Welcome to the JBL Chat API!",
        "info": "HTMX-powered chat interface is coming sooon!",
        "endpoints": {
            "chat": "/chat/",  # Future UI
            "login": "/chat/login",
            "logout": "/chat/logout",
            "users": "/chat/users",
            "messages": "/chat/messages/{user_id}/"
        }
    })


@csrf_exempt
def login_view(request):
    """
    Handles user login. If not logged in, shows the login form.
    """
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body)  # JSON Data
            else:
                data = request.POST  # Form-data
            username, password = data.get("username"), data.get("password")

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                # Redirect to chat after login
                return redirect("chat_view")

            return render(
                request, "chat/login.html",
                {"error": "Invalid username or password"}
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON format"},
                status=400)

    # Returns login form on GET request
    return render(request, "chat/login.html")


@csrf_exempt
def logout_view(request):
    """
    Logs the user out and dynamically returns the login page via HTMX.
    """
    if request.method == "POST":
        logout(request)
        return render(request, "chat/login.html")  # Swap chat with login form

    # If someone visits /chat/logout/ directly via GET, show a friendly message
    return JsonResponse(
            {"message": "Use POST request to logout."}, status=405
        )


@login_required
def chat_view(request):
    """
    Displays chat interface with a list of users and latest messages.
    """
    # Get all users except the logged-in user
    users = User.objects.exclude(id=request.user.id)

    return render(
        request, "chat/chat.html",
        {"users": users}
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    """
    API endpoint that returns a list of all users (requires authetication).
    Fetches all users returning only id's and usernames.
    """
    user_data = User.objects.values("id", "username")
    return JsonResponse(
        list(user_data),
        safe=False
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetch_chat_history(request, user_id):
    """
    Retrieves past messages between the logged-in user and another user.
    """
    current_user = request.user  # Get the logged-in user
    recipient = get_object_or_404(User, id=user_id)  # Ensure recipient

    # Fetch messages where the logged-in user is involved (sender or receiver)
    conversation = Message.objects.filter(
        Q(sender=current_user, receiver=recipient) |
        Q(sender=recipient, receiver=current_user)
    ).order_by("timestamp")

    return JsonResponse(
        {"messages": [
            {"from": msg.sender.username,
                "to": msg.receiver.username,
                "message": msg.message}
            for msg in conversation
        ]},
        safe=False
    )


def handle_not_found(request, exception):
    """"
    Handles requests to non-existing API endpoints and returns a JSON response.
    """
    return JsonResponse(
        {"error": "Endpoint not found"}, status=404
    )
