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
from django.conf.urls import patterns, include
from views import welcome, login, register, register2, add_friend, show_profile, modify_profile
from views import ajax_check_email_field, ajax_add_friend
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
  ('^$', welcome), # au lieu de login
  ('^login$', login),
  ('^welcome$', welcome),
  ('^register$', register),
  ('^register2$', register2),
  ('^addFriend$', add_friend),
  ('^showProfile$', show_profile),
  ('^modifyProfile$', modify_profile),
  ('^ajax/checkEmailField$', ajax_check_email_field),
  ('^ajax/addFriend$', ajax_add_friend),
  ('^admin/', include(admin.site.urls))
)
