from django.shortcuts import render, redirect
from .models import Posting
from django.urls import reverse
import zipfile
import os
from django.core.files import File
from django.contrib.auth.decorators import login_required


@login_required
def posting(request):
    if request.method == 'POST':
        # POST 요청 처리 로직
        title = request.POST.get('title')
        description = request.POST.get('description')
        example_picture = request.FILES.get('example_picture')
        example_description = request.POST.get('example_description')
        picture_zip = request.FILES.get('picture_zip')
        quantity = int(request.POST.get('quantity', 0))
        price = int(request.POST.get('price', 0))
        date = request.POST.get('date')

        if not title or not description or not quantity or not price or not date or not picture_zip:
            return render(request, 'create.html', {'에러': '필수 항목을 모두 작성해주세요'})
        
        # Posting 객체 생성
        posting = Posting.objects.create(
            writer=request.user,
            title=title,
            description=description,
            example_picture=example_picture,
            example_description=example_description,
            picture_zip=picture_zip, 
            quantity=quantity,
            price=price,
            date=date,
        )

        # total_amount 계산
        total_amount = quantity * price

        # confirmation.html로 이동, posting_id와 total_amount 전달
        return confirmation(request, posting_id=posting.id, total_amount=total_amount)
    return render(request, 'create.html')


def confirmation(request, posting_id, total_amount):
    # total_amount를 형변환하여 전달
    total_amount = int(total_amount)

    if request.method == 'POST':
        # POST 요청 처리 로직
        quantity = int(request.POST.get('quantity', 0))
        price = int(request.POST.get('price', 0))
        total_amount = quantity * price

    return render(request, 'confirmation.html', {'total_amount': total_amount})
