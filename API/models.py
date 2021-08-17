from enum import Flag
from hashlib import blake2b
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class CustomAccountManager(BaseUserManager):
    def check_email(self,email:str):
        if not email:
            raise ValueError(_('提示：請輸入有效電子郵件！'))
    
    def check_passwords(self,pass_1:str,pass_2:str):
        if pass_1 != pass_2:
            raise ValidationError(_('提示：請輸入相同的密碼！'))

    def create_user(self,email,user,name,password,repassword,role,**other_fields):
        self.check_email(email)
        self.check_passwords(password,repassword)

        email = self.normalize_email(email)
        user = self.model(
            email=email,user=user,name=name,
            role=role,**other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,user,name,password,role,**other_fields):
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)

        if other_fields.get('is_active') is not True:
            raise ValueError(_('提示：請至電子郵箱激活電子郵件！'))

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('提示：管理員設定有誤！'))

        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('提示：超級用戶權限設定有誤！'))

        return self.create_user(email,user,name,password,password,role,**other_fields)

class Account(AbstractBaseUser,PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=20,null=False,unique=True)
    name = models.CharField(_('Name'),max_length=20,null=False)
    email = models.EmailField(_('Email Address'),unique=True,null=True)
    role = models.SmallIntegerField(_('Option: \n [0] User \n [1] Researcher \n Your role number is'),default=0,null=False)
    hash_value = models.CharField(max_length=25,blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    dt_register = models.DateTimeField(default=timezone.now)
    dt_last_updated = models.DateTimeField(default=timezone.now)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = ['email','name','role']

class SymbolHistoryData(models.Model):
    symbol = models.CharField(max_length=10,null=False,blank=False)
    open_price = models.FloatField(null=False,blank=False)
    high_price = models.FloatField(null=False,blank=False) 
    low_price = models.FloatField(null=False,blank=False)
    close_price = models.FloatField(null=False,blank=False)
    volume = models.FloatField(default=False,null=False,blank=False)
    kline_size = models.CharField(default=False,max_length=5,null=False,blank=False)
    datetime = models.DateTimeField(null=False,blank=False)
    
    class Meta:
        unique_together = ('symbol','datetime')

class ResearcherModel(models.Model):
    id_researcher = models.IntegerField(primary_key=True,unique=True)
    model_name = models.CharField(default=False,max_length=20,null=False,blank=True)
    dt_created = models.DateTimeField(default=timezone.now)

