from django.db import models

# Create your models here.
from account_module.models import User


class add_email_for_off(models.Model):
    email = models.EmailField(max_length=100,
                              verbose_name='ایمیل مخاطب برای خبر نامه ')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده ')

    class Meta:
        verbose_name = 'ایمیل خبرنامه'
        verbose_name_plural = 'ایمیل ها برای خبرنامه'

    def __str__(self):
        return self.email
