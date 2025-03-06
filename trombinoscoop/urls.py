"""
URL configuration for trombinoscoop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, re_path, include
from django.contrib import admin
from trombinoscoop.views import (
    welcome, login, register, register2, add_friend, show_profile,
    modify_profile, ajax_check_email_field, ajax_add_friend
)


urlpatterns = [
    path('', welcome, name='home'),
    path('login/', login, name='login'),
    path('welcome/', welcome, name='welcome'),
    path('register/', register, name='register'),
    path('register2/', register2, name='register2'),
    path('addFriend/', add_friend, name='add_friend'),
    path('showProfile/', show_profile, name='show_profile'),
    path('modifyProfile/', modify_profile, name='modify_profile'),
    path('ajax/checkEmailField/', ajax_check_email_field, name='ajax_check_email_field'),
    path('ajax/addFriend/', ajax_add_friend, name='ajax_add_friend'),
    path('admin/', admin.site.urls),
]
