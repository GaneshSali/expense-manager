from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone

class User(AbstractUser):
    password = models.CharField(blank=True, max_length=128)


class Balance(models.Model):
    user = models.ForeignKey(User, related_name="balance" ,on_delete=models.CASCADE)
    account = models.CharField(max_length=20)
    balance = models.FloatField(blank=True,default=0)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    user = models.ForeignKey(User, related_name="category" ,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    c_type = models.CharField(max_length=20,blank=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Data(models.Model):
    user = models.ForeignKey(User, related_name="data" ,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="data" ,on_delete=models.CASCADE)
    account = models.ForeignKey(Balance, related_name="data" ,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    amount = models.FloatField()
    c_type = models.CharField(max_length=20,blank=True)
    is_delete = models.BooleanField(default=False)
    timestamp = models.DateTimeField(blank=True,default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)