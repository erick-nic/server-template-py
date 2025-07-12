from django.urls import path
from .views import delete_user, list_users, register_user, login_user, logout_user, retrieve_user, update_user

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('users/list/', list_users, name='list_users'),
    path('users/<uuid:user_id>/', retrieve_user, name='retrieve_user'),
    path('users/edit/<uuid:user_id>', update_user, name='edit_user'),
    path('users/delete/<uuid:user_id>', delete_user, name='delete_user'),    
]
