from django.contrib import admin
from . import models


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_filter = ['category', 'is_active']
    list_display = ['title', 'price', 'is_active', 'is_delete']
    list_editable = ['price', 'is_active']


class ProductVIsit(admin.ModelAdmin):
    list_display = ['product', 'ip', 'user']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductBrand)
admin.site.register(models.product_visit, ProductVIsit)
admin.site.register(models.gallery_product)
