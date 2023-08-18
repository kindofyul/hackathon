from django.contrib import admin
from django.urls import path, include
from account.views import *
from django.conf import settings
from django.conf.urls.static import static

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
    path('alt_text_generator/', alt_text_generator, name="alt_text_generator"), 
    path('posting/', include('posting.urls', namespace='posting')),  # 'posting' 앱의 URL 패턴을 include 합니다.
    path('mypage_edit/', mypage_edit, name='mypage_edit'),
    path('my_postings/', my_postings, name='my_postings'),
    path('posting/<int:posting_id>/', view_posting, name='posting'),
    path('refund_request/', refund_request, name='refund_request'),
    path('apply_refund/', apply_refund, name='apply_refund'),
    path('admin_notifications/', admin_notifications, name='admin_notifications'),
    path('post/<int:posting_id>/end/<int:image_index>/', end, name='end'),
    path('post/<int:pk>/', PostingDetailView.as_view(), name='posting_detail'),
    path('post/<int:posting_id>/write/<int:image_index>/', ImageWriteView.as_view(), name='write_page_url'),
    path('post/<int:pk>/participate/', detail_view_participate, name='participate_page_url'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)