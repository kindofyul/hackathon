from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import *

def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        userid = request.POST['username']
        userpw = request.POST['password']

        user = auth.authenticate(request, username=userid, password=userpw)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html')
        
def logout(request):
    auth.logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    else:
        userid = request.POST['username']
        userpw = request.POST['password']
        new_user = User.objects.create_user(username=userid, password=userpw)
        auth.login(request, new_user)
        return redirect('home')

def explore(request):
    return render(request,'explore.html')

def mypage(request):
    return render(request,'mypage.html')

def commission(request):
    return render(request,'commission.html')
    
def commissionneedlogin(request):
    return redirect(commissionneedlogin)

def popup_view(request):
    return render(request, 'kakaotalk.html')