from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
        user = auth.authenticate(request, userid, userpw)

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
    
    elif request.method == 'POST':
        legalname = request.POST['legalname']
        phone = request.POST['phone']
        address = request.POST['address']
        bankaccount = request.POST['bankaccount']
        username = request.POST['username']
        password = request.POST['password']

        # UserDetail 모델에 사용자 정보 저장
        user = UserDetail.objects.create(legalname=legalname, phone=phone, address=address, bankaccount=bankaccount,
                                           userid=username, userpw=password)

        # User 모델에 사용자 생성
        new_user = User.objects.create_user(username=username, password=password)

        # UserDetail과 User 모델 연결
        user.user = new_user
        user.save()

        # 로그인 처리
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

@login_required
def mypage(request):
    user_detail = get_object_or_404(UserDetail, user=request.user)
    return render(request, 'mypage.html', {'user_detail': user_detail})

@login_required
def mypage_edit(request):
    user_detail = UserDetail.objects.get(user=request.user)

    if request.method == 'POST':
        # 사용자가 수정한 정보 가져오기
        user_detail.legalname = request.POST['legalname']
        user_detail.phone = request.POST['phone']
        user_detail.address = request.POST['address']
        user_detail.bankaccount = request.POST['bankaccount']

        # UserDetail 모델의 save() 메서드를 사용하여 변경된 정보 저장
        user_detail.save()

        messages.success(request, '정보가 성공적으로 수정되었습니다.')
        return redirect('account:mypage')

    return render(request, 'mypage_edit.html', {'user_detail': user_detail})