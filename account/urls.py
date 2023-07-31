from django.contrib import admin
from django.urls import path
from account.views import *

app_name = 'account'

urlpatterns = [
    path('', home, name="home"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name="signup"),
    path('explore/', explore, name="explore"),
    path('commission/', commission, name="commission"),
    path('commissionneedlogin/', commissionneedlogin, name="commissionneedlogin"),
    path('mypage/', mypage, name="mypage"),
    path('popup/', popup_view, name='popup_view'),
]
