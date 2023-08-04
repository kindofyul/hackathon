from django.contrib import admin
from django.urls import path, include
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
    path('posting/', include('posting.urls', namespace='posting')),  # 'posting' 앱의 URL 패턴을 include 합니다.
    path('mypage_edit/', mypage_edit, name='mypage_edit'),
    path('my_postings/<int:user_id>/', my_postings, name='my_postings'),
    path('refund_request/', refund_request, name='refund_request'),
    path('apply_refund/', apply_refund, name='apply_refund'),
    path('admin_notifications/', admin_notifications, name='admin_notifications'),
]
