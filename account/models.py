from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    legalname = models.TextField(max_length=20)
    phone = models.TextField(null=True)
    address = models.TextField()
    bankaccount = models.TextField()
    username = models.CharField(max_length=40, unique=True, null=False)
    password = models.TextField(null=False)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"