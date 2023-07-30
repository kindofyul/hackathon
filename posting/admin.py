from django.contrib import admin
from .models import *

class ImageInline(admin.TabularInline):  # 혹은 StackedInline을 사용합니다.
    model = Image
    extra = 1  # 기본적으로 1개의 Image 입력 폼이 보이도록 설정합니다.

@admin.register(Posting)
class PostingAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass