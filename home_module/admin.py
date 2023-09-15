from django.contrib import admin
from . import models


# Register your models here.

class Add_email_display(admin.ModelAdmin):
    list_display = ['email', 'user']


admin.site.register(models.add_email_for_off)
