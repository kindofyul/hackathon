from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from posting.views import *
from posting.models import *
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, View


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
    postings = Posting.objects.all()
    posting_data = []
    for posting in postings:
        posting_data.append({
            'title': posting.title, 
            'price':posting.price, 
            'remaining_count': posting.remaining_count,
        })
    return render(request,'explore.html', {'postings':postings, 'posting_data': posting_data})

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

def my_postings(request):
    # 해당 유저가 작성한 모든 포스팅 가져오기
    user = request.user
    my_postings = Posting.objects.filter(writer=user)
    return render(request, 'my_postings.html', {'my_postings': my_postings})

def view_posting(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    images = posting.images.all()
    return render(request, 'posting.html', {'posting':posting, 'images':images})

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

def detail_view_participate(request, pk):
    posting = get_object_or_404(Posting, pk=pk)
    images_without_description = posting.images.filter(description__isnull=True)
    
    if images_without_description.exists():
        image_index = 0
        request.session['total_images'] = 0  # 초기화
        request.session['total_reward'] = 0  # 초기화
        return redirect('account:write_page_url', posting_id=posting.pk, image_index=image_index)
    else:
        return redirect('account:end', posting_id=posting.pk, image_index=image_index)
    
class PostingDetailView(DetailView):
    model = Posting
    template_name = 'detail.html'
    context_object_name = 'posting'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posting = self.object
        images = posting.images.all()
        if images:
            context['first_image_index'] = 0
        return context

class ImageWriteView(View):
    template_name = 'write.html'

    def get(self, request, posting_id, image_index):
        posting = get_object_or_404(Posting, pk=posting_id)
        images = posting.images.filter(description__isnull=True)
        if image_index < posting.remaining_count:
            image = images[image_index]
            image_index = images.filter(id__lte=image.id).count() - 1
            return render(request, self.template_name, {'posting': posting, 'image': image, 'image_index': image_index})
        else:
            return redirect('account:end', posting_id=posting.pk, image_index=image_index)

    def post(self, request, posting_id, image_index):
        posting = get_object_or_404(Posting, pk=posting_id)
        images_without_description = posting.images.filter(description__isnull=True)
        remaining_count = posting.remaining_count

        if image_index < len(images_without_description):
            request.session['image_index'] = image_index
            image = images_without_description[image_index]
            description = request.POST.get('description')
            if description:
                image.description = description
                image.save()

                # remaining_count 하나씩 차감하기 
                remaining_count -= 1
                if remaining_count < 0:
                    remaining_count = 0

                # remaining_count 업데이트
                posting.remaining_count = remaining_count
                posting.save()

                # 이미지 설명 저장 시 total_images와 total_reward 업데이트
                request.session['total_images'] = request.session.get('total_images', 0) + 1
                reward_per_image = posting.price
                request.session['total_reward'] = request.session.get('total_reward', 0) + reward_per_image
            
            if 'save_button' in request.POST:
                return render(request, self.template_name, {'posting': posting, 'image': image, 'image_index': image_index})
            
            if 'next_button' in request.POST:  # '넘어가기' 버튼이 눌렸을 때
                image_index += 1
                while image_index < len(images_without_description) and images_without_description[image_index].description:
                    image_index += 1
                if image_index < len(images_without_description):
                    # 이미지 인덱스를 다음 설명이 없는 이미지의 인덱스로 업데이트
                    return redirect('account:write_page_url', posting_id=posting.pk, image_index=image_index)
                else:
                    # 이미지 인덱스가 이미지 개수를 초과하면 write.html로 리다이렉트
                    return render(request, self.template_name, {'posting': posting, 'image': image, 'image_index': image_index})
            
        return render(request, self.template_name, {'posting': posting, 'image': image, 'image_index': image_index, 'images_without_description':images_without_description})
    
def end(request, posting_id, image_index):
    posting = get_object_or_404(Posting, id=posting_id)
    
    #UserDetail에 리워드 저장
    user_detail, created = UserDetail.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'complete':
            total_reward = request.session.get('total_reward', 0)
            user_detail.point += total_reward
            user_detail.save()
            request.session['total_images'] = 0
            request.session['total_reward'] = 0
            request.session['image_index'] = 0
            return redirect('account:explore')
        
    context = {
        'total_images': request.session.get('total_images', 0),
        'total_reward': request.session.get('total_reward', 0),
        'posting_id': posting_id,
        'image_index': image_index,
    }

    return render(request,'end.html',context)
