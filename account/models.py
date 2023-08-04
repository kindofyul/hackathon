from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    legalname = models.TextField(max_length=20)
    phone = models.IntegerField(null=True, blank=True, default=0)
    address = models.TextField()
    bankaccount = models.TextField()
    userid = models.CharField(max_length=40, unique=True, null=False)
    userpw = models.TextField(null=False)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.userid