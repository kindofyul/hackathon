from django.db import models

# Create your models here.

class UserDetail(models.Model):
    legalname = models.TextField(max_length=20)
    phone = models.IntegerField()
    address = models.TextField()
    bankaccount = models.TextField()
    userid = models.CharField(max_length = 40, unique = True, null = False, default=legalname)
    userpw = models.TextField(null = False, default = legalname)
    point = models.IntegerField(default=0)
    
    def __str__(self):
        return self.userid