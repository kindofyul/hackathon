from django.db import models

# Create your models here.

class UserDetail(models.Model):
    legalname = models.TextField(max_length=20)
    phone = models.IntegerField()
    address = models.TextField()
    bankaccount = models.TextField()
    userid = models.CharField(max_length=30, unique=True)
    userpw = models.CharField(max_length = 128)
    point = 0
    
    def __str__(self):
        return self.title