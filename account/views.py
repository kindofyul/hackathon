from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from posting.views import *
from posting.models import *
from django.http import HttpResponseForbidden



def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

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
                                           username=username, password=password)

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

def mypage(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    
    user_detail = get_object_or_404(UserDetail, user=request.user)
    return render(request, 'mypage.html', {'user_detail': user_detail})

def mypage_edit(request):
    if not request.user.is_authenticated:
        return redirect('account:login')

    user_detail = UserDetail.objects.get(user=request.user)

    if request.method == 'POST':
        # 사용자가 수정한 정보 가져오기
        user_detail.legalname = request.POST['legalname']
        user_detail.phone = request.POST['phone']
        user_detail.address = request.POST['address']
        user_detail.bankaccount = request.POST['bankaccount']
    
        ## 새로운 비밀번호 가져오기
        new_password = request.POST['new_password']
        if new_password:
            user_detail.password = new_password

        # UserDetail 모델의 save() 메서드를 사용하여 변경된 정보 저장
        user_detail.save()

        # 비밀번호 업데이트
        if new_password:
            request.user.set_password(new_password)
            request.user.save()

        return redirect('account:mypage') 
    
    return render(request, 'mypage_edit.html', {'user_detail': user_detail})

def my_postings(request, user_id):
    # 해당 유저가 작성한 모든 포스팅 가져오기
    my_postings = Posting.objects.filter(writer__id=user_id)
    return render(request, 'my_postings.html', {'my_postings': my_postings})

def refund_request(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    
    user_detail = request.user.userdetail  # 유저의 UserDetail 객체 가져오기

    return render(request, 'refund_request.html', {'user_detail': user_detail})

def apply_refund(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    
    if request.method == 'POST':
        refund_amount = int(request.POST['refund'])
        user_detail = request.user.userdetail

        # 포인트가 충분한지 확인하고 충분하다면 환급 처리
        if user_detail.point >= refund_amount:
            user_detail.point -= refund_amount
            user_detail.save()

            # 환급 신청 후 메시지 표시
            messages.success(request, f'{refund_amount}점 환급 신청이 완료되었습니다.')
           
            # 관리자에게 알림 추가
            message = f"{request.user.username}님이 {refund_amount}점 환급 신청하였습니다. 계좌는 다음과 같습니다: {user_detail.bankaccount}"
            Notification.objects.create(user=request.user, message=message)
        
        else:
            # 포인트 부족 시 메시지 표시
            messages.error(request, '포인트가 부족하여 환급 신청을 완료할 수 없습니다.')

    # user_detail을 함께 템플릿에 전달
    return render(request, 'apply_refund.html', {'user_detail': user_detail})

@login_required
def admin_notifications(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to view this page.")
    notifications = Notification.objects.all()

    return render(request, 'admin_notifications.html', {'notifications': notifications})