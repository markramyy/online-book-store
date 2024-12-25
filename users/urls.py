from django.urls import path
from users.views import *

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change-password/', change_password, name='change_password'),
]
