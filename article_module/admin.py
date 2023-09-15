from django.contrib import admin
from . import models
from .models import Article
from django.http import HttpRequest


# Register your models here.

class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'parent', 'is_active']
    list_editable = ['url_title', 'parent', 'is_active']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'author']
    list_editable = ['is_active']

    def save_model(self, request: HttpRequest, obj: Article, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)


class Article_comment_display(admin.ModelAdmin):
    list_display = ['user', 'article', 'parent']


admin.site.register(models.ArticleCategory, ArticleCategoryAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Article_comment, Article_comment_display)
