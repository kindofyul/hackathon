from django.db import models
import os
import zipfile
import shutil
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User


class Posting(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postings', blank=True, null=True)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=100)
    example_picture = models.ImageField(upload_to='example_pictures/', blank=True, null=True)
    example_description = models.TextField(max_length=100, blank=True, null=True)
    picture_zip = models.FileField(upload_to='picture_zips/', blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=False)
    price = models.PositiveIntegerField(blank=False)
    date = models.DateField()

    def __str__(self):
        return self.title


class Image(models.Model):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posted_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.posting.title} - Image {self.id}"


@receiver(post_save, sender=Posting)
def extract_images(sender, instance, **kwargs):
    if instance.picture_zip:
        # 압축 파일 열기
        zip_file_path = os.path.join(settings.MEDIA_ROOT, instance.picture_zip.name)
        # 압축 해제할 디렉토리 경로
        extract_to_directory = os.path.join(settings.MEDIA_ROOT, 'extracted_images', str(instance.id))

        # 압축 해제할 디렉토리 생성
        os.makedirs(extract_to_directory, exist_ok=True)

        # 압축 파일 열기
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # 압축 파일 내부의 이미지들을 모두 추출하여 임시 디렉토리에 저장
            for member in zip_ref.infolist():
                if "__MACOSX" not in member.filename and not member.filename.startswith("._"):
                    image_file_path = os.path.join(extract_to_directory, member.filename)
                    with open(image_file_path, 'wb') as image_file:
                        image_file.write(zip_ref.read(member.filename))

        # 추출된 이미지들의 경로를 가져와서 Image 모델에 저장
        for root, dirs, files in os.walk(extract_to_directory):
            for filename in files:
                # 이미지 파일의 절대 경로
                image_file_path = os.path.join(root, filename)
                # Image 모델에 이미지 저장
                image_instance = Image.objects.create(posting=instance)
                with open(image_file_path, 'rb') as image_file:
                    image_instance.image.save(filename, File(image_file))

        # 압축 해제된 디렉토리 삭제
        shutil.rmtree(extract_to_directory)
