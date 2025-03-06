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
    path("", chat_view, name="chat_view"),
    path("login/", login_view, name="login_view"),
    path("logout/", logout_view, name="logout_view"),
    path("users/", get_all_users, name="get_all_users"),
    path(
        "messages/<int:user_id>/",
        fetch_chat_history,
        name="fetch_chat_history"
    ),
    path("send_message/", send_message, name="send_message"),
]
