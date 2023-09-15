from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    avatar = models.FileField(upload_to='images/profile', verbose_name='تصویر آواتار', null=True, blank=True)
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل', editable=False)
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره نویسنده ')
    address = models.TextField(null=True, blank=True, verbose_name='نشانی منزل ')
    phone_number = models.IntegerField(null=True, blank=True, unique=True, verbose_name='شماره تماس')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username
