# Generated by Django 4.2.1 on 2023-07-02 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0005_alter_slider_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='ads_baner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان تبلیغ')),
                ('url', models.CharField(max_length=200, verbose_name='لینک تبلیغ')),
                ('position', models.CharField(choices=[('home_page', 'صفحه اصلی'), ('product_list', 'صفحه لیست محصولات ')], max_length=300, verbose_name='جایگاه نمایشی')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات تبلیغ')),
                ('image', models.ImageField(upload_to='images/sliders', verbose_name='تصویر تبلیغ')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال / غیرفعال')),
            ],
            options={
                'verbose_name': 'تبلیغ',
                'verbose_name_plural': 'تبلیغات ',
            },
        ),
    ]