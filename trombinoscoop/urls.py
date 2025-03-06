from django.contrib import admin
from django.urls import path
from trombinoscoop.views import (
    welcome, login, register, register2, add_friend, show_profile,
    modify_profile, ajax_check_email_field, ajax_add_friend
)

urlpatterns = [
    # Routes principales
    path('', welcome, name='home'),
    path('login/', login, name='login'),
    path('welcome/', welcome, name='welcome'),
    path('register/', register, name='register'),
    path('register2/', register2, name='register2'),
    path('addFriend/', add_friend, name='add_friend'),
    path('showProfile/', show_profile, name='show_profile'),
    path('modifyProfile/', modify_profile, name='modify_profile'),

    # Routes Ajax (sous un préfixe /ajax/)
    path('ajax/checkEmailField/', ajax_check_email_field, name='ajax_check_email_field'),
    path('ajax/addFriend/', ajax_add_friend, name='ajax_add_friend'),

    # URL admin
    path('admin/', admin.site.urls),
]
