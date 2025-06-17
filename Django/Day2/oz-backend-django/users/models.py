from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20) #이름
    description = models.TextField() #긴 문자열
    age = models.PositiveIntegerField(null=True) #나이
    gender = models.CharField(max_length=10) #성별

