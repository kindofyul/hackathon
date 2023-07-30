from django.contrib import admin
from django.urls import path
from posting.views import *

app_name = 'posting'

urlpatterns = [
    path('create/', posting, name="posting"),
    path('confirmation/', confirmation, name="confirmation"),  # name 추가
]
