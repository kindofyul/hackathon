from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import *
from posting.views import *

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
            return redirect('account:home')
        else:
            return render(request, 'login.html')
        
def logout(request):
    auth.logout(request)
    return redirect('account:home')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    else:
        detail = UserDetail()
        detail.legalname = request.POST['legalname']
        detail.phone = request.POST['phone']
        detail.address = request.POST['address']
        detail.bankaccount = request.POST['bankaccount']
        detail.userid = request.POST['username']
        detail.userpw = request.POST['password']
        detail.save()
        new_user = User.objects.create_user(username=detail.userid, password=detail.userpw)
        auth.login(request, new_user)
        return redirect('account:home')

def explore(request):
    return render(request,'explore.html')

def mypage(request):
    return render(request,'mypage.html')

def commission(request):
    return posting(request)
    
def commissionneedlogin(request):
    return render(request, 'commissionneedlogin.html')

def popup_view(request):
    return render(request, 'kakaotalk.html')