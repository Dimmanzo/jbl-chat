import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@permission_classes([IsAuthenticated])
# API endpoint that returns a list of all users (requires authetication).
def get_all_users(request):
    # Fetches all users returning only id's and usernames.
    user_data = User.objects.values("id", "username")
    return JsonResponse(
        list(user_data),
        safe=False
        )


@csrf_exempt
def login_view(request):
    """
    Handles user login.
    - For GET requests, returns a message explaining how to log in.
    - For POST requests, checks username/password and starts a session.
    """
    if request.method == "GET":
        return JsonResponse(
            {"message": "Use POST with 'username' and 'password' to log in."}
        )

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username, password = data.get("username"), data.get("password")

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse(
                    {"message": "Successfully logged in!"},
                    status=200
                )
            return JsonResponse(
                {"error": "Invalid username or password"},
                status=400
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON format"},
                status=400)

    # If the request method is something else, return an error.
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def logout_view(request):
    """
    Handles user logout.
    - GET: Returns instructions for logging out.
    - POST: Logs the user out and ends the session.
    """
    if request.method == "GET":
        return JsonResponse(
            {"message": "Use POST request to logout."}
        )

    if request.method == "POST":
        logout(request)
        return JsonResponse(
            {"message": "You have been logged out!"},
            status=200
        )

    # If the request method is something else, return an error.
    return JsonResponse({"error": "Method not allowed"}, status=405)
