from django.urls import path
from .views import (
    login_view,
    logout_view,
    get_all_users
)


urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('users/', get_all_users, name='get_all_users'),
]
