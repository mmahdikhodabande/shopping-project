# Generated by Django 4.2.1 on 2023-05-29 11:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article_module', '0006_article_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.date(2023, 5, 29), verbose_name='زمان و تاریخ '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده '),
        ),
    ]