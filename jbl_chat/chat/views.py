from django.contrib.auth.models import User
from django.http import JsonResponse


# API endpoint that returns a list of all users.
def get_all_users(request):
    # Gets only id's and usernames.
    user_data = User.objects.values("id", "username")
    return JsonResponse(list(user_data), safe=False)
