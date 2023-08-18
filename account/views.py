from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from posting.views import *
from posting.models import *
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import DetailView, View
from django.core.serializers import serialize
import csv
import openpyxl
from .forms import AltTextForm
from bs4 import BeautifulSoup
import pandas as pd
from difflib import SequenceMatcher

def home(request):
    return render(request,'index.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'loginpage_heesu.html')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('account:home')
        else:
            return render(request, 'loginpage_heesu.html')
        
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
    return render(request,'mission-acting.html', {'postings':postings, 'posting_data': posting_data})

def mypage(request):
    return render(request,'mypage.html')

def commission(request):
    return posting(request)
    
def commissionneedlogin(request):
    return render(request, 'commissionneedlogin.html')

def contact(request):
    return render(request, 'contact.html')

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

    if 'export' in request.POST:
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="image_info.xlsx"'

        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = 'Image Info'

        worksheet.append(['이미지명', '이미지 해설'])

        for image in images[:posting.quantity]:
            description = image.description if image.description else "아직 입력되지 않았습니다"
            worksheet.append([image.image.name, description])

        workbook.save(response)

        return response

    return render(request, 'posting.html', {'posting':posting, 'images':images})

def refund_request(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    
    user_detail = request.user.userdetail  # 유저의 UserDetail 객체 가져오기

    return render(request, 'refund-1.html', {'user_detail': user_detail})

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
    return render(request, 'refund-2.html', {'user_detail': user_detail})

@login_required
def admin_notifications(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to view this page.")
    notifications = Notification.objects.all()

    return render(request, 'admin_notifications.html', {'notifications': notifications})

def detail_view_participate(request, pk):
    posting = get_object_or_404(Posting, pk=pk)
    images_without_description = posting.images.filter(description__isnull=True)
    image_ids = list(images_without_description.values_list('id', flat=True))

    if images_without_description.exists():
        image_index = 0
        request.session['total_images'] = 0  # 초기화
        request.session['total_reward'] = 0  # 초기화
        request.session['image_ids'] = image_ids
        request.session['listlength'] = posting.remaining_count
        return redirect('account:write_page_url', posting_id=posting.pk, image_index=image_index)
    else:
        return redirect('account:end', posting_id=posting.pk, image_index=image_index)
    
class PostingDetailView(DetailView):
    model = Posting
    template_name = 'mission-acting-example.html'
    context_object_name = 'posting'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posting = self.object
        images = posting.images.all()
        if images:
            context['first_image_index'] = 0
        return context

class ImageWriteView(View):
    template_name = 'mission-acting-writing-1.html'

    def get_image_from_session(self, image_id):
        return Image.objects.get(id=image_id)
    
    def get(self, request, posting_id, image_index):
        posting = get_object_or_404(Posting, pk=posting_id)
        image_ids = request.session.get('image_ids', [])
        listlength = request.session.get('listlength')

        if image_index < len(image_ids):
            image_id = request.session.get('image_ids', [])[image_index]
            image = self.get_image_from_session(image_id)
        else:
            return redirect('account:end', posting_id=posting.pk, image_index=image_index)
        
        context = {
            'posting': posting,
            'image': image,
            'image_index': image_index,
            'listlength':listlength,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, posting_id, image_index):
        posting = get_object_or_404(Posting, pk=posting_id)
        image_ids = request.session.get('image_ids', [])
        image_id = request.session.get('image_ids', [])[image_index]
        image = self.get_image_from_session(image_id)
        listlength = request.session.get('listlength')
        remaining_count = posting.remaining_count

        context = {
            'posting': posting,
            'image': image,
            'image_index': image_index,
            'listlength':listlength,
        }

        description = request.POST.get('description')

        if 'save_button' in request.POST:
            if description:
                image.description = description
                image.save()
                context['button_disabled'] = True  # 버튼 비활성화 변수 추가

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

            return render(request, self.template_name, context)
        
        if 'next_button' in request.POST:
            next_image_index = image_index + 1
            if next_image_index < len(image_ids):
                return redirect('account:write_page_url', posting_id=posting.pk, image_index=next_image_index)
            else:
                return redirect('account:end', posting_id=posting.pk, image_index=image_index)
            
        if 'end_button' in request.POST:     
            return redirect('account:end', posting_id=posting.pk, image_index=image_index)
        
        return redirect('account:end', posting_id=posting.pk, image_index=image_index)

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
            request.session['listlength'] = posting.remaining_count
            return redirect('account:explore')
        
    context = {
        'total_images': request.session.get('total_images', 0),
        'total_reward': request.session.get('total_reward', 0),
        'posting_id': posting_id,
        'image_index': image_index,
    }
    request.session.pop('image_ids', None)
    return render(request,'mission-acting-finish.html',context)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def alt_text_generator(request):
    if request.method == 'POST':
        form = AltTextForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            html_text = request.POST.get('html_text', '')  # Get HTML text from textarea
            
            # Process the uploaded Excel file to get image names and alt texts
            excel_data = get_excel_data(excel_file)  # Replace with your actual logic
            
            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(html_text, 'html.parser')
            
            # Loop through Excel data and update HTML with alt attributes
            for excel_item in excel_data:
                excel_image_name = excel_item['이미지명']
                excel_alt_text = excel_item['이미지 해설']
                
                best_match_tag = None
                best_similarity = 0
                
                img_tags = soup.find_all('img')
                for img_tag in img_tags:
                    img_src = img_tag.get('src', '')
                    similarity = similar(excel_image_name, img_src)
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match_tag = img_tag
                
                if best_match_tag:
                    best_match_tag['alt'] = excel_alt_text
            
            # Get the modified HTML
            modified_html = str(soup)
            
            return render(request, 'alt_text_generator.html', {'form': form, 'modified_html': modified_html})
    else:
        form = AltTextForm()
    return render(request, 'alt_text_generator.html', {'form': form})

def get_excel_data(excel_file):
    # Load Excel file using pandas
    df = pd.read_excel(excel_file)
    
    # Convert DataFrame to list of dictionaries
    excel_data = df.to_dict(orient='records')
    
    return excel_data