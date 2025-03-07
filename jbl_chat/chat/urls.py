from django.urls import path
from .views import (
    login_view,
    logout_view,
    get_all_users,
    fetch_chat_history,
    chat_view,
    send_message
)

urlpatterns = [
    # Main chat view
    path("", chat_view, name="chat_view"),

    # Auth routes
    path("login/", login_view, name="login_view"),
    path("logout/", logout_view, name="logout_view"),

    # List of all users
    path("users/", get_all_users, name="get_all_users"),

    # Chat functionality
    path(
        "messages/<int:user_id>/",
        fetch_chat_history,
        name="fetch_chat_history"
    ),
    path("send_message/", send_message, name="send_message"),
]
